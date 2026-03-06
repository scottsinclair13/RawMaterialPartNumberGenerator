# data.py
"""
Central place for all raw material classification data:
categories, materials, alloys, grades, forms, abbreviations, etc.
"""

from typing import Dict, List, Optional, Union

# ───────────────────────────────────────────────
# Forms
# ───────────────────────────────────────────────
COMMON_FORMS = [
    "Sheet (thickness <= 0.25\")",
    "Plate/Bar (thickness > 0.25\")",
    "Rod",
    "Tube",
]

FORM_ABBREVIATIONS = {
    "Sheet (thickness <= 0.25\")": "SHT",
    "Plate/Bar (thickness > 0.25\")": "BAR",
    "Rod": "ROD",
    "Tube": "TUBE",
}

# ───────────────────────────────────────────────
# Basic categories (shown in first dropdown)
# ───────────────────────────────────────────────
CATEGORIES = [
    "Metals",
    "Phenolics",
    "Plastics",
    "Electrical Cable",
]

# ───────────────────────────────────────────────
# Level 2 – options per category
# ───────────────────────────────────────────────
LEVEL2_OPTIONS: Dict[str, Union[List[str], Dict[str, Dict[str, str]]]] = {
    "Metals": [
        "Aluminum",
        "Titanium",
        "Stainless Steel",
        "Steel",
        "Copper",
    ],
    "Phenolics": {
        "Linen Electrical":     {"spec": "MIL-I-24768/13"},
        "G3 Glass":             {"spec": "MIL-I-24768/18"},
        "G5 Melamine":          {"spec": "MIL-I-24768/8"},
        "G7 Silicone":          {"spec": "MIL-I-24768/17"},
        "Canvas Electrical":    {"spec": "MIL-I-24768/14"},
    },
    "Plastics": [
        "HDPE",
        "UHMW",
        "Polycarbonate",
        "Acetal Resin",
        "Nylon",
    ],
    "Electrical Cable": {
        "Single-Conductor Wire": {"prefix": "EC-WIRE-AS22759/"},
        "Multi-Conductor Cable": {"prefix": "EC-CBL-WC27500"},
        "Coaxial Cable":         {"prefix": "EC-COAX-M17/"},
    },
}

# ───────────────────────────────────────────────
# Level 3 – options per level-2 choice
# ───────────────────────────────────────────────

# Metals → Alloy / Grade
METALS_ALLOYS: Dict[str, List[str]] = {
    "Aluminum":     ["2024", "6061", "7075", "7050"],
    "Titanium":     ["6Al-4V", "6Al-4V ELI", "6Al-2Sn-4Zr-2Mo"],
    "Stainless Steel": ["304", "316", "17-4PH"],
    "Steel":        ["4340", "300M", "Aermet 100"],
    "Copper":       ["C10100", "C17200"],
}

# Plastics → Material / Grade
PLASTICS_GRADES: Dict[str, List[str]] = {
    "HDPE":         ["PE300", "PE500"],
    "UHMW":         ["PE1000", "Tivar-1000", "Tivar-88"],
    "Polycarbonate": ["Lexan", "Glass-filled"],
    "Acetal Resin": ["Generic(Acetal)", "Delrin 150", "Delrin AF"],
    "Nylon":        ["Nylon 6", "Nylon 6/6"],
}


# ───────────────────────────────────────────────
# Level 4 – options per level-3 choice
# ───────────────────────────────────────────────
METALS_TEMPERS: Dict[str, List[str]] = {
    "Aluminum": {
        "2024": ["T3", "T351", "T4"],
        "6061": ["T6", "T651"],
        "7075": ["T6", "T651", "T73", "T7351"],
        "7050": ["T7451", "T76"],
    },
    "Titanium": {
        "6Al-4V": ["Annealed", "STA"],
        "6Al-4V ELI": ["Annealed"],
        "6Al-2Sn-4Zr-2Mo": ["Annealed", "STA"],
    },
    "Stainless Steel": {
        "304": ["Annealed", "1/8 hard", "1/4 hard", "1/2 hard", "3/4 hard", "Full hard"],
        "316": ["Annealed", "Condition B"],
        "17-4PH": ["Annealed", "H900", "H1025"],
    },
    "Steel": {
        "4340": ["Normalized", "Q&T"],
        "300M": ["Q&T"],
        "Aermet 100": ["Q&T"],
    },
    "Copper": {
        "C10100": ["Annealed", "H02"],
        "C17200": ["TB00", "TF00"],
    },
}

PLASTICS_VARIANTS: Dict[str, List[str]] = {
    # HDPE
    "PE300":    ["Black", "Natural"],
    "PE500":    ["Black", "Natural"],
    
    # UHMW
    "PE1000":   ["Black", "Natural"],
    "Tivar-1000": ["Black", "Natural"],
    "Tivar-88":   ["Black", "Natural"],
    
    # Polycarbonate
    "Lexan":      ["9034", "XL10", "MR10", "MP"],
    "Glass-filled": ["10%", "20%", "30%"],
    
    # Acetal Resin
    "Generic(Acetal)": ["Black", "Natural"],
    "Delrin 150":      ["Black", "Natural"],
    "Delrin AF":       ["100AF", "500AF", "DE588AF"],
    
    # Nylon
    "Nylon 6":    ["Natural", "Glass-filled", "Oil-filled"],
    "Nylon 6/6":  ["Natural", "Glass-filled", "MDS-filled"],
}

# ───────────────────────────────────────────────
# Metals - AMS/Material Spec lookup
# ───────────────────────────────────────────────
AMS_LOOKUP: Dict[str, Dict[str, Dict[str, Dict[str, List[str]]]]] = {
    "AL": {  # Aluminum
        "2024": {
            "T3": {
                "SHEET": ["AMS4037", "AMS4041"],
                "PLATE/BAR": ["AMS4037"],
                "ROD": ["AMS4120"],
                "TUBE": ["AMS4088"],
            },
            "T351": {
                "SHEET": ["AMS4037"],
                "PLATE/BAR": ["AMS4037"],
                "ROD": ["AMS4120", "AMS-QQ-A-225/6"],
                "TUBE": [],  # Less common for T351
            },
            "T4": {
                "SHEET": ["AMS4035"],
                "PLATE/BAR": ["AMS-QQ-A-250/4"],
                "ROD": ["AMS4120"],
                "TUBE": ["AMS4087"],
            },
        },
        "6061": {
            "T6": {
                "SHEET": ["AMS4027"],
                "PLATE/BAR": ["AMS4027"],
                "ROD": ["AMS4117"],
                "TUBE": ["AMS4070"],
            },
            "T651": {
                "SHEET": ["AMS4027"],
                "PLATE/BAR": ["AMS4027"],
                "ROD": ["AMS4117"],
                "TUBE": [],  # Less common
            },
        },
        "7075": {
            "T6": {
                "SHEET": ["AMS4045", "AMS4049"],
                "PLATE/BAR": ["AMS4045"],
                "ROD": ["AMS4123"],
                "TUBE": [],  # Rare in tube form
            },
            "T651": {
                "SHEET": ["AMS4045"],
                "PLATE/BAR": ["AMS4045"],
                "ROD": ["AMS4123"],
                "TUBE": [],
            },
            "T73": {
                "SHEET": ["AMS4078"],
                "PLATE/BAR": ["AMS4078"],
                "ROD": ["AMS4124"],
                "TUBE": [],
            },
            "T7351": {
                "SHEET": ["AMS4078"],
                "PLATE/BAR": ["AMS4078"],
                "ROD": ["AMS4124"],
                "TUBE": [],
            },
        },
        "7050": {
            "T7451": {
                "SHEET": ["AMS4050"],
                "PLATE/BAR": ["AMS4050"],
                "ROD": [],  # Often custom / forging specs
                "TUBE": [],
            },
            "T76": {
                "SHEET": ["AMS4201"],
                "PLATE/BAR": ["AMS4050"],
                "ROD": [],
                "TUBE": [],
            },
        },
    },
    "TI": {  # Titanium
        "6Al-4V": {
            "Annealed": {
                "SHEET": ["AMS4911"],
                "PLATE/BAR": ["AMS4911"],
                "ROD": ["AMS4928"],
                "TUBE": ["AMS4943"],
            },
            "STA": {
                "SHEET": ["AMS4911"],
                "PLATE/BAR": ["AMS6930"],
                "ROD": ["AMS6930"],
                "TUBE": [],
            },
        },
        "6Al-4V ELI": {
            "Annealed": {
                "SHEET": ["AMS4907"],
                "PLATE/BAR": ["AMS4907"],
                "ROD": ["AMS4956"],
                "TUBE": [],
            },
        },
        "6Al-2Sn-4Zr-2Mo": {
            "Annealed": {
                "SHEET": ["AMS4919"],
                "PLATE/BAR": ["AMS4919"],
                "ROD": ["AMS4975"],
                "TUBE": [],
            },
            "STA": {
                "SHEET": ["AMS4919"],
                "PLATE/BAR": ["AMS4919"],
                "ROD": ["AMS4976"],
                "TUBE": [],
            },
        },
    },
    "SS": {  # Stainless Steel
        "304": {
            "Annealed": {
                "SHEET": ["AMS5511"],
                "PLATE/BAR": ["AMS5639"],
                "ROD": ["AMS5639"],
                "TUBE": ["AMS5560"],
            },
            # Work-hardened tempers often AMS5517 / 5516 etc. or QQ-S-766
            "1/4 hard": {
                "SHEET": ["AMS5517"], 
                "PLATE/BAR": [], 
                "ROD": [], 
                "TUBE": []},
            # ... add others as needed
        },
        "316": {
            "Annealed": {
                "SHEET": ["AMS5524"],
                "PLATE/BAR": ["AMS5648"],
                "ROD": ["AMS5648"],
                "TUBE": ["AMS6903"],
            },
        },
        "17-4PH": {
            "Annealed": {
                "SHEET": ["AMS5863"],
                "PLATE/BAR": ["AMS5643"],
                "ROD": ["AMS5643"],
                "TUBE": [],
            },
            "H900": {
                "SHEET": ["AMS5863"],
                "PLATE/BAR": ["AMS5643"],
                "ROD": ["AMS5643"],
                "TUBE": [],
            },
            "H1025": {
                "SHEET": ["AMS5863"],
                "PLATE/BAR": ["AMS5643"],
                "ROD": ["AMS5643"],
                "TUBE": [],
            },
        },
    },
    "ST": {  # Alloy Steel
        "4340": {
            "Normalized": {
                "SHEET": [],  # Rare
                "PLATE/BAR": ["AMS6359"],
                "ROD": ["AMS6414"],
                "TUBE": [],
            },
            "Q&T": {
                "SHEET": [],
                "PLATE/BAR": ["AMS6414"],
                "ROD": ["AMS6414"],
                "TUBE": [],
            },
        },
        "300M": {
            "Q&T": {
                "SHEET": [],
                "PLATE/BAR": ["AMS6417"],
                "ROD": ["AMS6419"],
                "TUBE": [],
            },
        },
        "Aermet 100": {
            "Q&T": {
                "SHEET": [],
                "PLATE/BAR": ["AMS6532"],
                "ROD": ["AMS6532"],
                "TUBE": [],
            },
        },
    },
    "CU": {  # Copper (less common AMSin aerospace; often ASTM)
        "C10100": {
            "Annealed": {
                "SHEET": ["AMS4500"],
                "PLATE/BAR": [],
                "ROD": [],
                "TUBE": [],
            },
            "H02": {
                "SHEET": [],
                "PLATE/BAR": [],
                "ROD": [],
                "TUBE": [],
            },
        },
        "C17200": {
            "TB00": {  # Solution annealed
                "SHEET": ["AMS4530"],
                "PLATE/BAR": ["AMS4533"],
                "ROD": ["AMS4533"],
                "TUBE": [],
            },
            "TF00": {  # Aged
                "SHEET": ["AMS4530"],
                "PLATE/BAR": ["AMS4533"],
                "ROD": ["AMS4533"],
                "TUBE": [],
            },
        },
    },
}

# ───────────────────────────────────────────────
# Abbreviations used in final part number
# ───────────────────────────────────────────────
ABBREV_MAP: Dict[str, str] = {
    
    # Materials
    "Aluminum":        "AL",
    "Titanium":        "TI",
    "Stainless Steel": "SS",
    "Steel":           "ST",
    "Copper":          "CU",
    "Linen Electrical": "LE",
    "G3 Glass":        "G3",
    "G5 Melamine":     "G5",
    "G7 Silicone":     "G7",
    "Canvas Electrical": "CE",
    "Polycarbonate":   "PC",
    "Generic(Acetal)":  "AR",
    "Delrin 150":     "DEL",
    "Delrin AF":      "DEL",
    "Lexan":          "LEX",
    
    # Metals – conditions / tempers (will be used later)
    "T3": "T3", 
    "T351": "T351", 
    "T4": "T4",
    "T6": "T6", 
    "T651": "T651", 
    "T73": "T73", 
    "T7351": "T7351",
    "T7451": "T7451", 
    "T76": "T76",
    "Annealed": "ANN", 
    "STA": "STA",
    "Normalized": "NORM", 
    "Q&T": "QT",
    "Condition B": "B",
    "1/4 hard": "1/4H", 
    "1/2 hard": "1/2H", 
    "3/4 hard": "3/4H", 
    "Full hard": "FH",
    "H900": "H900", 
    "H1025": "H1025",

    # Plastics – variants / colors / fillers
    "Black": "BLK", 
    "Natural": "NAT",
    "Glass-filled": "GF", 
    "10%": "10", 
    "20%": "20", 
    "30%": "30",
    "Oil-filled": "OF", 
    "MDS-filled": "MDS",
    
}

# ───────────────────────────────────────────────
# Helper functions – get filtered options for UI
# ───────────────────────────────────────────────

def get_level2_options(category: str) -> List[str]:
    level2 = LEVEL2_OPTIONS.get(category, [])
    if isinstance(level2, dict):
        return [""] + list(level2.keys())
    else:
        return [""] + level2

def get_alloy_options(material: str) -> List[str]:
    return [""] + METALS_ALLOYS.get(material, [])

def get_metal_temper_options(material: str, alloy: str) -> List[str]:
    if not material or not alloy:
        return []    
    # METALS_TEMPERS is Dict[material, Dict[alloy, List[temper]]]
    material_data = METALS_TEMPERS.get(material, {})
    tempers = material_data.get(alloy, [])
    return tempers

def get_ams(material_code: str, alloy: str, temper: str, form: str) -> List[str]:
    try:
        return AMS_LOOKUP[material_code][alloy][temper][form]
    except KeyError:
        return []  # Not found / not common

def get_phenolic_spec(phenolic_type: str) -> str:
    phenolics = LEVEL2_OPTIONS.get("Phenolics", {})
    return phenolics.get(phenolic_type, {}).get("spec", "")


def get_cable_prefix(cable_type: str) -> str:
    cables = LEVEL2_OPTIONS.get("Electrical Cable", {})
    return cables.get(cable_type, {}).get("prefix", "")


def get_plastic_grade_options(family: str) -> List[str]:
    return PLASTICS_GRADES.get(family, [""])

def get_plastic_variant_options(grade: str) -> List[str]:
    """Return possible variants/colors/fills for a given plastic grade."""
    return PLASTICS_VARIANTS.get(grade, [])

def get_abbrev(text: str, default: str = "") -> str:
    """Convert full name to abbreviation if known, else fallback"""
    return ABBREV_MAP.get(text, default or text.upper().replace(" ", "").replace("-", ""))



def build_part_number(session_state) -> str:
    """
    Builds the final part number based on current selections.
    Returns the PN string or an error message if incomplete.
    """
    cat = session_state.get("category", "")
    if not cat:
        return "Incomplete: No category selected"

    # Common pieces – form abbrev + dimensions string
    form = session_state.get("form", "")
    form_abbr = FORM_ABBREVIATIONS.get(form, "")
    dims = ""

    if session_state.get("dimensions_confirmed", False):
        if form in ["Sheet (thickness <= 0.25\")", "Plate/Bar (thickness > 0.25\")"]:
            t = session_state.get("parsed_thickness")
            w = session_state.get("parsed_width")
            if t is not None and w is not None:
                dims = f"T{t}-W{w}"
        elif form == "Rod":
            d = session_state.get("parsed_diameter")
            if d is not None:
                dims = f"D{d}"
        elif form == "Tube":
            wall = session_state.get("parsed_wall")
            od = session_state.get("parsed_od")
            if wall is not None and od is not None:
                dims = f"WT{wall}-OD{od}"

    # Category-specific PN construction
    if cat == "Metals":
        material_full = session_state.get("level2_Metals", "")
        alloy        = session_state.get("third_Metals", "")
        temper_full  = session_state.get("fourth_Metals", "")
        form         = session_state.get("form", "")

        if not all([material_full, alloy, temper_full, form]):
            return "Incomplete: Missing metal details (material, alloy, temper, or form)"

        # Abbreviations
        material_abbr = ABBREV_MAP.get(material_full, get_abbrev(material_full))
        temper_abbr   = get_abbrev(temper_full)

        # AMS spec lookup
        ams_list = get_ams(material_abbr, alloy, temper_abbr, form_abbr)
        
        spec = ""
        if ams_list:
            spec = ams_list[0]  # Just take the first one for simplicity

        # Build pieces
        pieces = [
            material_abbr,
            alloy,
            temper_abbr,
            spec,
            form_abbr,
            dims
        ]

        pn = "-".join(filter(None, pieces)).upper()
        
        # Optional: flag if spec was missing
        if "NO-SPEC-FOUND" in pn:
            return f"{pn}  (Warning: No AMS spec found for this combination)"
        
        return pn

    elif cat == "Phenolics":
        p_type = session_state.get("level2_Phenolics", "")
        if not p_type or not form:
            return "Incomplete: Missing phenolic details"
        spec = get_phenolic_spec(p_type)
        type_abbr = get_abbrev(p_type)  # e.g. "Linen Electrical" → "LE"
        pieces = [type_abbr, spec, form_abbr, dims]
        return "-".join(filter(None, pieces)).upper()

    elif cat == "Plastics":
        family = session_state.get("level2_Plastics", "")
        grade = session_state.get("third_Plastics", "")
        variant = session_state.get("variant_Plastics", "")
        if not all([family, grade, variant, form]):
            return "Incomplete: Missing plastic details"
        family_abbr = get_abbrev(family)  # e.g. "HDPE" → "HDPE"
        grade_abbr = get_abbrev(grade)    # e.g. "Tivar-1000" → "T1000"
        variant_abbr = get_abbrev(variant) # e.g. "Black" → "BLK"
        # Spec is fixed per grade/family (from document)
        spec = ""
        if grade in ["PE300", "PE500"]:
            spec = "ASTM-D4976"
        elif grade == "PE1000":
            spec = "ASTM-D4020"
        elif grade in ["Lexan"]:
            spec = "AMS-P-83310"
        elif grade == "Glass-filled":
            spec = "ASTM-D3935"
        # ... add more from document if needed
        pieces = [family_abbr, grade_abbr, variant_abbr, spec, form_abbr, dims]
        return "-".join(filter(None, pieces)).upper()

    elif cat == "Electrical Cable":
        # Read all values saved by the widgets (they use key= so Streamlit auto-saves them)
        cable_type   = session_state.get("level2_Electrical_Cable", "").strip()
        spool_choice = session_state.get("cable_spool", "No")
        length       = session_state.get("cable_length", "").strip().upper()

        # Safety: must have a type
        if not cable_type:
            return "Incomplete: No cable type selected"

        # Get the prefix (already defined in your LEVEL2_OPTIONS)
        prefix = get_cable_prefix(cable_type)  

        # Start building the pieces list
        pieces = [prefix]

        # ───────────────────────────────────────────────
        # Branch by cable type – exactly matching your spec
        # ───────────────────────────────────────────────
        if "Single-Conductor" in cable_type:
            slash = session_state.get("cable_slash", "").strip()
            awg   = session_state.get("cable_awg_size", "").strip()
            color = session_state.get("cable_color", "").strip().upper()

            # Required field
            if not slash:
                return "Incomplete: Missing Slash Sheet Number for Single-Conductor Wire"

            pieces.append(slash)

            # Optional AWG / Size
            if awg:
                pieces.append(awg)

            # Optional Color Code
            if color:
                pieces.append(color)

        elif "Multi-Conductor" in cable_type:
            config = session_state.get("cable_config", "").strip()

            # Required field
            if not config:
                return "Incomplete: Missing Configuration Code for Multi-Conductor Cable"

            pieces.append(config)

        elif "Coaxial" in cable_type:
            slash = session_state.get("cable_slash", "").strip()

            # Required field
            if not slash:
                return "Incomplete: Missing Slash Sheet Number for Coaxial Cable"

            pieces.append(slash)

        else:
            return "Incomplete: Unrecognized cable type"

        # ───────────────────────────────────────────────
        # Common: Spool handling (same for all types)
        # ───────────────────────────────────────────────
        if spool_choice == "Yes":
            pieces.append("SPOOL")
            if length:
                pieces.append(length)

        # Final PN – uppercase everything
        pn = "-".join(pieces).upper()
        if pn.count("-") > 1 and "/-" in pn:
            pn = pn.replace("/-", "/")  # fix the double separator
        return pn


# data.py
"""
Central place for all raw material classification data:
categories, materials, alloys, grades, forms, abbreviations, etc.
"""

from typing import Dict, List, Optional, Union

# ───────────────────────────────────────────────
# Forms
# ───────────────────────────────────────────────
COMMON_FORMS = [
    "Sheet (thickness <= 0.25\")",
    "Plate/Bar (thickness > 0.25\")",
    "Rod",
    "Tube",
]

FORM_ABBREVIATIONS = {
    "Sheet (thickness <= 0.25\")": "SHT",
    "Plate/Bar (thickness > 0.25\")": "BAR",
    "Rod": "ROD",
    "Tube": "TUBE",
}

# ───────────────────────────────────────────────
# Basic categories (shown in first dropdown)
# ───────────────────────────────────────────────
CATEGORIES = [
    "Metals",
    "Phenolics",
    "Plastics",
    "Electrical Cable",
]

# ───────────────────────────────────────────────
# Level 2 – options per category
# ───────────────────────────────────────────────
LEVEL2_OPTIONS: Dict[str, Union[List[str], Dict[str, Dict[str, str]]]] = {
    "Metals": [
        "Aluminum",
        "Titanium",
        "Stainless Steel",
        "Steel",
        "Copper",
    ],
    "Phenolics": {
        "Linen Electrical":     {"spec": "MIL-I-24768/13"},
        "G3 Glass":             {"spec": "MIL-I-24768/18"},
        "G5 Melamine":          {"spec": "MIL-I-24768/8"},
        "G7 Silicone":          {"spec": "MIL-I-24768/17"},
        "Canvas Electrical":    {"spec": "MIL-I-24768/14"},
    },
    "Plastics": [
        "HDPE",
        "UHMW",
        "Polycarbonate",
        "Acetal Resin",
        "Nylon",
    ],
    "Electrical Cable": {
        "Single-Conductor Wire": {"prefix": "EC-WIRE-AS22759/"},
        "Multi-Conductor Cable": {"prefix": "EC-CBL-WC27500"},
        "Coaxial Cable":         {"prefix": "EC-COAX-M17/"},
    },
}

# ───────────────────────────────────────────────
# Level 3 – options per level-2 choice
# ───────────────────────────────────────────────

# Metals → Alloy / Grade
METALS_ALLOYS: Dict[str, List[str]] = {
    "Aluminum":     ["2024", "6061", "7075", "7050"],
    "Titanium":     ["6Al-4V", "6Al-4V ELI", "6Al-2Sn-4Zr-2Mo"],
    "Stainless Steel": ["304", "316", "17-4PH"],
    "Steel":        ["4340", "300M", "Aermet 100"],
    "Copper":       ["C10100", "C17200"],
}

# Plastics → Material / Grade
PLASTICS_GRADES: Dict[str, List[str]] = {
    "HDPE":         ["PE300", "PE500"],
    "UHMW":         ["PE1000", "Tivar-1000", "Tivar-88"],
    "Polycarbonate": ["Lexan", "Glass-filled"],
    "Acetal Resin": ["Generic(Acetal)", "Delrin 150", "Delrin AF"],
    "Nylon":        ["Nylon 6", "Nylon 6/6"],
}


# ───────────────────────────────────────────────
# Level 4 – options per level-3 choice
# ───────────────────────────────────────────────
METALS_TEMPERS: Dict[str, List[str]] = {
    "Aluminum": {
        "2024": ["T3", "T351", "T4"],
        "6061": ["T6", "T651"],
        "7075": ["T6", "T651", "T73", "T7351"],
        "7050": ["T7451", "T76"],
    },
    "Titanium": {
        "6Al-4V": ["Annealed", "STA"],
        "6Al-4V ELI": ["Annealed"],
        "6Al-2Sn-4Zr-2Mo": ["Annealed", "STA"],
    },
    "Stainless Steel": {
        "304": ["Annealed", "1/8 hard", "1/4 hard", "1/2 hard", "3/4 hard", "Full hard"],
        "316": ["Annealed", "Condition B"],
        "17-4PH": ["Annealed", "H900", "H1025"],
    },
    "Steel": {
        "4340": ["Normalized", "Q&T"],
        "300M": ["Q&T"],
        "Aermet 100": ["Q&T"],
    },
    "Copper": {
        "C10100": ["Annealed", "H02"],
        "C17200": ["TB00", "TF00"],
    },
}

PLASTICS_VARIANTS: Dict[str, List[str]] = {
    # HDPE
    "PE300":    ["Black", "Natural"],
    "PE500":    ["Black", "Natural"],
    
    # UHMW
    "PE1000":   ["Black", "Natural"],
    "Tivar-1000": ["Black", "Natural"],
    "Tivar-88":   ["Black", "Natural"],
    
    # Polycarbonate
    "Lexan":      ["9034", "XL10", "MR10", "MP"],
    "Glass-filled": ["10%", "20%", "30%"],
    
    # Acetal Resin
    "Generic(Acetal)": ["Black", "Natural"],
    "Delrin 150":      ["Black", "Natural"],
    "Delrin AF":       ["100AF", "500AF", "DE588AF"],
    
    # Nylon
    "Nylon 6":    ["Natural", "Glass-filled", "Oil-filled"],
    "Nylon 6/6":  ["Natural", "Glass-filled", "MDS-filled"],
}

# ───────────────────────────────────────────────
# Metals - AMS/Material Spec lookup
# ───────────────────────────────────────────────
AMS_LOOKUP: Dict[str, Dict[str, Dict[str, Dict[str, List[str]]]]] = {
    "AL": {  # Aluminum
        "2024": {
            "T3": {
                "SHEET": ["AMS4037", "AMS4041"],
                "PLATE/BAR": ["AMS4037"],
                "ROD": ["AMS4120"],
                "TUBE": ["AMS4088"],
            },
            "T351": {
                "SHEET": ["AMS4037"],
                "PLATE/BAR": ["AMS4037"],
                "ROD": ["AMS4120", "AMS-QQ-A-225/6"],
                "TUBE": [],  # Less common for T351
            },
            "T4": {
                "SHEET": ["AMS4035"],
                "PLATE/BAR": ["AMS-QQ-A-250/4"],
                "ROD": ["AMS4120"],
                "TUBE": ["AMS4087"],
            },
        },
        "6061": {
            "T6": {
                "SHEET": ["AMS4027"],
                "PLATE/BAR": ["AMS4027"],
                "ROD": ["AMS4117"],
                "TUBE": ["AMS4070"],
            },
            "T651": {
                "SHEET": ["AMS4027"],
                "PLATE/BAR": ["AMS4027"],
                "ROD": ["AMS4117"],
                "TUBE": [],  # Less common
            },
        },
        "7075": {
            "T6": {
                "SHEET": ["AMS4045", "AMS4049"],
                "PLATE/BAR": ["AMS4045"],
                "ROD": ["AMS4123"],
                "TUBE": [],  # Rare in tube form
            },
            "T651": {
                "SHEET": ["AMS4045"],
                "PLATE/BAR": ["AMS4045"],
                "ROD": ["AMS4123"],
                "TUBE": [],
            },
            "T73": {
                "SHEET": ["AMS4078"],
                "PLATE/BAR": ["AMS4078"],
                "ROD": ["AMS4124"],
                "TUBE": [],
            },
            "T7351": {
                "SHEET": ["AMS4078"],
                "PLATE/BAR": ["AMS4078"],
                "ROD": ["AMS4124"],
                "TUBE": [],
            },
        },
        "7050": {
            "T7451": {
                "SHEET": ["AMS4050"],
                "PLATE/BAR": ["AMS4050"],
                "ROD": [],  # Often custom / forging specs
                "TUBE": [],
            },
            "T76": {
                "SHEET": ["AMS4201"],
                "PLATE/BAR": ["AMS4050"],
                "ROD": [],
                "TUBE": [],
            },
        },
    },
    "TI": {  # Titanium
        "6Al-4V": {
            "Annealed": {
                "SHEET": ["AMS4911"],
                "PLATE/BAR": ["AMS4911"],
                "ROD": ["AMS4928"],
                "TUBE": ["AMS4943"],
            },
            "STA": {
                "SHEET": ["AMS4911"],
                "PLATE/BAR": ["AMS6930"],
                "ROD": ["AMS6930"],
                "TUBE": [],
            },
        },
        "6Al-4V ELI": {
            "Annealed": {
                "SHEET": ["AMS4907"],
                "PLATE/BAR": ["AMS4907"],
                "ROD": ["AMS4956"],
                "TUBE": [],
            },
        },
        "6Al-2Sn-4Zr-2Mo": {
            "Annealed": {
                "SHEET": ["AMS4919"],
                "PLATE/BAR": ["AMS4919"],
                "ROD": ["AMS4975"],
                "TUBE": [],
            },
            "STA": {
                "SHEET": ["AMS4919"],
                "PLATE/BAR": ["AMS4919"],
                "ROD": ["AMS4976"],
                "TUBE": [],
            },
        },
    },
    "SS": {  # Stainless Steel
        "304": {
            "Annealed": {
                "SHEET": ["AMS5511"],
                "PLATE/BAR": ["AMS5639"],
                "ROD": ["AMS5639"],
                "TUBE": ["AMS5560"],
            },
            # Work-hardened tempers often AMS5517 / 5516 etc. or QQ-S-766
            "1/4 hard": {
                "SHEET": ["AMS5517"], 
                "PLATE/BAR": [], 
                "ROD": [], 
                "TUBE": []},
            # ... add others as needed
        },
        "316": {
            "Annealed": {
                "SHEET": ["AMS5524"],
                "PLATE/BAR": ["AMS5648"],
                "ROD": ["AMS5648"],
                "TUBE": ["AMS6903"],
            },
        },
        "17-4PH": {
            "Annealed": {
                "SHEET": ["AMS5863"],
                "PLATE/BAR": ["AMS5643"],
                "ROD": ["AMS5643"],
                "TUBE": [],
            },
            "H900": {
                "SHEET": ["AMS5863"],
                "PLATE/BAR": ["AMS5643"],
                "ROD": ["AMS5643"],
                "TUBE": [],
            },
            "H1025": {
                "SHEET": ["AMS5863"],
                "PLATE/BAR": ["AMS5643"],
                "ROD": ["AMS5643"],
                "TUBE": [],
            },
        },
    },
    "ST": {  # Alloy Steel
        "4340": {
            "Normalized": {
                "SHEET": [],  # Rare
                "PLATE/BAR": ["AMS6359"],
                "ROD": ["AMS6414"],
                "TUBE": [],
            },
            "Q&T": {
                "SHEET": [],
                "PLATE/BAR": ["AMS6414"],
                "ROD": ["AMS6414"],
                "TUBE": [],
            },
        },
        "300M": {
            "Q&T": {
                "SHEET": [],
                "PLATE/BAR": ["AMS6417"],
                "ROD": ["AMS6419"],
                "TUBE": [],
            },
        },
        "Aermet 100": {
            "Q&T": {
                "SHEET": [],
                "PLATE/BAR": ["AMS6532"],
                "ROD": ["AMS6532"],
                "TUBE": [],
            },
        },
    },
    "CU": {  # Copper (less common AMSin aerospace; often ASTM)
        "C10100": {
            "Annealed": {
                "SHEET": ["AMS4500"],
                "PLATE/BAR": [],
                "ROD": [],
                "TUBE": [],
            },
            "H02": {
                "SHEET": [],
                "PLATE/BAR": [],
                "ROD": [],
                "TUBE": [],
            },
        },
        "C17200": {
            "TB00": {  # Solution annealed
                "SHEET": ["AMS4530"],
                "PLATE/BAR": ["AMS4533"],
                "ROD": ["AMS4533"],
                "TUBE": [],
            },
            "TF00": {  # Aged
                "SHEET": ["AMS4530"],
                "PLATE/BAR": ["AMS4533"],
                "ROD": ["AMS4533"],
                "TUBE": [],
            },
        },
    },
}

# ───────────────────────────────────────────────
# Abbreviations used in final part number
# ───────────────────────────────────────────────
ABBREV_MAP: Dict[str, str] = {
    
    # Materials
    "Aluminum":        "AL",
    "Titanium":        "TI",
    "Stainless Steel": "SS",
    "Steel":           "ST",
    "Copper":          "CU",
    "Linen Electrical": "LE",
    "G3 Glass":        "G3",
    "G5 Melamine":     "G5",
    "G7 Silicone":     "G7",
    "Canvas Electrical": "CE",
    "Polycarbonate":   "PC",
    "Generic(Acetal)":  "AR",
    "Delrin 150":     "DEL",
    "Delrin AF":      "DEL",
    "Lexan":          "LEX",
    
    # Metals – conditions / tempers (will be used later)
    "T3": "T3", 
    "T351": "T351", 
    "T4": "T4",
    "T6": "T6", 
    "T651": "T651", 
    "T73": "T73", 
    "T7351": "T7351",
    "T7451": "T7451", 
    "T76": "T76",
    "Annealed": "ANN", 
    "STA": "STA",
    "Normalized": "NORM", 
    "Q&T": "QT",
    "Condition B": "B",
    "1/4 hard": "1/4H", 
    "1/2 hard": "1/2H", 
    "3/4 hard": "3/4H", 
    "Full hard": "FH",
    "H900": "H900", 
    "H1025": "H1025",

    # Plastics – variants / colors / fillers
    "Black": "BLK", 
    "Natural": "NAT",
    "Glass-filled": "GF", 
    "10%": "10", 
    "20%": "20", 
    "30%": "30",
    "Oil-filled": "OF", 
    "MDS-filled": "MDS",
    
}

# ───────────────────────────────────────────────
# Helper functions – get filtered options for UI
# ───────────────────────────────────────────────

def get_level2_options(category: str) -> List[str]:
    level2 = LEVEL2_OPTIONS.get(category, [])
    if isinstance(level2, dict):
        return [""] + list(level2.keys())
    else:
        return [""] + level2

def get_alloy_options(material: str) -> List[str]:
    return [""] + METALS_ALLOYS.get(material, [])

def get_metal_temper_options(material: str, alloy: str) -> List[str]:
    if not material or not alloy:
        return []    
    # METALS_TEMPERS is Dict[material, Dict[alloy, List[temper]]]
    material_data = METALS_TEMPERS.get(material, {})
    tempers = material_data.get(alloy, [])
    return tempers

def get_ams(material_code: str, alloy: str, temper: str, form: str) -> List[str]:
    try:
        return AMS_LOOKUP[material_code][alloy][temper][form]
    except KeyError:
        return []  # Not found / not common

def get_phenolic_spec(phenolic_type: str) -> str:
    phenolics = LEVEL2_OPTIONS.get("Phenolics", {})
    return phenolics.get(phenolic_type, {}).get("spec", "")


def get_cable_prefix(cable_type: str) -> str:
    cables = LEVEL2_OPTIONS.get("Electrical Cable", {})
    return cables.get(cable_type, {}).get("prefix", "")


def get_plastic_grade_options(family: str) -> List[str]:
    return PLASTICS_GRADES.get(family, [""])

def get_plastic_variant_options(grade: str) -> List[str]:
    """Return possible variants/colors/fills for a given plastic grade."""
    return PLASTICS_VARIANTS.get(grade, [])

def get_abbrev(text: str, default: str = "") -> str:
    """Convert full name to abbreviation if known, else fallback"""
    return ABBREV_MAP.get(text, default or text.upper().replace(" ", "").replace("-", ""))



def build_part_number(session_state) -> str:
    """
    Builds the final part number based on current selections.
    Returns the PN string or an error message if incomplete.
    """
    cat = session_state.get("category", "")
    if not cat:
        return "Incomplete: No category selected"

    # Common pieces – form abbrev + dimensions string
    form = session_state.get("form", "")
    form_abbr = FORM_ABBREVIATIONS.get(form, "")
    dims = ""

    if session_state.get("dimensions_confirmed", False):
        if form in ["Sheet (thickness <= 0.25\")", "Plate/Bar (thickness > 0.25\")"]:
            t = session_state.get("parsed_thickness")
            w = session_state.get("parsed_width")
            if t is not None and w is not None:
                dims = f"T{t}-W{w}"
        elif form == "Rod":
            d = session_state.get("parsed_diameter")
            if d is not None:
                dims = f"D{d}"
        elif form == "Tube":
            wall = session_state.get("parsed_wall")
            od = session_state.get("parsed_od")
            if wall is not None and od is not None:
                dims = f"WT{wall}-OD{od}"

    # Category-specific PN construction
    if cat == "Metals":
        material_full = session_state.get("level2_Metals", "")
        alloy        = session_state.get("third_Metals", "")
        temper_full  = session_state.get("fourth_Metals", "")
        form         = session_state.get("form", "")

        if not all([material_full, alloy, temper_full, form]):
            return "Incomplete: Missing metal details (material, alloy, temper, or form)"

        # Abbreviations
        material_abbr = ABBREV_MAP.get(material_full, get_abbrev(material_full))
        temper_abbr   = get_abbrev(temper_full)

        # AMS spec lookup
        ams_list = get_ams(material_abbr, alloy, temper_abbr, form_abbr)
        
        spec = ""
        if ams_list:
            spec = ams_list[0]  # Just take the first one for simplicity

        # Build pieces
        pieces = [
            material_abbr,
            alloy,
            temper_abbr,
            spec,
            form_abbr,
            dims
        ]

        pn = "-".join(filter(None, pieces)).upper()
        
        # Optional: flag if spec was missing
        if "NO-SPEC-FOUND" in pn:
            return f"{pn}  (Warning: No AMS spec found for this combination)"
        
        return pn

    elif cat == "Phenolics":
        p_type = session_state.get("level2_Phenolics", "")
        if not p_type or not form:
            return "Incomplete: Missing phenolic details"
        spec = get_phenolic_spec(p_type)
        type_abbr = get_abbrev(p_type)  # e.g. "Linen Electrical" → "LE"
        pieces = [type_abbr, spec, form_abbr, dims]
        return "-".join(filter(None, pieces)).upper()

    elif cat == "Plastics":
        family = session_state.get("level2_Plastics", "")
        grade = session_state.get("third_Plastics", "")
        variant = session_state.get("variant_Plastics", "")
        if not all([family, grade, variant, form]):
            return "Incomplete: Missing plastic details"
        family_abbr = get_abbrev(family)  # e.g. "HDPE" → "HDPE"
        grade_abbr = get_abbrev(grade)    # e.g. "Tivar-1000" → "T1000"
        variant_abbr = get_abbrev(variant) # e.g. "Black" → "BLK"
        # Spec is fixed per grade/family (from document)
        spec = ""
        if grade in ["PE300", "PE500"]:
            spec = "ASTM-D4976"
        elif grade == "PE1000":
            spec = "ASTM-D4020"
        elif grade in ["Lexan"]:
            spec = "AMS-P-83310"
        elif grade == "Glass-filled":
            spec = "ASTM-D3935"
        # ... add more from document if needed
        pieces = [family_abbr, grade_abbr, variant_abbr, spec, form_abbr, dims]
        return "-".join(filter(None, pieces)).upper()

    elif cat == "Electrical Cable":
        # Read all values saved by the widgets (they use key= so Streamlit auto-saves them)
        cable_type   = session_state.get("level2_Electrical_Cable", "").strip()
        spool_choice = session_state.get("cable_spool", "No")
        length       = session_state.get("cable_length", "").strip().upper()

        # Safety: must have a type
        if not cable_type:
            return "Incomplete: No cable type selected"

        # Get the prefix (already defined in your LEVEL2_OPTIONS)
        prefix = get_cable_prefix(cable_type)  

        # Start building the pieces list
        pieces = [prefix]

        # ───────────────────────────────────────────────
        # Branch by cable type – exactly matching your spec
        # ───────────────────────────────────────────────
        if "Single-Conductor" in cable_type:
            slash = session_state.get("cable_slash", "").strip()
            awg   = session_state.get("cable_awg_size", "").strip()
            color = session_state.get("cable_color", "").strip().upper()

            # Required field
            if not slash:
                return "Incomplete: Missing Slash Sheet Number for Single-Conductor Wire"

            pieces.append(slash)

            # Optional AWG / Size
            if awg:
                pieces.append(awg)

            # Optional Color Code
            if color:
                pieces.append(color)

        elif "Multi-Conductor" in cable_type:
            config = session_state.get("cable_config", "").strip()

            # Required field
            if not config:
                return "Incomplete: Missing Configuration Code for Multi-Conductor Cable"

            pieces.append(config)

        elif "Coaxial" in cable_type:
            slash = session_state.get("cable_slash", "").strip()

            # Required field
            if not slash:
                return "Incomplete: Missing Slash Sheet Number for Coaxial Cable"

            pieces.append(slash)

        else:
            return "Incomplete: Unrecognized cable type"

        # ───────────────────────────────────────────────
        # Common: Spool handling (same for all types)
        # ───────────────────────────────────────────────
        if spool_choice == "Yes":
            pieces.append("SPOOL")
            if length:
                pieces.append(length)

        # Final PN – uppercase everything
        pn = "-".join(pieces).upper()
        if pn.count("-") > 1 and "/-" in pn:
            pn = pn.replace("/-", "/")  # fix the double separator
        return pn

