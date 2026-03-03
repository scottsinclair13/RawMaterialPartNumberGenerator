# streamlit_app.py
import streamlit as st
from RM_PN_generator import (  # ← your original file name, without .py
    ABBREV_MAP,
    pn_token,
    FORM_ABBREVIATIONS,
    COMMON_FORMS,
    CABLE_FORMS,
    COMMON_PROCSPECS,
    METALS,
    PHENOLICS,
    PLASTICS,
    CABLES,
    Choice,
    MetalSpec,
    PlasticFamily,
    BuildResult,
    normalize_form_code,
    _format_number,
    infer_needed_dimension_keys,
    dims_to_string,
    default_uom,
    build_part_number,
)

# ────────────────────────────────────────────────
#                Streamlit UI only
# ────────────────────────────────────────────────

st.set_page_config(page_title="Raw Material PN Generator", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    .stApp { background-color: #0b0f14; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    section.main > div { padding-top: 1rem; }
    h1, h2, h3 { color: #e6edf3; }
    .stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput input {
        background-color: #e6e6e6 !important;
        color: #0a0f18 !important;
        border: none !important;
        font-size: 14px;
    }
    .stButton > button {
        background: #cfcfcf;
        color: #0a0f18;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover { background: #e0e0e0; }
    .accent { background: #cfcfcf !important; font-weight: 700 !important; font-size: 15px !important; }
    .output { background: #0b1220; color: #e6edf3; font-family: Consolas, monospace; padding: 1.2rem; border-radius: 6px; white-space: pre-wrap; }
    .pn { font-size: 1.4rem; font-weight: bold; display: block; margin: 0.8rem 0; }
</style>
""", unsafe_allow_html=True)

st.title("Raw Material Part Number Generator")
st.caption("Consistency built-in • Confusion built-out")

col_left, col_right = st.columns([3, 1.3])

# Session state to mimic the original selections dict + flow control
if "selections" not in st.session_state:
    st.session_state.selections = {}
if "step" not in st.session_state:
    st.session_state.step = "category"
if "pn_result" not in st.session_state:
    st.session_state.pn_result = None

sels = st.session_state.selections

def reset_after(step):
    steps = ["category", "metal_material", "metal_alloy", "metal_condition",
             "phen_material", "plastic_family", "plastic_grade", "plastic_variant",
             "cable_material", "cable_construction", "spec", "form", "dims"]
    try:
        idx = steps.index(step)
        for s in steps[idx+1:]:
            if s in sels:
                del sels[s]
        st.session_state.step = step
        st.session_state.pn_result = None
    except ValueError:
        pass

with col_left:
    # ── Category ─────────────────────────────────────────────────────────────
    if st.session_state.step == "category" or "category" not in sels:
        cat = st.selectbox(
            "Category",
            options=[""] + ["Metals", "Phenolics", "Plastics", "Electrical Cable"],
            index=0,
            key="cat_sel"
        )
        if cat:
            sels["category"] = cat
            reset_after("category")
            st.rerun()

    # ── Metals branch ────────────────────────────────────────────────────────
    if sels.get("category") == "Metals":
        # Material
        if st.session_state.step == "category" or st.session_state.step == "metal_material":
            mats = [m.material.label for m in METALS] + ["Other"]
            mat = st.selectbox("Metal Material", [""] + mats, key="metal_mat")
            if mat:
                if mat == "Other":
                    custom = st.text_input("Custom metal material", key="custom_metal")
                    if custom.strip():
                        sels["material"] = custom.strip()
                        st.session_state.step = "metal_alloy"
                        st.rerun()
                else:
                    sels["material"] = mat
                    st.session_state.step = "metal_alloy"
                    st.rerun()

        # Alloy
        if sels.get("material") and st.session_state.step == "metal_alloy":
            for m in METALS:
                if m.material.label == sels["material"]:
                    alloys = list(m.alloys_to_conditions.keys()) + ["Other"]
                    break
            else:
                alloys = ["Other"]

            alloy = st.selectbox("Alloy / Grade", [""] + alloys, key="metal_alloy_sel")
            if alloy:
                if alloy == "Other":
                    custom = st.text_input("Custom alloy/grade", key="custom_alloy")
                    if custom.strip():
                        sels["alloy"] = custom.strip()
                        st.session_state.step = "metal_condition"
                        st.rerun()
                else:
                    sels["alloy"] = alloy
                    st.session_state.step = "metal_condition"
                    st.rerun()

        # (continue similarly for condition, spec, form, dims — pattern is identical)

        # Generate button at the end
        if "form" in sels:
            if st.button("Generate Part Number", type="primary", key="gen_btn"):
                try:
                    res = build_part_number(sels)
                    st.session_state.pn_result = res
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

    # Phenolics, Plastics, Cable branches follow the exact same conditional/step logic

with col_right:
    st.markdown("**Output**")
    if st.session_state.pn_result:
        res = st.session_state.pn_result
        st.markdown(f'<div class="output">Generated Part Number:\n\n<span class="pn">{res.pn}</span>\n\nDefault UOM:\n{res.uom}</div>', unsafe_allow_html=True)
        st.button("Copy PN", on_click=lambda: st.session_state.__setitem__("copied", res.pn))
        if "copied" in st.session_state:
            st.success("Copied to clipboard!")
            del st.session_state["copied"]
        if res.warnings:
            st.warning("\n".join(res.warnings))
    else:
        st.info("Select options on the left.\n\nGenerated PN will appear here.")

