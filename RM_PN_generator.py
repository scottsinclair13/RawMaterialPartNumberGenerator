"""
Raw Material Part Number Generator (stable GUI, testable core)
=============================================================

Fixes in this version:
- Dropdowns are visible (explicit ttk combobox styling for dark UI)
- Scrollable left panel correctly resizes (no clipped content)
- All dropdowns start empty (no auto-selection)
- Full-text dropdown labels; PN uses abbreviations via ABBREV_MAP
  - If missing abbreviation: fall back to sanitized full text
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from typing import Dict, List

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("rm_pn_gen")


# -----------------------------
# Data structures
# -----------------------------
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


# -----------------------------
# Abbrev mapping (FULL TEXT -> PN TOKEN)
# -----------------------------
ABBREV_MAP: Dict[str, str] = {
    #Metal conditions
    "Annealed": "ANN",
    "Normalized": "NORM",
    "Q&T": "QT",
    "STA": "STA",
    "Condition B": "B",
    "1/4 hard": "1/4H",
    "1/2 hard": "1/2H",
    "3/4 hard": "3/4H",
    "Full hard": "FH",

    #Colors 
    "Black": "BLK",
    "Natural": "NAT",
    "Blue": "BLU",
    "Grey": "GRY",

    #Alloys/Grades
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
    """Map label to abbreviation; if missing, fall back to sanitized label."""
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


# -----------------------------
# Dropdown lists (FULL TEXT)
# -----------------------------
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


# -----------------------------
# Pure functions (testable)
# -----------------------------
def normalize_form_code(form_label: str) -> str:
    return FORM_ABBREVIATIONS.get(form_label, pn_token(form_label)[:8])


def _format_number(value_str: str, integer_only: bool = False) -> str:
    s = value_str.strip()
    if not s:
        raise ValueError("Empty number")
    if integer_only:
        v = int(s)
        if v <= 0:
            raise ValueError("Must be > 0")
        return str(v)

    v = float(s)
    if v <= 0:
        raise ValueError("Must be > 0")
    return str(int(v)) if v == int(v) else f"{v:g}"


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
        if cond:
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


# -----------------------------
# GUI
# -----------------------------
class RawMaterialPNApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Raw Material PN Generator")
        self.geometry("1100x900")
        self.minsize(1100, 900)
        self.configure(bg="#0b0f14")

        self.selections: Dict[str, object] = {}
        self.frames: Dict[str, ttk.Frame] = {}

        self._setup_theme()
        self._build_layout()
        self._build_category_step()

    def _setup_theme(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # --- Color palette (Dark vibes) ---
        self.COL_BG     = "#070b12"   # window background (very dark)
        self.COL_PANEL  = "#0d1626"   # panel background (navy)
        self.COL_PANEL2 = "#0b1220"   # slightly different navy for depth
        self.COL_TEXT   = "#e6edf3"   # primary text
        self.COL_MUTED  = "#9aa4b2"   # secondary text
        self.COL_ACCENT = "#00d1ff"   # cyan accent

        # IMPORTANT: light input fields (combobox/entry) like your screenshot
        self.COL_FIELD_BG  = "#e6e6e6"  # light field background
        self.COL_FIELD_FG  = "#0a0f18"  # dark field text

        # Apply window background
        self.configure(bg=self.COL_BG)

        # --- ttk base widget styles ---
        style.configure("TFrame", background=self.COL_BG)
        style.configure("Panel.TFrame", background=self.COL_PANEL)

        style.configure(
            "TLabel",
            background=self.COL_BG,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 12),
        )
        style.configure(
            "Header.TLabel",
            background=self.COL_BG,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "SubHeader.TLabel",
            background=self.COL_BG,
            foreground=self.COL_MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "PanelLabel.TLabel",
            background=self.COL_PANEL,
            foreground=self.COL_TEXT,
            font=("Segoe UI", 12),
        )

        # Buttons: neutral gray like screenshot
        style.configure(
            "TButton",
            padding=10,
            background="#cfcfcf",
            foreground="#0a0f18",
            borderwidth=0,
            focusthickness=2,
            focuscolor=self.COL_ACCENT,
            font=("Segoe UI", 12),
        )
        style.map(
            "TButton",
            background=[("active", "#e0e0e0"), ("disabled", "#cfcfcf")],
            foreground=[("disabled", "#8a8a8a")],
        )

        # If you have an Accent button style, keep it subtle (optional)
        style.configure(
            "Accent.TButton",
            padding=10,
            background="#cfcfcf",
            foreground="#0a0f18",
            font=("Segoe UI", 14, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#e0e0e0"), ("disabled", "#cfcfcf")],
            foreground=[("disabled", "#8a8a8a")],
        )

        # Combobox: LIGHT field background like screenshot
        style.configure(
            "TCombobox",
            padding=6,
            fieldbackground=self.COL_FIELD_BG,
            background=self.COL_FIELD_BG,
            foreground=self.COL_FIELD_FG,
            arrowcolor="#0a0f18",
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.COL_FIELD_BG)],
            foreground=[("readonly", self.COL_FIELD_FG)],
            selectbackground=[("readonly", self.COL_FIELD_BG)],
            selectforeground=[("readonly", self.COL_FIELD_FG)],
        )

        # Entry: LIGHT field background like screenshot
        style.configure(
            "TEntry",
            padding=6,
            fieldbackground=self.COL_FIELD_BG,
            foreground=self.COL_FIELD_FG,
        )

    def _build_layout(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=18, pady=(16, 8))
        ttk.Label(header, text="Raw Material Part Number Generator", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header, text="Consistency built-in • Confusion built-out", style="SubHeader.TLabel").pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=18, pady=12)

        # LEFT (scrollable)
        left_outer = ttk.Frame(body, style="Panel.TFrame")
        left_outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_outer.configure(padding=8)

        self.left_canvas = tk.Canvas(left_outer, bg=self.COL_PANEL, highlightthickness=0)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = ttk.Scrollbar(left_outer, orient="vertical", command=self.left_canvas.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_canvas.configure(yscrollcommand=scroll.set)

        self.step_container = ttk.Frame(self.left_canvas, style="Panel.TFrame")
        self.step_container.configure(padding=16)

        self.step_window_id = self.left_canvas.create_window((0, 0), window=self.step_container, anchor="nw")

        # FIX #1: scrollregion updates when content size changes
        def on_frame_configure(_evt):
            self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

        self.step_container.bind("<Configure>", on_frame_configure)

        # FIX #2: resize inner window to canvas width so content is not clipped
        def on_canvas_configure(evt):
            self.left_canvas.itemconfigure(self.step_window_id, width=evt.width)

        self.left_canvas.bind("<Configure>", on_canvas_configure)

        # RIGHT (output)
        self.right = ttk.Frame(body, style="Panel.TFrame")
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self.right.configure(padding=16, width=360)

        ttk.Label(self.right, text="Output", style="PanelLabel.TLabel").pack(anchor="w")

        self.output = tk.Text(
            self.right,
            height=28,
            font=("Consolas", 14),
            bg=self.COL_PANEL2,
            fg=self.COL_TEXT,
            insertbackground=self.COL_ACCENT,
            relief="flat",
            wrap="word",
        )
        self.output.tag_configure("pn", font=("Consolas", 16, "bold"))

        self.output.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        self._set_output("Select options on the left.\n\nGenerated PN will appear here.")

        self.copy_btn = ttk.Button(self.right, text="Copy PN", command=self._copy, state="disabled")
        self.copy_btn.pack(fill=tk.X)

        self.warn_label = ttk.Label(self.right, text="", style="PanelLabel.TLabel")
        self.warn_label.pack(anchor="w", pady=(12, 0))

        self.pn_latest = ""

    def _set_output(self, text: str) -> None:
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", text)
        self.output.config(state="disabled")

    def _destroy_steps_after(self, step_name: str) -> None:
        order = [
            "category",
            "metal_material", "metal_alloy", "metal_condition",
            "phen_material",
            "plastic_family", "plastic_grade", "plastic_variant",
            "cable_material", "cable_construction",
            "spec", "form", "dims", "generate",
        ]
        if step_name not in order:
            return
        idx = order.index(step_name)
        for s in order[idx + 1:]:
            fr = self.frames.pop(s, None)
            if fr is not None:
                fr.destroy()

        self.pn_latest = ""
        self.copy_btn.config(state="disabled")
        self.warn_label.config(text="")
        self._set_output("Select options on the left.\n\nGenerated PN will appear here.")

    # -----------------------
    # Step 1: Category (EMPTY start)
    # -----------------------
    def _build_category_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["category"] = fr

        ttk.Label(fr, text="1) Category", style="PanelLabel.TLabel").pack(anchor="w")

        self.category_cb = ttk.Combobox(fr, state="readonly", values=["Metals", "Phenolics", "Plastics", "Electrical Cable"])
        self.category_cb.pack(fill=tk.X, pady=(8, 0))
        self.category_cb.bind("<<ComboboxSelected>>", self._on_category)
        # start empty: no set(), no auto-call

    def _on_category(self, _event) -> None:
        cat = self.category_cb.get().strip()
        if not cat:
            return

        self.selections = {"category": cat}
        self._destroy_steps_after("category")

        if cat == "Metals":
            self._build_metal_material_step()
        elif cat == "Phenolics":
            self._build_phenolic_material_step()
        elif cat == "Plastics":
            self._build_plastic_family_step()
        elif cat == "Electrical Cable":
            self._build_cable_material_step()

    # -----------------------
    # Metals
    # -----------------------
    def _build_metal_material_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["metal_material"] = fr

        ttk.Label(fr, text="2) Metal Material", style="PanelLabel.TLabel").pack(anchor="w")
        mats = [m.material.label for m in METALS] + ["Other"]
        self.metal_material_cb = ttk.Combobox(fr, state="readonly", values=mats)
        self.metal_material_cb.pack(fill=tk.X, pady=(8, 0))
        self.metal_material_cb.bind("<<ComboboxSelected>>", self._on_metal_material)

    def _on_metal_material(self, _event) -> None:
        self._destroy_steps_after("metal_material")
        mat = self.metal_material_cb.get().strip()
        if not mat:
            return

        if mat == "Other":
            txt = simpledialog.askstring("Custom metal", "Enter metal material name:")
            self.selections["material"] = (txt or "Other").strip()
        else:
            self.selections["material"] = mat

        self._build_metal_alloy_step()

    def _build_metal_alloy_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["metal_alloy"] = fr

        ttk.Label(fr, text="3) Alloy / Grade", style="PanelLabel.TLabel").pack(anchor="w")

        mat = str(self.selections.get("material", ""))
        alloys = []
        for m in METALS:
            if m.material.label == mat:
                alloys = list(m.alloys_to_conditions.keys())
                break
        alloys = alloys + ["Other"]

        self.metal_alloy_cb = ttk.Combobox(fr, state="readonly", values=alloys)
        self.metal_alloy_cb.pack(fill=tk.X, pady=(8, 0))
        self.metal_alloy_cb.bind("<<ComboboxSelected>>", self._on_metal_alloy)

    def _on_metal_alloy(self, _event) -> None:
        self._destroy_steps_after("metal_alloy")
        alloy = self.metal_alloy_cb.get().strip()
        if not alloy:
            return

        if alloy == "Other":
            txt = simpledialog.askstring("Custom alloy", "Enter alloy / grade:")
            self.selections["alloy"] = (txt or "Other").strip()
        else:
            self.selections["alloy"] = alloy

        self._build_metal_condition_step()

    def _build_metal_condition_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["metal_condition"] = fr

        ttk.Label(fr, text="4) Condition / Temper (optional)", style="PanelLabel.TLabel").pack(anchor="w")

        mat = str(self.selections.get("material", ""))
        alloy = str(self.selections.get("alloy", ""))

        conds = []
        for m in METALS:
            if m.material.label == mat:
                conds = m.alloys_to_conditions.get(alloy, [])
                break

        values = ["None / Not Applicable"] + conds + ["Other"]
        self.metal_cond_cb = ttk.Combobox(fr, state="readonly", values=values)
        self.metal_cond_cb.pack(fill=tk.X, pady=(8, 0))
        self.metal_cond_cb.bind("<<ComboboxSelected>>", self._on_metal_condition)

    def _on_metal_condition(self, _event) -> None:
        self._destroy_steps_after("metal_condition")
        v = self.metal_cond_cb.get().strip()
        if not v:
            return

        if v == "None / Not Applicable":
            self.selections.pop("condition", None)
        elif v == "Other":
            txt = simpledialog.askstring("Custom condition", "Enter condition/temper:")
            if txt:
                self.selections["condition"] = txt.strip()
        else:
            self.selections["condition"] = v

        self._build_spec_step()

    # -----------------------
    # Phenolics
    # -----------------------
    def _build_phenolic_material_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["phen_material"] = fr

        ttk.Label(fr, text="2) Phenolic Type", style="PanelLabel.TLabel").pack(anchor="w")

        mats = [p.label for p in PHENOLICS]
        self.phen_cb = ttk.Combobox(fr, state="readonly", values=mats)
        self.phen_cb.pack(fill=tk.X, pady=(8, 0))
        self.phen_cb.bind("<<ComboboxSelected>>", self._on_phenolic)

    def _on_phenolic(self, _event) -> None:
        self._destroy_steps_after("phen_material")
        v = self.phen_cb.get().strip()
        if not v:
            return

        self.selections["material"] = v
        self.selections.pop("custom_material_text", None)

        if v == "Other":
            txt = simpledialog.askstring("Custom phenolic", "Enter phenolic name/type:")
            if txt:
                self.selections["custom_material_text"] = txt.strip()

        self._build_spec_step()

    # -----------------------
    # Plastics
    # -----------------------
    def _build_plastic_family_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["plastic_family"] = fr

        ttk.Label(fr, text="2) Plastic Family", style="PanelLabel.TLabel").pack(anchor="w")

        fams = [p.material.label for p in PLASTICS]
        self.pl_family_cb = ttk.Combobox(fr, state="readonly", values=fams)
        self.pl_family_cb.pack(fill=tk.X, pady=(8, 0))
        self.pl_family_cb.bind("<<ComboboxSelected>>", self._on_plastic_family)

    def _on_plastic_family(self, _event) -> None:
        self._destroy_steps_after("plastic_family")
        fam = self.pl_family_cb.get().strip()
        if not fam:
            return

        self.selections["plastic_family"] = fam
        self._build_plastic_grade_step()

    def _build_plastic_grade_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["plastic_grade"] = fr

        ttk.Label(fr, text="3) Grade (optional)", style="PanelLabel.TLabel").pack(anchor="w")

        fam = str(self.selections.get("plastic_family", ""))
        grades = []
        for p in PLASTICS:
            if p.material.label == fam:
                grades = list(p.grades.keys())
                break
        values = ["None / Not Applicable"] + grades

        self.pl_grade_cb = ttk.Combobox(fr, state="readonly", values=values)
        self.pl_grade_cb.pack(fill=tk.X, pady=(8, 0))
        self.pl_grade_cb.bind("<<ComboboxSelected>>", self._on_plastic_grade)

    def _on_plastic_grade(self, _event) -> None:
        self._destroy_steps_after("plastic_grade")
        g = self.pl_grade_cb.get().strip()
        if not g:
            return

        self.selections.pop("custom_grade_text", None)

        if g == "None / Not Applicable":
            self.selections.pop("plastic_grade", None)
        else:
            self.selections["plastic_grade"] = g
            if g == "Other":
                txt = simpledialog.askstring("Custom plastic grade", "Enter custom grade:")
                if txt:
                    self.selections["custom_grade_text"] = txt.strip()

        self._build_plastic_variant_step()

    def _build_plastic_variant_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["plastic_variant"] = fr

        ttk.Label(fr, text="4) Variant / Color (optional)", style="PanelLabel.TLabel").pack(anchor="w")

        fam = str(self.selections.get("plastic_family", ""))
        grade = str(self.selections.get("plastic_grade", ""))
        variants: List[str] = []
        for p in PLASTICS:
            if p.material.label == fam:
                variants = p.grades.get(grade, [])
                break
        values = ["None / Not Applicable"] + variants

        self.pl_var_cb = ttk.Combobox(fr, state="readonly", values=values)
        self.pl_var_cb.pack(fill=tk.X, pady=(8, 0))
        self.pl_var_cb.bind("<<ComboboxSelected>>", self._on_plastic_variant)

    def _on_plastic_variant(self, _event) -> None:
        self._destroy_steps_after("plastic_variant")
        v = self.pl_var_cb.get().strip()
        if not v:
            return

        if v == "None / Not Applicable":
            self.selections.pop("plastic_variant", None)
        else:
            self.selections["plastic_variant"] = v

        self._build_spec_step()

    # -----------------------
    # Cable
    # -----------------------
    def _build_cable_material_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["cable_material"] = fr

        ttk.Label(fr, text="2) Cable Type", style="PanelLabel.TLabel").pack(anchor="w")

        mats = [c.label for c in CABLES]
        self.cable_cb = ttk.Combobox(fr, state="readonly", values=mats)
        self.cable_cb.pack(fill=tk.X, pady=(8, 0))
        self.cable_cb.bind("<<ComboboxSelected>>", self._on_cable_material)

    def _on_cable_material(self, _event) -> None:
        self._destroy_steps_after("cable_material")
        v = self.cable_cb.get().strip()
        if not v:
            return

        self.selections["material"] = v
        self._build_cable_construction_step()

    def _build_cable_construction_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["cable_construction"] = fr

        ttk.Label(fr, text="3) Construction / Jacket (optional)", style="PanelLabel.TLabel").pack(anchor="w")
        ttk.Label(fr, text="Example: PTFE, PVC, RG316", style="SubHeader.TLabel").pack(anchor="w", pady=(4, 0))

        self.cable_ent = ttk.Entry(fr)
        self.cable_ent.pack(fill=tk.X, pady=(8, 0))
        self.cable_ent.bind("<KeyRelease>", self._on_cable_construction_change)

        self._build_spec_step()

    def _on_cable_construction_change(self, _event) -> None:
        txt = self.cable_ent.get().strip()
        if txt:
            self.selections["cable_construction"] = txt
        else:
            self.selections.pop("cable_construction", None)

    # -----------------------
    # Shared: Spec / Form / Dims / Generate
    # -----------------------
    def _build_spec_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["spec"] = fr

        ttk.Label(fr, text="(Optional) Material Specification", style="PanelLabel.TLabel").pack(anchor="w")

        specs = self._spec_options()
        values = ["None / Not Applicable"] + specs + ["Other"]

        self.spec_cb = ttk.Combobox(fr, state="readonly", values=values)
        self.spec_cb.pack(fill=tk.X, pady=(8, 0))
        self.spec_cb.bind("<<ComboboxSelected>>", self._on_spec)

    def _spec_options(self) -> List[str]:
        cat = str(self.selections.get("category", ""))
        if cat == "Metals":
            mat = str(self.selections.get("material", ""))
            alloy = str(self.selections.get("alloy", ""))
            d = COMMON_PROCSPECS.get(mat, {})
            return d.get(alloy, []) if isinstance(d, dict) else []
        if cat == "Phenolics":
            mat = str(self.selections.get("material", ""))
            d = COMMON_PROCSPECS.get("Phenolic", {})
            return d.get(mat, []) if isinstance(d, dict) else []
        if cat == "Electrical Cable":
            mat = str(self.selections.get("material", ""))
            lst = COMMON_PROCSPECS.get(mat, [])
            return lst if isinstance(lst, list) else []
        return []

    def _on_spec(self, _event) -> None:
        self._destroy_steps_after("spec")
        v = self.spec_cb.get().strip()
        if not v:
            return

        if v == "None / Not Applicable":
            self.selections.pop("specification", None)
        elif v == "Other":
            txt = simpledialog.askstring("Custom spec", "Enter spec (AMS/ASTM/MIL/etc):")
            if txt:
                self.selections["specification"] = txt.strip()
        else:
            self.selections["specification"] = v

        self._build_form_step()

    def _build_form_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["form"] = fr

        ttk.Label(fr, text="Form", style="PanelLabel.TLabel").pack(anchor="w")

        cat = str(self.selections.get("category", ""))
        forms = COMMON_FORMS if cat in ("Metals", "Phenolics", "Plastics") else CABLE_FORMS

        self.form_cb = ttk.Combobox(fr, state="readonly", values=forms)
        self.form_cb.pack(fill=tk.X, pady=(8, 0))
        self.form_cb.bind("<<ComboboxSelected>>", self._on_form)

    def _on_form(self, _event) -> None:
        self._destroy_steps_after("form")
        f = self.form_cb.get().strip()
        if not f:
            return

        if f == "Other":
            txt = simpledialog.askstring("Custom form", "Enter custom form:")
            f = (txt or "Other").strip()

        self.selections["form"] = f
        self._build_dims_step()

    def _build_dims_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["dims"] = fr

        ttk.Label(fr, text="Dimensions", style="PanelLabel.TLabel").pack(anchor="w")

        cat = str(self.selections.get("category", ""))
        form = str(self.selections.get("form", ""))
        needed = infer_needed_dimension_keys(cat, form)

        self.dim_entries: Dict[str, ttk.Entry] = {}

        if not needed:
            ttk.Label(fr, text="No dimensions required for this selection.", style="SubHeader.TLabel").pack(anchor="w", pady=(6, 0))
            self._build_generate_step()
            return

        grid = ttk.Frame(fr, style="Panel.TFrame")
        grid.pack(fill=tk.X, pady=(10, 8))
        grid.columnconfigure(1, weight=1)

        def row(r: int, label: str, key: str, hint: str) -> None:
            ttk.Label(grid, text=label, style="PanelLabel.TLabel").grid(row=r, column=0, sticky="w", padx=(0, 10), pady=6)
            e = ttk.Entry(grid)
            e.grid(row=r, column=1, sticky="ew", pady=6)
            ttk.Label(grid, text=hint, style="SubHeader.TLabel").grid(row=r, column=2, sticky="w", padx=(10, 0), pady=6)
            self.dim_entries[key] = e

        r = 0
        if needed == ["thick", "width"]:
            row(r, "Thickness (in)", "thick", "e.g. 0.125"); r += 1
            row(r, "Width (in)", "width", "e.g. 6"); r += 1
        elif needed == ["dia"]:
            row(r, "Diameter (in)", "dia", "e.g. 1"); r += 1
        elif needed == ["od", "wall"]:
            row(r, "OD (in)", "od", "e.g. 1"); r += 1
            row(r, "Wall (in)", "wall", "e.g. 0.065"); r += 1
        elif needed == ["gauge"]:
            row(r, "Wire Gauge (AWG)", "gauge", "e.g. 22"); r += 1

        ttk.Button(fr, text="Confirm Dimensions", command=self._confirm_dims).pack(fill=tk.X, pady=(6, 0))

    def _confirm_dims(self) -> None:
        cat = str(self.selections.get("category", ""))
        form = str(self.selections.get("form", ""))
        needed = infer_needed_dimension_keys(cat, form)

        dims: Dict[str, str] = {}
        try:
            for k in needed:
                raw = self.dim_entries[k].get()
                if k == "gauge":
                    dims[k] = _format_number(raw, integer_only=True)
                else:
                    dims[k] = _format_number(raw, integer_only=False)
        except Exception:
            messagebox.showerror("Invalid dimensions", "All dimension fields must be valid positive numbers.")
            return

        self.selections["dimensions"] = dims
        self._destroy_steps_after("dims")
        self._build_generate_step()

    def _build_generate_step(self) -> None:
        fr = ttk.Frame(self.step_container, style="Panel.TFrame")
        fr.pack(fill=tk.X, pady=(0, 12))
        self.frames["generate"] = fr

        ttk.Button(fr, text="Generate Part Number", style="Accent.TButton", command=self._generate).pack(fill=tk.X, pady=(6, 6))
        ttk.Button(fr, text="Debug: print selections", command=lambda: log.info("Selections: %s", self.selections)).pack(fill=tk.X)

    def _generate(self) -> None:
        try:
            res = build_part_number(self.selections)
        except Exception as e:
            messagebox.showerror("Cannot generate", str(e))
            return

        self.pn_latest = res.pn
        self.copy_btn.config(state="normal")
        #self._set_output(f"Generated Part Number:\n\n{res.pn}\n\nDefault UOM:\n{res.uom}")
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)

        self.output.insert(tk.END, "Generated Part Number:\n\n")
        self.output.insert(tk.END, res.pn + "\n", "pn")  # <-- apply tag to PN only
        self.output.insert(tk.END, "\nDefault UOM:\n")
        self.output.insert(tk.END, res.uom)

        self.output.config(state="disabled")
        
        self.warn_label.config(text=("Warnings:\n- " + "\n- ".join(res.warnings)) if res.warnings else "")

    def _copy(self) -> None:
        if not self.pn_latest:
            return
        self.clipboard_clear()
        self.clipboard_append(self.pn_latest)
        messagebox.showinfo("Copied", "Part number copied to clipboard.")


def main() -> None:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    app = RawMaterialPNApp()
    app.mainloop()


if __name__ == "__main__":
    main()