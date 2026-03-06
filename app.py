import streamlit as st # type: ignore
from data import (
    CATEGORIES,
    COMMON_FORMS,
    get_level2_options,
    get_alloy_options,
    get_metal_temper_options,
    get_ams,
    get_phenolic_spec,
    get_cable_prefix,
    get_plastic_grade_options,
    get_plastic_variant_options,
    build_part_number,
    # we'll add more helpers later
)

# ───────────────────────────────────────────────
# Page config – must be the first Streamlit command
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="Raw Material PN Generator",
    page_icon="🛠️",
    layout="centered",
)

# Dark / defense-tech inspired styling
st.markdown(
    """
    <style>
        /* === 1. Global Theme & Font ===================================== */
        /* Sets dark background and light text for the entire app */
        .stApp {
            background-color: #0b0f14;
        }

        /* Force monospace font everywhere (your defense-tech look) */
        html, body, [class*="st-"] * {
            font-family: 'Consolas', 'Courier New', monospace !important;
        }

        /* All text (paragraphs, labels, etc.) gets light color */
        p, div, label, .stMarkdown, span {
            color: #e6edf3 !important;
        }

        /* === 2. Headers ================================================== */
        /* Main title and all headings */
        h1, h2, h3, h4, h5, h6 {
            color: #e6edf3 !important;
        }

        /* Main title (h1) – control font size independently */
        h1 {
            font-size: 2.2rem !important;          /* ← change this number to experiment */
            margin-bottom: -1.5rem !important;      /* optional: controls gap to divider */
            line-height: 1.2 !important;           /* optional: tighter if very large */
        }

        /* Subheaders (h3) – lighter weight, smaller bottom margin */
        h3 {
            font-weight: 400 !important;        /* normal weight instead of bold */
            color: #a5b4d1 !important;          /* softer gray for hierarchy */
            margin-bottom: 0.0rem !important;   /* controls gap to next element */
            font-size: 1.3rem !important;       /* slightly smaller than default */
        }

        /* === 3. Form Inputs (dropdowns & text boxes) ===================== */
        /* Dark background, light text, visible border */
        .stSelectbox > div > div > div,
        .stTextInput > div > div > input {
            background-color: #1f2a44 !important;
            color: #e6edf3 !important;
            border: 1px solid #3b4a6b !important;
            font-size: 0.95rem !important;
            padding: 0.5rem 0.5rem !important;  /* smaller padding = tighter look */
        }

        /* Remove white/bright container behind dropdowns */
        .stSelectbox > div {
            background-color: transparent !important;
        }

        /* Smaller labels above inputs */
        .stSelectbox label,
        .stTextInput label {
            font-size: 0.95rem !important;
            margin-bottom: 0.2rem !important;
            color: #a5b4d1 !important;
        }

        /* === 4. Vertical Spacing & Layout Tightening ===================== */
        /* Main content container – reduces top/bottom padding of whole page */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }

        /* Space below every input widget (dropdown, text box) */
        .stSelectbox,
        .stTextInput {
            margin-bottom: 0.0rem !important;   /* was probably 1–1.5rem */
        }

        /* Dividers (hr) – very tight spacing */
        hr {
            background-color: #3b4a6b !important;
            margin-top: 0.0rem !important;
            margin-bottom: 0.0rem !important;
        }

        
    </style>
    """,
    unsafe_allow_html=True
)

# ───────────────────────────────────────────────
# Title only (no caption, no extra text)
# ───────────────────────────────────────────────
st.title("Raw Material Part Number Generator")
st.divider()

# ───────────────────────────────────────────────
# 1. Category
# ───────────────────────────────────────────────
if "category" not in st.session_state:
    st.session_state.category = ""

st.subheader("Category")
category_options = [""] + CATEGORIES   # "" is the blank/placeholder first option
selected_category = st.selectbox(
    "Category",
    options=category_options,
    index=category_options.index(st.session_state.get("category", "")) 
    if st.session_state.get("category", "") in category_options else 0,
    label_visibility="collapsed",
    key="category_select"
)
if selected_category != st.session_state.category:
    st.session_state.category = selected_category


# ───────────────────────────────────────────────
# 2. Second level – only show after category selected
# ───────────────────────────────────────────────
if st.session_state.get("category", "") != "":
    st.divider()

    level2_label = {
        "Metals": "Material",
        "Phenolics": "Phenolic Type",
        "Plastics": "Plastic Family",
        "Electrical Cable": "Cable Type",
    }.get(st.session_state.category, "Type")

    st.subheader(level2_label)

    options = get_level2_options(st.session_state.category)

    
    level2_key = f"level2_{st.session_state.category.replace(' ', '_')}"

    selected_level2 = st.selectbox(
        level2_label,
        options=options,
        # Use the same consistent key for index lookup
        index=options.index(st.session_state.get(level2_key, ""))
            if st.session_state.get(level2_key, "") in options else 0,
        label_visibility="collapsed",
        key=level2_key   # ← now widget writes directly to the key the app uses
    )

    
    # ───────────────────────────────────────────────
    # 3. Third level – examples for Metals and Plastics
    # ───────────────────────────────────────────────
    show_third = False
    third_label = ""
    third_options = [""]

    if st.session_state.category == "Metals" and st.session_state.get("level2_Metals"):
        show_third = True
        third_label = "Alloy / Grade"
        third_options = get_alloy_options(st.session_state["level2_Metals"])

    elif st.session_state.category == "Plastics" and st.session_state.get("level2_Plastics"):
        show_third = True
        third_label = "Material / Grade"
        third_options = [""] + get_plastic_grade_options(st.session_state["level2_Plastics"])

    elif st.session_state.category in ("Phenolics", "Electrical Cable"):
        show_third = False

    if show_third:
        st.divider()
        st.subheader(third_label)

        widget_key = f"third_{st.session_state.category.replace(' ', '_')}"



        selected_third = st.selectbox(
            third_label,
            options=third_options,
            #index=0,                            # we want blank
            label_visibility="collapsed",
            key=widget_key
        )       
    
    
    st.write(f"DEBUG: alloy value just after selectbox = '{st.session_state.get('third_Metals', 'NOT SET')}'")
    
    
    
    # ───────────────────────────────────────────────
    # Electrical Cable specific fields – only after cable type selected
    # ───────────────────────────────────────────────
    show_cable_details = False

    if st.session_state.category == "Electrical Cable" and st.session_state.get("level2_Electrical_Cable"):
        show_cable_details = True


    if show_cable_details:
        st.divider()
        st.subheader("Cable Specifications")

        cable_type = st.session_state.get("level2_Electrical_Cable", "")

        # ───────────────────────────────────────────────
        # Fields specific to each cable type
        # ───────────────────────────────────────────────
        required_filled = False

        if "Single-Conductor" in cable_type:
            col1, col2, col3 = st.columns(3)

            with col1:
                slash_sheet = st.text_input(
                    "Slash Sheet Number",
                    value=st.session_state.get("cable_slash", ""),
                    key="cable_slash",
                    placeholder="e.g. AS22759/[Slash Sheet Number]"
                )

            with col2:
                awg_size = st.text_input(
                    "AWG / Size",
                    value=st.session_state.get("cable_awg_size", ""),
                    key="cable_awg_size",
                    placeholder="e.g. 20"
                )

            with col3:
                color_code = st.text_input(
                    "Color Code(from AS22759)",
                    value=st.session_state.get("cable_color", ""),
                    key="cable_color",
                    placeholder="e.g. 0=Black.....9=White"
                )

            required_filled = bool(slash_sheet.strip())

        elif "Multi-Conductor" in cable_type:
            config_code = st.text_input(
                "Configuration Code",
                value=st.session_state.get("cable_config", ""),
                key="cable_config",
                placeholder="e.g. WC27500-[Configuration Code]"
            )

            required_filled = bool(config_code.strip())

        elif "Coaxial" in cable_type:
            slash_sheet = st.text_input(
                "Slash Sheet Number",
                value=st.session_state.get("cable_slash", ""),
                key="cable_slash",
                placeholder="e.g. M17/[Slash Sheet Number]"
            )

            required_filled = bool(slash_sheet.strip())

        else:
            st.warning("Please select a valid cable type.")
            required_filled = False

        # ───────────────────────────────────────────────
        # Common: Spool? dropdown (shown for all types)
        # ───────────────────────────────────────────────
        spool_options = ["No", "Yes"]
        spool_choice = st.selectbox(
            "Spool?",
            options=spool_options,
            index=spool_options.index(st.session_state.get("cable_spool", "No"))
                if st.session_state.get("cable_spool", "No") in spool_options else 0,
            key="cable_spool",
            label_visibility="visible"
        )

        # Length – only if Yes
        length = ""
        if spool_choice == "Yes":
            length = st.text_input(
                "Length of Spool",
                value=st.session_state.get("cable_length", ""),
                key="cable_length",
                placeholder="e.g. 1000 ft or 500 m"
            )

        # ───────────────────────────────────────────────
        # Generate button – enabled when required field(s) are filled
        # ───────────────────────────────────────────────
        if required_filled:
            if st.button("Generate Part Number", type="primary", use_container_width=True):
                pn = build_part_number(st.session_state)
                st.session_state.generated_pn = pn

        if "generated_pn" in st.session_state:
            pn = st.session_state.generated_pn

            #st.subheader("Generated Part Number")
            st.markdown(
                """
                <style>
                    /* Tighten spacing just for this PN output area */
                    .pn-container {
                        margin-top: 0.0rem !important;      /* less space above the box */
                        margin-bottom: 1rem !important;
                    }
                    .pn-box {
                        font-size: 1.8rem;
                        font-weight: bold;
                        font-family: 'Consolas', 'Courier New', monospace;
                        background-color: #1f2a44;
                        padding: 0.8rem 1.2rem !important;   /* reduced top/bottom padding */
                        border-radius: 0.5rem;
                        border: 1px solid #3b4a6b;
                        color: #e6edf3;
                        white-space: pre-wrap;
                        word-break: break-all;
                        line-height: 1.3;                     /* tighter line height if multi-line */
                    }
                    /* Reduce default margin below subheader when followed by PN */
                    .stSubheader + .pn-container {
                        margin-top: -0.5rem !important;       /* pull box closer to subheader */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="pn-container"><div class="pn-box">{pn}</div></div>',
                unsafe_allow_html=True
            )

                                        
        
    # ───────────────────────────────────────────────
    # 4. Fourth level – Condition / Temper (only for Metals)
    # ───────────────────────────────────────────────
    show_fourth = False
    fourth_label = ""
    fourth_options = [""]

    if st.session_state.category == "Metals":
        material    = st.session_state.get("level2_Metals", "")
        alloy       = st.session_state.get("third_Metals", "")
        
        if material and alloy:
            show_fourth = True
            fourth_label = "Condition / Temper"
            fourth_options = [""] + get_metal_temper_options(material, alloy)
    
    
    #st.write(f"Debug: material = '{material}', alloy = '{alloy}', show_fourth = {show_fourth}")


    if show_fourth:
        st.divider()
        st.subheader(fourth_label)

        widget_key = "fourth_Metals"

        # ─── Insert the initialization here ────────────────────────────────
        temper_key = "level4_Metals"   # or "fourth_Metals" to match your naming

        if temper_key not in st.session_state:
            st.session_state[temper_key] = ""

        # Force reset to blank when upstream (material or alloy) changes
        fresh_key = f"fresh_fourth_Metals_{material}_{alloy}"
        
        if fresh_key not in st.session_state:
            st.session_state[fresh_key] = True
            if widget_key in st.session_state:
                del st.session_state[widget_key]
            # Also reset the stored temper value
            if temper_key in st.session_state:
                st.session_state[temper_key] = ""

        selected_fourth = st.selectbox(
            fourth_label,
            options=fourth_options,
            index=fourth_options.index(st.session_state.get(temper_key, "")),
            label_visibility="collapsed",
            key=widget_key
        )

    # ───────────────────────────────────────────────
    # 4. Fourth level – Variant / Color (only for Plastics)
    # ───────────────────────────────────────────────
    show_variant = False
    variant_options = [""]

    if st.session_state.category == "Plastics":
        grade = st.session_state.get("third_Plastics", "")
        if grade:
            show_variant = True
            variant_options = [""] + get_plastic_variant_options(grade)

    if show_variant:
        st.divider()
        st.subheader("Variant / Color / Fill")
        widget_key = "fourth_Plastics"

        fresh_key = f"fresh_variant_Plastics_{grade}"
        if fresh_key not in st.session_state:
            st.session_state[fresh_key] = True
            if widget_key in st.session_state:
                del st.session_state[widget_key]
            if "variant_Plastics" in st.session_state:
                del st.session_state["variant_Plastics"]

        selected_variant = st.selectbox(
            "Variant / Color / Fill",
            options=variant_options,
            index=variant_options.index(st.session_state.get("variant_Plastics", "")) 
            if st.session_state.get("variant_Plastics", "") 
            in variant_options 
            else 0,
            label_visibility="collapsed",
            key=widget_key
        )

        if "variant_Plastics" not in st.session_state:
            st.session_state.variant_Plastics = ""
        if selected_variant != st.session_state.variant_Plastics:
            st.session_state.variant_Plastics = selected_variant

    # ───────────────────────────────────────────────
    # Form – shared for Metals, Phenolics, Plastics
    # ───────────────────────────────────────────────
    show_form = False
    form_options = [""] + COMMON_FORMS

    if st.session_state.category in ("Metals", "Phenolics", "Plastics"):
        # Determine if upstream selections are complete
        if st.session_state.category == "Metals":
            upstream_complete = bool(
                st.session_state.get("level2_Metals") and
                st.session_state.get("third_Metals") and
                st.session_state.get("fourth_Metals") and
                st.session_state.fourth_Metals != "" # make sure temper isn't just blank
            )
        
        elif st.session_state.category == "Phenolics":
            upstream_complete = bool(st.session_state.get("level2_Phenolics"))
        
        elif st.session_state.category == "Plastics":
            upstream_complete = bool(
                st.session_state.get("level2_Plastics") and
                st.session_state.get("third_Plastics") and
                st.session_state.get("variant_Plastics") and
                st.session_state.variant_Plastics != "" #make sure variant isn't just blank
            )

        if upstream_complete:
            show_form = True

    if show_form:
        st.divider()
        st.subheader("Form")

        widget_key = f"form_{st.session_state.category.replace(' ', '_')}"

        # ─── Initialize form key only when we are actually showing the widget ───
        if "form" not in st.session_state:
            st.session_state.form = ""

        # Reset when upstream changes (similar pattern you already use)
        fresh_key = f"fresh_form_{st.session_state.category}_{st.session_state.get('level2_' + st.session_state.category, '')}"
        if fresh_key not in st.session_state:
            st.session_state[fresh_key] = True
            if widget_key in st.session_state:
                del st.session_state[widget_key]
            st.session_state.form = ""  # reset

        selected_form = st.selectbox(
            "Form",
            options=form_options,
            index=form_options.index(st.session_state.form) if st.session_state.form in form_options else 0,
            label_visibility="collapsed",
            key=widget_key
        )

        if selected_form != st.session_state.form:
            st.session_state.form = selected_form


        #───────────────────────────────────────────────────────────────────────────
        # ─── Dimension inputs – only when Form is selected ────────────────────────
        #───────────────────────────────────────────────────────────────────────────
        if st.session_state.form and st.session_state.form != "":

            # Raw input strings (what user types)
            if "dim_thickness" not in st.session_state:
                st.session_state.dim_thickness = ""
            if "dim_width" not in st.session_state:
                st.session_state.dim_width = ""
            if "dim_diameter" not in st.session_state:
                st.session_state.dim_diameter = ""
            if "dim_wall_thickness" not in st.session_state:
                st.session_state.dim_wall_thickness = ""
            if "dim_od" not in st.session_state:
                st.session_state.dim_od = ""

            # Confirmation flag – starts False every time Form changes
            if "dimensions_confirmed" not in st.session_state:
                st.session_state.dimensions_confirmed = False

            # Parsed numbers – only set after successful confirmation
            if "parsed_thickness" not in st.session_state:
                st.session_state.parsed_thickness = None
            if "parsed_width" not in st.session_state:
                st.session_state.parsed_width = None
            # ... same for diameter, wall, od if needed

            st.divider()
            st.subheader("Dimensions")

            form = st.session_state.form

            if form == "Sheet (thickness <= 0.25\")":
                col1, col2 = st.columns(2)
                with col1:
                    thickness = st.text_input(
                        "Thickness (inches)",
                        value=st.session_state.dim_thickness,
                        key="dim_thickness_input",
                        placeholder="e.g. 0.250"
                    )
                with col2:
                    width = st.text_input(
                        "Width (inches)",
                        value=st.session_state.dim_width,
                        key="dim_width_input",
                        placeholder="e.g. 48"
                    )

                # Store raw values
                st.session_state.dim_thickness = thickness
                st.session_state.dim_width = width

            elif form == "Plate/Bar (thickness > 0.25\")":
                col1, col2 = st.columns(2)
                with col1:
                    thickness = st.text_input(
                        "Thickness (inches)",
                        value=st.session_state.dim_thickness,
                        key="dim_thickness_input_plate",
                        placeholder="e.g. 0.250"
                    )
                with col2:
                    width = st.text_input(
                        "Width (inches)",
                        value=st.session_state.dim_width,
                        key="dim_width_input_plate",
                        placeholder="e.g. 12"
                    )

                st.session_state.dim_thickness = thickness
                st.session_state.dim_width = width

            elif form == "Rod":
                diameter = st.text_input(
                    "Diameter (inches)",
                    value=st.session_state.dim_diameter,
                    key="dim_diameter_input",
                    placeholder="e.g. 1.0"
                )
                st.session_state.dim_diameter = diameter

            elif form == "Tube":
                col1, col2 = st.columns(2)
                with col1:
                    wall = st.text_input(
                        "Wall Thickness (inches)",
                        value=st.session_state.dim_wall_thickness,
                        key="dim_wall_input",
                        placeholder="e.g. 0.065"
                    )
                with col2:
                    od = st.text_input(
                        "Outer Diameter (inches)",
                        value=st.session_state.dim_od,
                        key="dim_od_input",
                        placeholder="e.g. 1.0"
                    )

                st.session_state.dim_wall_thickness = wall
                st.session_state.dim_od = od

            else:
                st.info("No dimensions required for this form.", icon="ℹ️")

            if st.button("Confirm Dimensions", type="primary", use_container_width=True):

                # Reset confirmation status first
                st.session_state.dimensions_confirmed = False
                st.session_state.parsed_thickness = None
                # ... reset other parsed values if you add them

                try:
                    if form in ["Sheet (thickness <= 0.25\")", "Plate/Bar (thickness > 0.25\")"]:
                        thick_str = st.session_state.dim_thickness.strip()
                        width_str = st.session_state.dim_width.strip()

                        if not thick_str or not width_str:
                            st.error("Both thickness and width are required.")
                            st.stop()

                        thickness_val = float(thick_str)
                        width_val = float(width_str)

                        if thickness_val <= 0:
                            st.error("Thickness must be greater than 0.")
                            st.stop()

                        # Form-specific thickness check
                        if form == "Sheet (thickness <= 0.25\")" and thickness_val > 0.25:
                            st.error("Sheet thickness must be ≤ 0.25 inches.")
                            st.stop()
                        elif form == "Plate/Bar (thickness > 0.25\")" and thickness_val <= 0.25:
                            st.error("Plate/Bar thickness must be > 0.25 inches.")
                            st.stop()

                        # Store parsed values
                        st.session_state.parsed_thickness = thickness_val
                        st.session_state.parsed_width = width_val
                        st.session_state.dimensions_confirmed = True
                        st.success("Dimensions confirmed!")

                    elif form == "Rod":
                        dia_str = st.session_state.dim_diameter.strip()
                        if not dia_str:
                            st.error("Diameter is required.")
                            st.stop()
                        dia_val = float(dia_str)
                        if dia_val <= 0:
                            st.error("Diameter must be greater than 0.")
                            st.stop()
                        st.session_state.parsed_diameter = dia_val
                        st.session_state.dimensions_confirmed = True
                        st.success("Dimensions confirmed!")

                    elif form == "Tube":
                        wall_str = st.session_state.dim_wall_thickness.strip()
                        od_str = st.session_state.dim_od.strip()

                        if not wall_str or not od_str:
                            st.error("Both wall thickness and OD are required.")
                            st.stop()

                        wall_val = float(wall_str)
                        od_val = float(od_str)

                        if wall_val <= 0 or od_val <= 0:
                            st.error("Wall thickness and OD must be greater than 0.")
                            st.stop()

                        st.session_state.parsed_wall = wall_val
                        st.session_state.parsed_od = od_val
                        st.session_state.dimensions_confirmed = True
                        st.success("Dimensions confirmed!")

                except ValueError:
                    st.error("All inputs must be valid numbers (e.g. 0.250, 1.0, 48).")


                # ─── Generate button – only show when confirmed ────────────────────────
            if st.session_state.dimensions_confirmed:
                if st.button(
                    "Generate Part Number", 
                    type="primary", 
                    use_container_width=True,
                    key="generate_part_number_btn"
                ):
                    pn = build_part_number(st.session_state)
                    st.session_state.generated_pn = pn
                

                if "generated_pn" in st.session_state:
                    pn = st.session_state.generated_pn

                    #st.subheader("Generated Part Number")
                    st.markdown(
                        """
                        <style>
                            /* Tighten spacing just for this PN output area */
                            .pn-container {
                                margin-top: 0.0rem !important;      /* less space above the box */
                                margin-bottom: 1rem !important;
                            }
                            .pn-box {
                                font-size: 1.8rem;
                                font-weight: bold;
                                font-family: 'Consolas', 'Courier New', monospace;
                                background-color: #1f2a44;
                                padding: 0.8rem 1.2rem !important;   /* reduced top/bottom padding */
                                border-radius: 0.5rem;
                                border: 1px solid #3b4a6b;
                                color: #e6edf3;
                                white-space: pre-wrap;
                                word-break: break-all;
                                line-height: 1.3;                     /* tighter line height if multi-line */
                            }
                            /* Reduce default margin below subheader when followed by PN */
                            .stSubheader + .pn-container {
                                margin-top: -0.5rem !important;       /* pull box closer to subheader */
                            }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="pn-container"><div class="pn-box">{pn}</div></div>',
                        unsafe_allow_html=True
                    )

                                        
import streamlit as st # type: ignore
from data import (
    CATEGORIES,
    COMMON_FORMS,
    get_level2_options,
    get_alloy_options,
    get_metal_temper_options,
    get_ams,
    get_phenolic_spec,
    get_cable_prefix,
    get_plastic_grade_options,
    get_plastic_variant_options,
    build_part_number,
    # we'll add more helpers later
)

# ───────────────────────────────────────────────
# Page config – must be the first Streamlit command
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="Raw Material PN Generator",
    page_icon="🛠️",
    layout="centered",
)

# Dark / defense-tech inspired styling
st.markdown(
    """
    <style>
        /* === 1. Global Theme & Font ===================================== */
        /* Sets dark background and light text for the entire app */
        .stApp {
            background-color: #0b0f14;
        }

        /* Force monospace font everywhere (your defense-tech look) */
        html, body, [class*="st-"] * {
            font-family: 'Consolas', 'Courier New', monospace !important;
        }

        /* All text (paragraphs, labels, etc.) gets light color */
        p, div, label, .stMarkdown, span {
            color: #e6edf3 !important;
        }

        /* === 2. Headers ================================================== */
        /* Main title and all headings */
        h1, h2, h3, h4, h5, h6 {
            color: #e6edf3 !important;
        }

        /* Main title (h1) – control font size independently */
        h1 {
            font-size: 2.2rem !important;          /* ← change this number to experiment */
            margin-bottom: -1.5rem !important;      /* optional: controls gap to divider */
            line-height: 1.2 !important;           /* optional: tighter if very large */
        }

        /* Subheaders (h3) – lighter weight, smaller bottom margin */
        h3 {
            font-weight: 400 !important;        /* normal weight instead of bold */
            color: #a5b4d1 !important;          /* softer gray for hierarchy */
            margin-bottom: 0.0rem !important;   /* controls gap to next element */
            font-size: 1.3rem !important;       /* slightly smaller than default */
        }

        /* === 3. Form Inputs (dropdowns & text boxes) ===================== */
        /* Dark background, light text, visible border */
        .stSelectbox > div > div > div,
        .stTextInput > div > div > input {
            background-color: #1f2a44 !important;
            color: #e6edf3 !important;
            border: 1px solid #3b4a6b !important;
            font-size: 0.95rem !important;
            padding: 0.5rem 0.5rem !important;  /* smaller padding = tighter look */
        }

        /* Remove white/bright container behind dropdowns */
        .stSelectbox > div {
            background-color: transparent !important;
        }

        /* Smaller labels above inputs */
        .stSelectbox label,
        .stTextInput label {
            font-size: 0.95rem !important;
            margin-bottom: 0.2rem !important;
            color: #a5b4d1 !important;
        }

        /* === 4. Vertical Spacing & Layout Tightening ===================== */
        /* Main content container – reduces top/bottom padding of whole page */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }

        /* Space below every input widget (dropdown, text box) */
        .stSelectbox,
        .stTextInput {
            margin-bottom: 0.0rem !important;   /* was probably 1–1.5rem */
        }

        /* Dividers (hr) – very tight spacing */
        hr {
            background-color: #3b4a6b !important;
            margin-top: 0.0rem !important;
            margin-bottom: 0.0rem !important;
        }

        
    </style>
    """,
    unsafe_allow_html=True
)

# ───────────────────────────────────────────────
# Title only (no caption, no extra text)
# ───────────────────────────────────────────────
st.title("Raw Material Part Number Generator")
st.divider()

# ───────────────────────────────────────────────
# 1. Category
# ───────────────────────────────────────────────
if "category" not in st.session_state:
    st.session_state.category = ""

st.subheader("Category")
category_options = [""] + CATEGORIES   # "" is the blank/placeholder first option
selected_category = st.selectbox(
    "Category",
    options=category_options,
    index=category_options.index(st.session_state.get("category", "")) 
    if st.session_state.get("category", "") in category_options else 0,
    label_visibility="collapsed",
    key="category_select"
)
if selected_category != st.session_state.category:
    st.session_state.category = selected_category


# ───────────────────────────────────────────────
# 2. Second level – only show after category selected
# ───────────────────────────────────────────────
if st.session_state.get("category", "") != "":
    st.divider()

    level2_label = {
        "Metals": "Material",
        "Phenolics": "Phenolic Type",
        "Plastics": "Plastic Family",
        "Electrical Cable": "Cable Type",
    }.get(st.session_state.category, "Type")

    st.subheader(level2_label)

    options = get_level2_options(st.session_state.category)

    
    level2_key = f"level2_{st.session_state.category.replace(' ', '_')}"

    selected_level2 = st.selectbox(
        level2_label,
        options=options,
        # Use the same consistent key for index lookup
        index=options.index(st.session_state.get(level2_key, ""))
            if st.session_state.get(level2_key, "") in options else 0,
        label_visibility="collapsed",
        key=level2_key   # ← now widget writes directly to the key the app uses
    )

    
    # ───────────────────────────────────────────────
    # 3. Third level – examples for Metals and Plastics
    # ───────────────────────────────────────────────
    show_third = False
    third_label = ""
    third_options = [""]

    if st.session_state.category == "Metals" and st.session_state.get("level2_Metals"):
        show_third = True
        third_label = "Alloy / Grade"
        third_options = get_alloy_options(st.session_state["level2_Metals"])

    elif st.session_state.category == "Plastics" and st.session_state.get("level2_Plastics"):
        show_third = True
        third_label = "Material / Grade"
        third_options = [""] + get_plastic_grade_options(st.session_state["level2_Plastics"])

    elif st.session_state.category in ("Phenolics", "Electrical Cable"):
        show_third = False

    if show_third:
        st.divider()
        st.subheader(third_label)

        widget_key = f"third_{st.session_state.category.replace(' ', '_')}"



        selected_third = st.selectbox(
            third_label,
            options=third_options,
            #index=0,                            # we want blank
            label_visibility="collapsed",
            key=widget_key
        )       
    
    
    #st.write(f"DEBUG: alloy value just after selectbox = '{st.session_state.get('third_Metals', 'NOT SET')}'")
    
    
    
    # ───────────────────────────────────────────────
    # Electrical Cable specific fields – only after cable type selected
    # ───────────────────────────────────────────────
    show_cable_details = False

    if st.session_state.category == "Electrical Cable" and st.session_state.get("level2_Electrical_Cable"):
        show_cable_details = True


    if show_cable_details:
        st.divider()
        st.subheader("Cable Specifications")

        cable_type = st.session_state.get("level2_Electrical_Cable", "")

        # ───────────────────────────────────────────────
        # Fields specific to each cable type
        # ───────────────────────────────────────────────
        required_filled = False

        if "Single-Conductor" in cable_type:
            col1, col2, col3 = st.columns(3)

            with col1:
                slash_sheet = st.text_input(
                    "Slash Sheet Number",
                    value=st.session_state.get("cable_slash", ""),
                    key="cable_slash",
                    placeholder="e.g. AS22759/[Slash Sheet Number]"
                )

            with col2:
                awg_size = st.text_input(
                    "AWG / Size",
                    value=st.session_state.get("cable_awg_size", ""),
                    key="cable_awg_size",
                    placeholder="e.g. 20"
                )

            with col3:
                color_code = st.text_input(
                    "Color Code(from AS22759)",
                    value=st.session_state.get("cable_color", ""),
                    key="cable_color",
                    placeholder="e.g. 0=Black.....9=White"
                )

            required_filled = bool(slash_sheet.strip())

        elif "Multi-Conductor" in cable_type:
            config_code = st.text_input(
                "Configuration Code",
                value=st.session_state.get("cable_config", ""),
                key="cable_config",
                placeholder="e.g. WC27500-[Configuration Code]"
            )

            required_filled = bool(config_code.strip())

        elif "Coaxial" in cable_type:
            slash_sheet = st.text_input(
                "Slash Sheet Number",
                value=st.session_state.get("cable_slash", ""),
                key="cable_slash",
                placeholder="e.g. M17/[Slash Sheet Number]"
            )

            required_filled = bool(slash_sheet.strip())

        else:
            st.warning("Please select a valid cable type.")
            required_filled = False

        # ───────────────────────────────────────────────
        # Common: Spool? dropdown (shown for all types)
        # ───────────────────────────────────────────────
        spool_options = ["No", "Yes"]
        spool_choice = st.selectbox(
            "Spool?",
            options=spool_options,
            index=spool_options.index(st.session_state.get("cable_spool", "No"))
                if st.session_state.get("cable_spool", "No") in spool_options else 0,
            key="cable_spool",
            label_visibility="visible"
        )

        # Length – only if Yes
        length = ""
        if spool_choice == "Yes":
            length = st.text_input(
                "Length of Spool",
                value=st.session_state.get("cable_length", ""),
                key="cable_length",
                placeholder="e.g. 1000 ft or 500 m"
            )

        # ───────────────────────────────────────────────
        # Generate button – enabled when required field(s) are filled
        # ───────────────────────────────────────────────
        if required_filled:
            if st.button("Generate Part Number", type="primary", use_container_width=True):
                pn = build_part_number(st.session_state)
                st.session_state.generated_pn = pn

        if "generated_pn" in st.session_state:
            pn = st.session_state.generated_pn

            #st.subheader("Generated Part Number")
            st.markdown(
                """
                <style>
                    /* Tighten spacing just for this PN output area */
                    .pn-container {
                        margin-top: 0.0rem !important;      /* less space above the box */
                        margin-bottom: 1rem !important;
                    }
                    .pn-box {
                        font-size: 1.8rem;
                        font-weight: bold;
                        font-family: 'Consolas', 'Courier New', monospace;
                        background-color: #1f2a44;
                        padding: 0.8rem 1.2rem !important;   /* reduced top/bottom padding */
                        border-radius: 0.5rem;
                        border: 1px solid #3b4a6b;
                        color: #e6edf3;
                        white-space: pre-wrap;
                        word-break: break-all;
                        line-height: 1.3;                     /* tighter line height if multi-line */
                    }
                    /* Reduce default margin below subheader when followed by PN */
                    .stSubheader + .pn-container {
                        margin-top: -0.5rem !important;       /* pull box closer to subheader */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="pn-container"><div class="pn-box">{pn}</div></div>',
                unsafe_allow_html=True
            )

                                        
        
    # ───────────────────────────────────────────────
    # 4. Fourth level – Condition / Temper (only for Metals)
    # ───────────────────────────────────────────────
    show_fourth = False
    fourth_label = ""
    fourth_options = [""]

    if st.session_state.category == "Metals":
        material    = st.session_state.get("level2_Metals", "")
        alloy       = st.session_state.get("third_Metals", "")
        
        if material and alloy:
            show_fourth = True
            fourth_label = "Condition / Temper"
            fourth_options = [""] + get_metal_temper_options(material, alloy)
    
    
    #st.write(f"Debug: material = '{material}', alloy = '{alloy}', show_fourth = {show_fourth}")


    if show_fourth:
        st.divider()
        st.subheader(fourth_label)

        widget_key = "fourth_Metals"

        # ─── Insert the initialization here ────────────────────────────────
        temper_key = "level4_Metals"   # or "fourth_Metals" to match your naming

        if temper_key not in st.session_state:
            st.session_state[temper_key] = ""

        # Force reset to blank when upstream (material or alloy) changes
        fresh_key = f"fresh_fourth_Metals_{material}_{alloy}"
        
        if fresh_key not in st.session_state:
            st.session_state[fresh_key] = True
            if widget_key in st.session_state:
                del st.session_state[widget_key]
            # Also reset the stored temper value
            if temper_key in st.session_state:
                st.session_state[temper_key] = ""

        selected_fourth = st.selectbox(
            fourth_label,
            options=fourth_options,
            index=fourth_options.index(st.session_state.get(temper_key, "")),
            label_visibility="collapsed",
            key=widget_key
        )

    # ───────────────────────────────────────────────
    # 4. Fourth level – Variant / Color (only for Plastics)
    # ───────────────────────────────────────────────
    show_variant = False
    variant_options = [""]

    if st.session_state.category == "Plastics":
        grade = st.session_state.get("third_Plastics", "")
        if grade:
            show_variant = True
            variant_options = [""] + get_plastic_variant_options(grade)

    if show_variant:
        st.divider()
        st.subheader("Variant / Color / Fill")
        widget_key = "fourth_Plastics"

        fresh_key = f"fresh_variant_Plastics_{grade}"
        if fresh_key not in st.session_state:
            st.session_state[fresh_key] = True
            if widget_key in st.session_state:
                del st.session_state[widget_key]
            if "variant_Plastics" in st.session_state:
                del st.session_state["variant_Plastics"]

        selected_variant = st.selectbox(
            "Variant / Color / Fill",
            options=variant_options,
            index=variant_options.index(st.session_state.get("variant_Plastics", "")) 
            if st.session_state.get("variant_Plastics", "") 
            in variant_options 
            else 0,
            label_visibility="collapsed",
            key=widget_key
        )

        if "variant_Plastics" not in st.session_state:
            st.session_state.variant_Plastics = ""
        if selected_variant != st.session_state.variant_Plastics:
            st.session_state.variant_Plastics = selected_variant

    # ───────────────────────────────────────────────
    # Form – shared for Metals, Phenolics, Plastics
    # ───────────────────────────────────────────────
    show_form = False
    form_options = [""] + COMMON_FORMS

    if st.session_state.category in ("Metals", "Phenolics", "Plastics"):
        # Determine if upstream selections are complete
        if st.session_state.category == "Metals":
            upstream_complete = bool(
                st.session_state.get("level2_Metals") and
                st.session_state.get("third_Metals") and
                st.session_state.get("fourth_Metals") and
                st.session_state.fourth_Metals != "" # make sure temper isn't just blank
            )
        
        elif st.session_state.category == "Phenolics":
            upstream_complete = bool(st.session_state.get("level2_Phenolics"))
        
        elif st.session_state.category == "Plastics":
            upstream_complete = bool(
                st.session_state.get("level2_Plastics") and
                st.session_state.get("third_Plastics") and
                st.session_state.get("variant_Plastics") and
                st.session_state.variant_Plastics != "" #make sure variant isn't just blank
            )

        if upstream_complete:
            show_form = True

    if show_form:
        st.divider()
        st.subheader("Form")

        widget_key = f"form_{st.session_state.category.replace(' ', '_')}"

        # ─── Initialize form key only when we are actually showing the widget ───
        if "form" not in st.session_state:
            st.session_state.form = ""

        # Reset when upstream changes (similar pattern you already use)
        fresh_key = f"fresh_form_{st.session_state.category}_{st.session_state.get('level2_' + st.session_state.category, '')}"
        if fresh_key not in st.session_state:
            st.session_state[fresh_key] = True
            if widget_key in st.session_state:
                del st.session_state[widget_key]
            st.session_state.form = ""  # reset

        selected_form = st.selectbox(
            "Form",
            options=form_options,
            index=form_options.index(st.session_state.form) if st.session_state.form in form_options else 0,
            label_visibility="collapsed",
            key=widget_key
        )

        if selected_form != st.session_state.form:
            st.session_state.form = selected_form


        #───────────────────────────────────────────────────────────────────────────
        # ─── Dimension inputs – only when Form is selected ────────────────────────
        #───────────────────────────────────────────────────────────────────────────
        if st.session_state.form and st.session_state.form != "":

            # Raw input strings (what user types)
            if "dim_thickness" not in st.session_state:
                st.session_state.dim_thickness = ""
            if "dim_width" not in st.session_state:
                st.session_state.dim_width = ""
            if "dim_diameter" not in st.session_state:
                st.session_state.dim_diameter = ""
            if "dim_wall_thickness" not in st.session_state:
                st.session_state.dim_wall_thickness = ""
            if "dim_od" not in st.session_state:
                st.session_state.dim_od = ""

            # Confirmation flag – starts False every time Form changes
            if "dimensions_confirmed" not in st.session_state:
                st.session_state.dimensions_confirmed = False

            # Parsed numbers – only set after successful confirmation
            if "parsed_thickness" not in st.session_state:
                st.session_state.parsed_thickness = None
            if "parsed_width" not in st.session_state:
                st.session_state.parsed_width = None
            # ... same for diameter, wall, od if needed

            st.divider()
            st.subheader("Dimensions")

            form = st.session_state.form

            if form == "Sheet (thickness <= 0.25\")":
                col1, col2 = st.columns(2)
                with col1:
                    thickness = st.text_input(
                        "Thickness (inches)",
                        value=st.session_state.dim_thickness,
                        key="dim_thickness_input",
                        placeholder="e.g. 0.250"
                    )
                with col2:
                    width = st.text_input(
                        "Width (inches)",
                        value=st.session_state.dim_width,
                        key="dim_width_input",
                        placeholder="e.g. 48"
                    )

                # Store raw values
                st.session_state.dim_thickness = thickness
                st.session_state.dim_width = width

            elif form == "Plate/Bar (thickness > 0.25\")":
                col1, col2 = st.columns(2)
                with col1:
                    thickness = st.text_input(
                        "Thickness (inches)",
                        value=st.session_state.dim_thickness,
                        key="dim_thickness_input_plate",
                        placeholder="e.g. 0.250"
                    )
                with col2:
                    width = st.text_input(
                        "Width (inches)",
                        value=st.session_state.dim_width,
                        key="dim_width_input_plate",
                        placeholder="e.g. 12"
                    )

                st.session_state.dim_thickness = thickness
                st.session_state.dim_width = width

            elif form == "Rod":
                diameter = st.text_input(
                    "Diameter (inches)",
                    value=st.session_state.dim_diameter,
                    key="dim_diameter_input",
                    placeholder="e.g. 1.0"
                )
                st.session_state.dim_diameter = diameter

            elif form == "Tube":
                col1, col2 = st.columns(2)
                with col1:
                    wall = st.text_input(
                        "Wall Thickness (inches)",
                        value=st.session_state.dim_wall_thickness,
                        key="dim_wall_input",
                        placeholder="e.g. 0.065"
                    )
                with col2:
                    od = st.text_input(
                        "Outer Diameter (inches)",
                        value=st.session_state.dim_od,
                        key="dim_od_input",
                        placeholder="e.g. 1.0"
                    )

                st.session_state.dim_wall_thickness = wall
                st.session_state.dim_od = od

            else:
                st.info("No dimensions required for this form.", icon="ℹ️")

            if st.button("Confirm Dimensions", type="primary", use_container_width=True):

                # Reset confirmation status first
                st.session_state.dimensions_confirmed = False
                st.session_state.parsed_thickness = None
                # ... reset other parsed values if you add them

                try:
                    if form in ["Sheet (thickness <= 0.25\")", "Plate/Bar (thickness > 0.25\")"]:
                        thick_str = st.session_state.dim_thickness.strip()
                        width_str = st.session_state.dim_width.strip()

                        if not thick_str or not width_str:
                            st.error("Both thickness and width are required.")
                            st.stop()

                        thickness_val = float(thick_str)
                        width_val = float(width_str)

                        if thickness_val <= 0:
                            st.error("Thickness must be greater than 0.")
                            st.stop()

                        # Form-specific thickness check
                        if form == "Sheet (thickness <= 0.25\")" and thickness_val > 0.25:
                            st.error("Sheet thickness must be ≤ 0.25 inches.")
                            st.stop()
                        elif form == "Plate/Bar (thickness > 0.25\")" and thickness_val <= 0.25:
                            st.error("Plate/Bar thickness must be > 0.25 inches.")
                            st.stop()

                        # Store parsed values
                        st.session_state.parsed_thickness = thickness_val
                        st.session_state.parsed_width = width_val
                        st.session_state.dimensions_confirmed = True
                        st.success("Dimensions confirmed!")

                    elif form == "Rod":
                        dia_str = st.session_state.dim_diameter.strip()
                        if not dia_str:
                            st.error("Diameter is required.")
                            st.stop()
                        dia_val = float(dia_str)
                        if dia_val <= 0:
                            st.error("Diameter must be greater than 0.")
                            st.stop()
                        st.session_state.parsed_diameter = dia_val
                        st.session_state.dimensions_confirmed = True
                        st.success("Dimensions confirmed!")

                    elif form == "Tube":
                        wall_str = st.session_state.dim_wall_thickness.strip()
                        od_str = st.session_state.dim_od.strip()

                        if not wall_str or not od_str:
                            st.error("Both wall thickness and OD are required.")
                            st.stop()

                        wall_val = float(wall_str)
                        od_val = float(od_str)

                        if wall_val <= 0 or od_val <= 0:
                            st.error("Wall thickness and OD must be greater than 0.")
                            st.stop()

                        st.session_state.parsed_wall = wall_val
                        st.session_state.parsed_od = od_val
                        st.session_state.dimensions_confirmed = True
                        st.success("Dimensions confirmed!")

                except ValueError:
                    st.error("All inputs must be valid numbers (e.g. 0.250, 1.0, 48).")


                # ─── Generate button – only show when confirmed ────────────────────────
            if st.session_state.dimensions_confirmed:
                if st.button(
                    "Generate Part Number", 
                    type="primary", 
                    use_container_width=True,
                    key="generate_part_number_btn"
                ):
                    pn = build_part_number(st.session_state)
                    st.session_state.generated_pn = pn
                

                if "generated_pn" in st.session_state:
                    pn = st.session_state.generated_pn

                    #st.subheader("Generated Part Number")
                    st.markdown(
                        """
                        <style>
                            /* Tighten spacing just for this PN output area */
                            .pn-container {
                                margin-top: 0.0rem !important;      /* less space above the box */
                                margin-bottom: 1rem !important;
                            }
                            .pn-box {
                                font-size: 1.8rem;
                                font-weight: bold;
                                font-family: 'Consolas', 'Courier New', monospace;
                                background-color: #1f2a44;
                                padding: 0.8rem 1.2rem !important;   /* reduced top/bottom padding */
                                border-radius: 0.5rem;
                                border: 1px solid #3b4a6b;
                                color: #e6edf3;
                                white-space: pre-wrap;
                                word-break: break-all;
                                line-height: 1.3;                     /* tighter line height if multi-line */
                            }
                            /* Reduce default margin below subheader when followed by PN */
                            .stSubheader + .pn-container {
                                margin-top: -0.5rem !important;       /* pull box closer to subheader */
                            }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="pn-container"><div class="pn-box">{pn}</div></div>',
                        unsafe_allow_html=True
                    )


                                        
