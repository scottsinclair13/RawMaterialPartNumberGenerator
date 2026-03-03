import streamlit as st
from dataclasses import dataclass
from typing import Dict, List


# =============================================================================
# DATA + LOGIC (mirrors RM_PN_generator.py)
# =============================================================================

@dataclass(frozen=True)
class Choice:
    label: str
    code: str


@dataclass(frozen=True)
class MetalSpec:
    material: Choice
    alloys_to_conditions: Dict[str, List[str]]


@dataclass(frozen=True)
class PlasticFamily:
    material: Choice
    grades: Dict[str, List[str]]


@dataclass
class BuildResult:
    pn: str
    uom: str
    warnings: List[str]


ABBREV_MAP: Dict[str, str] = {
    # Metal conditions
    "Annealed": "ANN",
    "Normalized": "NORM",
    "Q&T": "QT",
    "STA": "STA",
    "Condition B": "B",
    "1/4 hard": "1/4H",
    "1/2 hard": "1/2H",
    "3/4 hard": "3/4H",
    "Full hard": "FH",

    # Colors
    "Black": "BLK",
    "Natural": "NAT",
    "Blue": "BLU",
    "Grey": "GRY",

    # Alloys/Grades
    "6Al-4V": "GR5",
    "6Al-4V ELI": "GR23",
    "6Al-2Sn-4Zr-2Mo": "6242",
    "17-4PH": "174PH",
    "Generic(Acetal)": "ACET",
    "Delrin 150": "DEL",
    "Delrin AF": "DEL",
    "Glass-filled": "GF",
    "Oil-filled": "OF",
    "MDS-filled": "MDS",
    "Tivar-1000": "T1000",
    "Tivar-88": "T88",
    "Nylon 6": "PA6",
    "Nylon 6/6": "PA66",
    "10%": "10",
    "20%": "20",
    "30%": "30",
}


def pn_token(label: str) -> str:
    if not label:
        return ""
    if label in ABBREV_MAP:
        return ABBREV_MAP[label]
    return (
        label.strip()
        .upper()
        .replace(" ", "")
        .replace("/", "-")
        .replace("\\", "-")
    )


FORM_ABBREVIATIONS = {
    "Sheet (thickness <= 0.25\")": "SHT",
    "Plate/Bar (thickness > 0.25\")": "BAR",
    "Rod": "ROD",
    "Tube": "TUBE",
    "INSULATED": "INS",
    "SHIELDED": "SHLD",
    "50OHM": "50OHM",
    "ARM": "ARM",
}

COMMON_FORMS = [
    "Sheet (thickness <= 0.25\")",
    "Plate/Bar (thickness > 0.25\")",
    "Rod",
    "Tube",
    "Other",
]

CABLE_FORMS = ["INSULATED", "SHIELDED", "50OHM", "ARM", "Other"]

COMMON_PROCSPECS = {
    "Aluminum": {
        "2024": ["AMS4037", "AMS4120", "ASTM B209", "QQ A-250/4"],
        "6061": ["AMS4027", "AMS4117", "ASTM B209", "ASTM B221"],
        "7075": ["AMS4045", "AMS4078", "QQ A-250/12"],
        "7050": ["AMS4050", "AMS4201"],
    },
    "Titanium": {
        "6Al-4V": ["AMS4928", "AMS4965"],
        "6Al-4V ELI": ["AMS4907", "AMS4930"],
        "6Al-2Sn-4Zr-2Mo": ["AMS4919", "MIL-T-9046"],
    },
    "Stainless Steel": {
        "304": ["AMS5639"],
        "316": ["AMS5648"],
        "17-4PH": ["AMS5643"],
    },
    "Steel": {
        "4340": ["AMS6415", "AMS6526"],
        "300M": ["AMS6417", "AMS6419"],
        "Aermet 100": ["AMS6532", "AMS6478"],
    },
    "Copper": {
        "C10100": ["AMS4700", "ASTM B152"],
        "C17200": ["AMS4650", "AMS4530"],
    },
    "Phenolic": {
        "Linen Electrical": ["MIL-I-24768/13"],
        "G3 Glass": ["MIL-I-24768/18"],
        "G5 Melamine": ["MIL-I-24768/8"],
        "G7 Silicone": ["MIL-I-24768/17"],
        "Canvas Electrical": ["MIL-I-24768/14"],
    },
    "Single-Conductor Wire": ["MIL-W-22759", "AS22759"],
    "Multi-Conductor Cable": ["MIL-DTL-27500", "AS50881"],
    "Coaxial Cable": ["MIL-C-17", "MIL-DTL-17"],
    "Specialty Cable": ["MIL-PRF-49291", "AS8041"],
}

METALS: List[MetalSpec] = [
    MetalSpec(Choice("Aluminum", "AL"), {
        "2024": ["T3", "T351", "T4"],
        "6061": ["T6", "T651"],
        "7075": ["T6", "T651", "T73", "T7351"],
        "7050": ["T7451", "T76"],
    }),
    MetalSpec(Choice("Titanium", "TI"), {
        "6Al-4V": ["Annealed", "STA"],
        "6Al-4V ELI": ["Annealed"],
        "6Al-2Sn-4Zr-2Mo": ["Annealed", "STA"],
    }),
    MetalSpec(Choice("Stainless Steel", "SS"), {
        "304": ["Annealed", "1/8 hard", "1/4 hard", "1/2 hard", "3/4 hard", "Full hard"],
        "316": ["Annealed", "Condition B"],
        "17-4PH": ["Annealed", "H900", "H1025"],
    }),
    MetalSpec(Choice("Steel", "ST"), {
        "4340": ["Normalized", "Q&T"],
        "300M": ["Q&T"],
        "Aermet 100": ["Q&T"],
    }),
    MetalSpec(Choice("Copper", "CU"), {
        "C10100": ["Annealed", "H02"],
        "C17200": ["TB00", "TF00"],
    }),
]

PHENOLICS: List[Choice] = [
    Choice("Linen Electrical", "LE"),
    Choice("G3 Glass", "G3"),
    Choice("G5 Melamine", "G5"),
    Choice("G7 Silicone", "G7"),
    Choice("Canvas Electrical", "CE"),
    Choice("Other", "OT"),
]

PLASTICS: List[PlasticFamily] = [
    PlasticFamily(Choice("HDPE", "HDPE"), {
        "PE300": ["Black", "Natural"],
        "PE500": ["Black", "Natural"],
        "Other": [],
    }),
    PlasticFamily(Choice("UHMW", "UHMW"), {
        "PE1000": ["Black", "Natural"],
        "Tivar-1000": ["Black", "Natural"],
        "Tivar-88": ["Black", "Natural"],
        "Other": [],
    }),
    PlasticFamily(Choice("Polycarbonate", "PC"), {
        "Lexan": ["9034", "XL10", "MR10", "MP"],
        "Glass-filled": ["10%", "20%", "30%"],
        "Other": [],
    }),
    PlasticFamily(Choice("Acetal Resin", "AR"), {
        "Generic(Acetal)": ["Black", "Natural"],
        "Delrin 150": ["Black", "Natural"],
        "Delrin AF": ["100AF", "500AF", "DE588AF"],
        "Other": [],
    }),
    PlasticFamily(Choice("Nylon", "NYL"), {
        "Nylon 6": ["Natural", "Glass-filled", "Oil-filled"],
        "Nylon 6/6": ["Natural", "Glass-filled", "MDS-filled"],
        "Other": [],
    }),
]

CABLES: List[Choice] = [
    Choice("Single-Conductor Wire", "WC"),
    Choice("Multi-Conductor Cable", "MC"),
    Choice("Coaxial Cable", "CX"),
    Choice("Specialty Cable", "SC"),
]


def normalize_form_code(form_label: str) -> str:
    return FORM_ABBREVIATIONS.get(form_label, pn_token(form_label)[:8])


def infer_needed_dimension_keys(category: str, form_label: str) -> List[str]:
    f = (form_label or "").lower()
    if category in ("Metals", "Phenolics", "Plastics"):
        if any(w in f for w in ("sheet", "plate", "bar")):
            return ["thick", "width"]
        if "rod" in f:
            return ["dia"]
        if "tube" in f:
            return ["od", "wall"]
        return []
    if category == "Electrical Cable":
        return ["gauge"]
    return []


def dims_to_string(category: str, form_label: str, dims: Dict[str, str]) -> str:
    f = (form_label or "").lower()
    if category in ("Metals", "Phenolics", "Plastics"):
        if any(w in f for w in ("sheet", "plate", "bar")):
            return f"T{dims['thick']}-W{dims['width']}"
        if "rod" in f:
            return f"D{dims['dia']}"
        if "tube" in f:
            return f"OD{dims['od']}-W{dims['wall']}"
    if category == "Electrical Cable":
        return f"AWG{dims['gauge']}"
    return ""


def default_uom(category: str, has_dims: bool) -> str:
    if not has_dims:
        return "EA (each)"
    if category in ("Metals", "Phenolics", "Plastics"):
        return "IN (length)"
    if category == "Electrical Cable":
        return "FT (feet)"
    return "EA (each)"


def build_part_number(sel: Dict[str, object]) -> BuildResult:
    warnings: List[str] = []

    category = str(sel.get("category") or "").strip()
    form = str(sel.get("form") or "").strip()
    if not category or not form:
        raise ValueError("Category and Form are required.")

    form_code = normalize_form_code(form)
    spec = (sel.get("specification") or "").strip()

    parts: List[str] = []

    if category == "Metals":
        mat = (sel.get("material") or "").strip()
        alloy = (sel.get("alloy") or "").strip()
        cond = (sel.get("condition") or "").strip()
        if not mat or not alloy:
            raise ValueError("Metals require material + alloy.")

        abbrev = "XX"
        for m in METALS:
            if m.material.label == mat:
                abbrev = m.material.code
                break

        parts.extend([abbrev, pn_token(alloy)])
        if cond and cond != "None / Not Applicable":
            parts.append(pn_token(cond))
        if spec:
            parts.append(pn_token(spec))
        parts.append(form_code)

    elif category == "Phenolics":
        mat = (sel.get("material") or "").strip()
        if not mat:
            raise ValueError("Phenolics require material.")
        code_map = {c.label: c.code for c in PHENOLICS}
        ph_code = code_map.get(mat, "OT")
        if mat == "Other":
            custom = (sel.get("custom_material_text") or "").strip()
            if custom:
                ph_code = pn_token(custom)[:8]
                warnings.append("Custom phenolic token trimmed for PN readability.")
        parts.append(ph_code)
        if spec:
            parts.append(pn_token(spec))
        parts.append(form_code)

    elif category == "Plastics":
        fam = (sel.get("plastic_family") or "").strip()
        grade = (sel.get("plastic_grade") or "").strip()
        var = (sel.get("plastic_variant") or "").strip()
        if not fam:
            raise ValueError("Plastics require plastic family.")

        fam_code = "PL"
        for p in PLASTICS:
            if p.material.label == fam:
                fam_code = p.material.code
                break

        parts.append(fam_code)
        if grade and grade != "None / Not Applicable":
            if grade == "Other":
                cg = (sel.get("custom_grade_text") or "").strip()
                if cg:
                    parts.append(pn_token(cg)[:10])
            else:
                parts.append(pn_token(grade)[:10])
        if var and var != "None / Not Applicable":
            parts.append(pn_token(var)[:10])
        if spec:
            parts.append(pn_token(spec))
        parts.append(form_code)

    elif category == "Electrical Cable":
        mat = (sel.get("material") or "").strip()
        if not mat:
            raise ValueError("Electrical Cable requires cable type.")
        code_map = {c.label: c.code for c in CABLES}
        cable_code = code_map.get(mat, "CB")
        construction = (sel.get("cable_construction") or "").strip()

        parts.append(cable_code)
        if construction:
            parts.append(pn_token(construction)[:12])
        if spec:
            parts.append(pn_token(spec))
        parts.append(form_code)

    else:
        raise ValueError(f"Unknown category: {category}")

    dims = sel.get("dimensions") or {}
    dim_str = ""
    if isinstance(dims, dict) and dims:
        dim_str = dims_to_string(category, form, dims)

    pn = "-".join([p for p in parts if p])
    if dim_str:
        pn = f"{pn}-{dim_str}"

    return BuildResult(pn=pn, uom=default_uom(category, bool(dim_str)), warnings=warnings)


# =============================================================================
# STREAMLIT UI (force Tk look: light fields + dark panels)
# =============================================================================

st.set_page_config(page_title="Raw Material PN Generator", layout="wide")

COL_BG = "#070b12"
COL_PANEL = "#0d1626"
COL_PANEL2 = "#0b1220"
COL_TEXT = "#e6edf3"
COL_MUTED = "#9aa4b2"
COL_ACCENT = "#00d1ff"
COL_FIELD_BG = "#e6e6e6"
COL_FIELD_FG = "#0a0f18"

st.markdown(
    f"""
<style>
/* Global background */
.stApp {{
  background: {COL_BG};
  color: {COL_TEXT};
}}
.block-container {{
  padding-top: 1.1rem;
  max-width: 1500px;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

/* Panels */
.rm-panel {{
  background: {COL_PANEL};
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 18px;
}}
.rm-panel-output {{
  background: {COL_PANEL2};
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 18px;
  min-height: 640px;
}}

/* Typography */
.rm-title {{
  font-size: 40px;
  font-weight: 800;
  margin: 0;
}}
.rm-sub {{
  margin-top: 6px;
  color: {COL_MUTED};
  font-size: 13px;
}}
.rm-section {{
  font-size: 22px;
  font-weight: 800;
  margin: 6px 0 12px 0;
}}
.rm-hr {{
  border: none;
  border-top: 1px solid rgba(255,255,255,0.08);
  margin: 16px 0;
}}

/* Labels */
div[data-testid="stWidgetLabel"] > label {{
  color: {COL_TEXT} !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  margin-bottom: 4px !important;
}}

/* ====== HARD FORCE LIGHT INPUTS (BaseWeb) ====== */
/* Selectbox outer container */
div[data-baseweb="select"] > div {{
  background-color: {COL_FIELD_BG} !important;
  border: 1px solid rgba(0,0,0,0.35) !important;
  border-radius: 8px !important;
}}
/* Selectbox text + placeholder */
div[data-baseweb="select"] span {{
  color: {COL_FIELD_FG} !important;
  font-weight: 600 !important;
}}
/* Selectbox chevron */
div[data-baseweb="select"] svg {{
  fill: {COL_FIELD_FG} !important;
}}

/* Text input */
div[data-testid="stTextInput"] input {{
  background-color: {COL_FIELD_BG} !important;
  color: {COL_FIELD_FG} !important;
  border: 1px solid rgba(0,0,0,0.35) !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
}}

/* Focus outline */
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stTextInput"] input:focus {{
  outline: 2px solid rgba(0, 209, 255, 0.30) !important;
  box-shadow: none !important;
}}

/* Buttons: Tk-like gray bars */
.stButton > button {{
  background: #cfcfcf !important;
  color: {COL_FIELD_FG} !important;
  border: 0 !important;
  border-radius: 8px !important;
  padding: 0.65rem 1.05rem !important;
  font-weight: 800 !important;
}}
.stButton > button:hover {{
  background: #e0e0e0 !important;
}}
.stButton > button:disabled {{
  background: #cfcfcf !important;
  color: #8a8a8a !important;
}}

/* Output typography */
.rm-out {{
  font-family: Consolas, "Courier New", monospace;
  font-size: 16px;
  color: {COL_TEXT};
  line-height: 1.55;
}}
.rm-pn {{
  font-family: Consolas, "Courier New", monospace;
  font-size: 22px;
  font-weight: 900;
  color: {COL_TEXT};
  margin: 10px 0 14px 0;
}}
.rm-muted {{
  color: {COL_MUTED};
}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="rm-title">Raw Material Part Number Generator</div>
<div class="rm-sub">Consistency built-in • Confusion built-out</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# Helpers
def selectbox_empty(label: str, options: List[str], key: str) -> str:
    return st.selectbox(label, options=[""] + options, index=0, key=key)

def is_pos_float(s: str) -> bool:
    try:
        return float(s) > 0
    except Exception:
        return False

def is_pos_int(s: str) -> bool:
    try:
        return int(s) > 0
    except Exception:
        return False


# Session output state
if "generated_pn" not in st.session_state:
    st.session_state.generated_pn = ""
if "generated_uom" not in st.session_state:
    st.session_state.generated_uom = ""
if "generated_warnings" not in st.session_state:
    st.session_state.generated_warnings = []

left, right = st.columns([1.15, 0.9], gap="large")

with left:
    st.markdown('<div class="rm-panel">', unsafe_allow_html=True)
    st.markdown('<div class="rm-section">Inputs</div>', unsafe_allow_html=True)

    selections: Dict[str, object] = {}

    category = selectbox_empty("1) Category", ["Metals", "Phenolics", "Plastics", "Electrical Cable"], "category")
    if category:
        selections["category"] = category

    if category == "Metals":
        mat = selectbox_empty("2) Metal Material", [m.material.label for m in METALS] + ["Other"], "metal_material")
        if mat:
            selections["material"] = mat if mat != "Other" else (st.text_input("Custom metal material name", "", key="metal_material_custom").strip() or "Other")

            alloys = []
            for m in METALS:
                if m.material.label == mat:
                    alloys = list(m.alloys_to_conditions.keys())
                    break

            alloy = selectbox_empty("3) Alloy / Grade", alloys + ["Other"], "metal_alloy")
            if alloy:
                selections["alloy"] = alloy if alloy != "Other" else (st.text_input("Custom alloy / grade", "", key="metal_alloy_custom").strip() or "Other")

                conds = []
                for m in METALS:
                    if m.material.label == mat:
                        conds = m.alloys_to_conditions.get(alloy, [])
                        break

                cond = selectbox_empty("4) Condition / Temper (optional)", ["None / Not Applicable"] + conds + ["Other"], "metal_condition")
                if cond and cond not in ("None / Not Applicable", ""):
                    if cond == "Other":
                        cc = st.text_input("Custom condition/temper", "", key="metal_condition_custom").strip()
                        if cc:
                            selections["condition"] = cc
                    else:
                        selections["condition"] = cond

                spec_opts = []
                d = COMMON_PROCSPECS.get(mat, {})
                if isinstance(d, dict):
                    spec_opts = d.get(alloy, [])
                spec = selectbox_empty("(Optional) Material Specification", ["None / Not Applicable"] + spec_opts + ["Other"], "spec")
                if spec and spec not in ("None / Not Applicable", ""):
                    if spec == "Other":
                        cs = st.text_input("Custom spec (AMS/ASTM/MIL/etc)", "", key="spec_custom").strip()
                        if cs:
                            selections["specification"] = cs
                    else:
                        selections["specification"] = spec

                form = selectbox_empty("Form", COMMON_FORMS, "form")
                if form:
                    selections["form"] = form if form != "Other" else (st.text_input("Custom form", "", key="form_custom").strip() or "Other")

    elif category == "Phenolics":
        mat = selectbox_empty("2) Phenolic Type", [p.label for p in PHENOLICS], "phen_material")
        if mat:
            selections["material"] = mat
            if mat == "Other":
                c = st.text_input("Custom phenolic name/type", "", key="phen_custom").strip()
                if c:
                    selections["custom_material_text"] = c

            phen_map = COMMON_PROCSPECS.get("Phenolic", {})
            spec_opts = phen_map.get(mat, []) if isinstance(phen_map, dict) else []
            spec = selectbox_empty("(Optional) Material Specification", ["None / Not Applicable"] + spec_opts + ["Other"], "spec")
            if spec and spec not in ("None / Not Applicable", ""):
                if spec == "Other":
                    cs = st.text_input("Custom spec (AMS/ASTM/MIL/etc)", "", key="spec_custom").strip()
                    if cs:
                        selections["specification"] = cs
                else:
                    selections["specification"] = spec

            form = selectbox_empty("Form", COMMON_FORMS, "form")
            if form:
                selections["form"] = form if form != "Other" else (st.text_input("Custom form", "", key="form_custom").strip() or "Other")

    elif category == "Plastics":
        fam = selectbox_empty("2) Plastic Family", [p.material.label for p in PLASTICS], "plastic_family")
        if fam:
            selections["plastic_family"] = fam
            grades = []
            for p in PLASTICS:
                if p.material.label == fam:
                    grades = list(p.grades.keys())
                    break
            grade = selectbox_empty("3) Grade (optional)", ["None / Not Applicable"] + grades, "plastic_grade")
            if grade and grade != "None / Not Applicable":
                if grade == "Other":
                    cg = st.text_input("Custom grade", "", key="plastic_grade_custom").strip()
                    selections["plastic_grade"] = "Other"
                    if cg:
                        selections["custom_grade_text"] = cg
                else:
                    selections["plastic_grade"] = grade

            variants = []
            if grade and grade not in ("None / Not Applicable", ""):
                for p in PLASTICS:
                    if p.material.label == fam:
                        variants = p.grades.get(grade, [])
                        break
            var = selectbox_empty("4) Variant / Color (optional)", ["None / Not Applicable"] + variants, "plastic_variant")
            if var and var != "None / Not Applicable":
                selections["plastic_variant"] = var

            spec = selectbox_empty("(Optional) Material Specification", ["None / Not Applicable", "Other"], "spec")
            if spec == "Other":
                cs = st.text_input("Custom spec (AMS/ASTM/MIL/etc)", "", key="spec_custom").strip()
                if cs:
                    selections["specification"] = cs

            form = selectbox_empty("Form", COMMON_FORMS, "form")
            if form:
                selections["form"] = form if form != "Other" else (st.text_input("Custom form", "", key="form_custom").strip() or "Other")

    elif category == "Electrical Cable":
        mat = selectbox_empty("2) Cable Type", [c.label for c in CABLES], "cable_type")
        if mat:
            selections["material"] = mat
            cc = st.text_input("3) Construction / Jacket (optional)", "", key="cable_construction").strip()
            if cc:
                selections["cable_construction"] = cc

            spec_opts = COMMON_PROCSPECS.get(mat, [])
            spec_list = spec_opts if isinstance(spec_opts, list) else []
            spec = selectbox_empty("(Optional) Material Specification", ["None / Not Applicable"] + spec_list + ["Other"], "spec")
            if spec and spec not in ("None / Not Applicable", ""):
                if spec == "Other":
                    cs = st.text_input("Custom spec (AMS/ASTM/MIL/etc)", "", key="spec_custom").strip()
                    if cs:
                        selections["specification"] = cs
                else:
                    selections["specification"] = spec

            form = selectbox_empty("Form", CABLE_FORMS, "form")
            if form:
                selections["form"] = form if form != "Other" else (st.text_input("Custom form", "", key="form_custom").strip() or "Other")

    # Dimensions
    if selections.get("category") and selections.get("form"):
        needed = infer_needed_dimension_keys(selections["category"], selections["form"])
        if needed:
            st.markdown('<hr class="rm-hr"/>', unsafe_allow_html=True)
            st.markdown('<div class="rm-section" style="font-size:18px;">Dimensions</div>', unsafe_allow_html=True)
            dims: Dict[str, str] = {}

            if needed == ["thick", "width"]:
                t = st.text_input("Thickness (in)", "", key="dim_thick")
                w = st.text_input("Width (in)", "", key="dim_width")
                if t and w and is_pos_float(t) and is_pos_float(w):
                    dims["thick"] = t.strip()
                    dims["width"] = w.strip()
            elif needed == ["dia"]:
                d = st.text_input("Diameter (in)", "", key="dim_dia")
                if d and is_pos_float(d):
                    dims["dia"] = d.strip()
            elif needed == ["od", "wall"]:
                od = st.text_input("OD (in)", "", key="dim_od")
                wall = st.text_input("Wall (in)", "", key="dim_wall")
                if od and wall and is_pos_float(od) and is_pos_float(wall):
                    dims["od"] = od.strip()
                    dims["wall"] = wall.strip()
            elif needed == ["gauge"]:
                g = st.text_input("Wire Gauge (AWG)", "", key="dim_gauge")
                if g and is_pos_int(g):
                    dims["gauge"] = g.strip()

            if dims:
                selections["dimensions"] = dims

    st.markdown('<hr class="rm-hr"/>', unsafe_allow_html=True)
    can_generate = bool(selections.get("category")) and bool(selections.get("form"))

    if st.button("Generate Part Number", use_container_width=True, disabled=not can_generate):
        try:
            needed = infer_needed_dimension_keys(selections["category"], selections["form"])
            if needed and "dimensions" not in selections:
                raise ValueError("Dimensions are required and must be valid positive numbers (AWG must be positive integer).")
            res = build_part_number(selections)
            st.session_state.generated_pn = res.pn
            st.session_state.generated_uom = res.uom
            st.session_state.generated_warnings = res.warnings
        except Exception as e:
            st.session_state.generated_pn = ""
            st.session_state.generated_uom = ""
            st.session_state.generated_warnings = []
            st.error(str(e))

    with st.expander("Debug: selections"):
        st.json(selections)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="rm-panel-output">', unsafe_allow_html=True)
    st.markdown('<div class="rm-section">Output</div>', unsafe_allow_html=True)

    pn = st.session_state.get("generated_pn", "")
    uom = st.session_state.get("generated_uom", "")
    warns = st.session_state.get("generated_warnings", [])

    if not pn:
        st.markdown('<div class="rm-out">Select options on the left.<br><br>Generated PN will appear here.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="rm-out">Generated Part Number:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rm-pn">{pn}</div>', unsafe_allow_html=True)
        st.markdown('<div class="rm-out">Default UOM:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rm-out">{uom}</div>', unsafe_allow_html=True)

        if warns:
            st.markdown('<hr class="rm-hr"/>', unsafe_allow_html=True)
            st.markdown('<div class="rm-out">Warnings:</div>', unsafe_allow_html=True)
            for w in warns:
                st.markdown(f'<div class="rm-muted">- {w}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
