"""
waste_info.py

Maps each detected waste CLASS to a PARENT CATEGORY
and provides general disposal guidance.

The three parent categories used in the project are:
1. Hazardous
2. Biodegradable
3. Non-biodegradable / Recyclable
"""


# ============================================================
# PARENT CATEGORIES
# ============================================================

HAZARDOUS = "Hazardous"
BIODEGRADABLE = "Biodegradable"
NON_BIODEGRADABLE = "Non-biodegradable / Recyclable"

ALL_PARENTS = [
    HAZARDOUS,
    BIODEGRADABLE,
    NON_BIODEGRADABLE,
]


# ============================================================
# CLASS → PARENT CATEGORY
# ============================================================

PARENT_CATEGORY = {

    # --------------------------------------------------------
    # HAZARDOUS
    # --------------------------------------------------------

    "Battery": HAZARDOUS,
    "battery": HAZARDOUS,

    "Paints": HAZARDOUS,
    "paint_chemical_container": HAZARDOUS,

    "Pesticides": HAZARDOUS,
    "pesticide": HAZARDOUS,

    "aerosol_can": HAZARDOUS,

    "ewaste_device": HAZARDOUS,
    "e_waste": HAZARDOUS,

    "medical_waste": HAZARDOUS,


    # --------------------------------------------------------
    # BIODEGRADABLE
    # --------------------------------------------------------

    "Food_waste": BIODEGRADABLE,
    "food_waste": BIODEGRADABLE,

    "Paper": BIODEGRADABLE,
    "paper": BIODEGRADABLE,

    "Cardboard": BIODEGRADABLE,
    "cardboard": BIODEGRADABLE,
    "paper_cardboard": BIODEGRADABLE,

    "Textile_trash": BIODEGRADABLE,
    "textile_trash": BIODEGRADABLE,


    # --------------------------------------------------------
    # NON-BIODEGRADABLE / RECYCLABLE
    # --------------------------------------------------------

    "Cans": NON_BIODEGRADABLE,
    "cans": NON_BIODEGRADABLE,
    "metal_can": NON_BIODEGRADABLE,

    "Glass": NON_BIODEGRADABLE,
    "glass": NON_BIODEGRADABLE,

    "Metal": NON_BIODEGRADABLE,
    "metal": NON_BIODEGRADABLE,

    "Plastic": NON_BIODEGRADABLE,
    "plastic": NON_BIODEGRADABLE,

    "Plastic_bottles": NON_BIODEGRADABLE,
    "plastic_bottle": NON_BIODEGRADABLE,

    "Plastic_bags_wrappers": NON_BIODEGRADABLE,
    "plastic_bag_wrapper": NON_BIODEGRADABLE,

    "Plastic_cup": NON_BIODEGRADABLE,
    "plastic_cup": NON_BIODEGRADABLE,

    "Plastic_straw": NON_BIODEGRADABLE,
    "plastic_straw": NON_BIODEGRADABLE,

    "Paper_straw": NON_BIODEGRADABLE,
    "paper_straw": NON_BIODEGRADABLE,

    "Ceramic_product": NON_BIODEGRADABLE,
    "ceramic_product": NON_BIODEGRADABLE,

    "Shoes": NON_BIODEGRADABLE,
    "shoes": NON_BIODEGRADABLE,

    "Styrofoam_product": NON_BIODEGRADABLE,
    "styrofoam_product": NON_BIODEGRADABLE,


    # --------------------------------------------------------
    # SANITARY WASTE
    # --------------------------------------------------------
    # The trained model is currently predicting
    # "medical_sanitary" for sanitary-pad images.
    # Keep this separate from chemical hazardous waste.

    "medical_sanitary": NON_BIODEGRADABLE,
    "Medical_sanitary": NON_BIODEGRADABLE,
    "medical_sanitary_waste": NON_BIODEGRADABLE,

    "Sanitary_napkin": NON_BIODEGRADABLE,
    "sanitary_napkin": NON_BIODEGRADABLE,

    "Diapers": NON_BIODEGRADABLE,
    "diapers": NON_BIODEGRADABLE,


    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    "cigarette_butt": NON_BIODEGRADABLE,

    "metal_scrap_foil": NON_BIODEGRADABLE,

    "plastic_other": NON_BIODEGRADABLE,

    "other_litter": NON_BIODEGRADABLE,
}


# ============================================================
# BOX COLOURS
# OpenCV uses BGR format.
# ============================================================

PARENT_COLOR_BGR = {

    HAZARDOUS: (0, 0, 255),
    BIODEGRADABLE: (0, 170, 0),
    NON_BIODEGRADABLE: (255, 128, 0),
}


# ============================================================
# HAZARDOUS-WASTE DISCLAIMER
# ============================================================

HAZARD_DISCLAIMER = (
    "This is an AI-based visual prediction from an image. "
    "The system cannot determine the exact contents, condition, "
    "or contamination of an item. Follow local waste-management "
    "rules and use an authorised waste facility where required."
)


# ============================================================
# CLASS-SPECIFIC DISPOSAL GUIDANCE
# ============================================================

GUIDANCE = {

    # --------------------------------------------------------
    # HAZARDOUS WASTE
    # --------------------------------------------------------

    "Battery": (
        "Keep batteries separate from normal household waste "
        "and take them to an authorised battery or e-waste "
        "collection point."
    ),

    "battery": (
        "Keep batteries separate from normal household waste "
        "and take them to an authorised battery or e-waste "
        "collection point."
    ),

    "Paints": (
        "Paint containers may contain residue. Keep them separate "
        "from normal household waste and follow local hazardous-waste "
        "collection rules."
    ),

    "paint_chemical_container": (
        "Containers that held paint or chemicals may contain residue. "
        "Keep them separate from normal waste and follow local "
        "hazardous-waste collection rules."
    ),

    "Pesticides": (
        "Pesticide containers may contain hazardous residues. "
        "Do not mix them with normal household waste. Follow local "
        "hazardous-waste collection requirements."
    ),

    "pesticide": (
        "Pesticide containers may contain hazardous residues. "
        "Do not mix them with normal household waste. Follow local "
        "hazardous-waste collection requirements."
    ),

    "aerosol_can": (
        "Aerosol cans may contain pressurised material. Do not puncture "
        "or burn them. Follow local hazardous-waste disposal rules."
    ),

    "ewaste_device": (
        "Electronic devices should not normally be placed in household "
        "waste. Take them to an authorised e-waste collection or "
        "recycling centre."
    ),

    "e_waste": (
        "Electronic devices should not normally be placed in household "
        "waste. Take them to an authorised e-waste collection or "
        "recycling centre."
    ),

    "medical_waste": (
        "Medical waste should be kept separate from normal household "
        "recyclables and handled according to local waste-management rules."
    ),


    # --------------------------------------------------------
    # BIODEGRADABLE
    # --------------------------------------------------------

    "Food_waste": (
        "Place food waste in the appropriate organic or wet-waste "
        "collection system. Where available, it can also be composted."
    ),

    "food_waste": (
        "Place food waste in the appropriate organic or wet-waste "
        "collection system. Where available, it can also be composted."
    ),

    "Paper": (
        "Keep paper clean and dry and place it with paper recycling "
        "where recycling facilities are available."
    ),

    "paper": (
        "Keep paper clean and dry and place it with paper recycling "
        "where recycling facilities are available."
    ),

    "Cardboard": (
        "Keep cardboard clean and dry and place it with paper/cardboard "
        "recycling where available."
    ),

    "cardboard": (
        "Keep cardboard clean and dry and place it with paper/cardboard "
        "recycling where available."
    ),

    "paper_cardboard": (
    "Keep cardboard clean and dry and place it with paper/cardboard "
    "recycling where available."
),

    "Textile_trash": (
        "Reusable textiles can be donated or sent to a suitable textile "
        "collection facility. Follow local rules for damaged textiles."
    ),

    "textile_trash": (
        "Reusable textiles can be donated or sent to a suitable textile "
        "collection facility. Follow local rules for damaged textiles."
    ),


    # --------------------------------------------------------
    # NON-BIODEGRADABLE / RECYCLABLE
    # --------------------------------------------------------

    "Cans": (
        "Empty cans and place them with metal recycling where "
        "this service is available."
    ),

    "cans": (
        "Empty cans and place them with metal recycling where "
        "this service is available."
    ),

    "metal_can": (
    "Empty cans and place them with metal recycling where "
    "this service is available."
),

    "Glass": (
        "Place suitable glass items in a glass-recycling collection "
        "where available. Handle broken glass carefully."
    ),

    "glass": (
        "Place suitable glass items in a glass-recycling collection "
        "where available. Handle broken glass carefully."
    ),

    "Metal": (
        "Place suitable metal items with metal recycling where "
        "local recycling facilities accept them."
    ),

    "metal": (
        "Place suitable metal items with metal recycling where "
        "local recycling facilities accept them."
    ),

    "Plastic": (
        "Place clean and suitable plastic items in the appropriate "
        "plastic or dry-waste collection according to local rules."
    ),

    "plastic": (
        "Place clean and suitable plastic items in the appropriate "
        "plastic or dry-waste collection according to local rules."
    ),

    "Plastic_bottles": (
        "Empty and rinse plastic bottles and place them with plastic "
        "recycling if accepted by the local recycling system."
    ),

    "plastic_bottle": (
        "Empty and rinse plastic bottles and place them with plastic "
        "recycling if accepted by the local recycling system."
    ),

    "Plastic_bags_wrappers": (
        "Plastic bags and wrappers are often not accepted in normal "
        "recycling. Follow local rules for plastic-film or dry-waste "
        "collection."
    ),

    "plastic_bag_wrapper": (
        "Plastic bags and wrappers are often not accepted in normal "
        "recycling. Follow local rules for plastic-film or dry-waste "
        "collection."
    ),

    "Plastic_cup": (
        "Dispose of plastic cups according to local dry-waste or "
        "plastic-recycling rules."
    ),

    "plastic_cup": (
        "Dispose of plastic cups according to local dry-waste or "
        "plastic-recycling rules."
    ),

    "Plastic_straw": (
        "Plastic straws are usually difficult to recycle. Place them "
        "in the appropriate dry-waste collection."
    ),

    "plastic_straw": (
        "Plastic straws are usually difficult to recycle. Place them "
        "in the appropriate dry-waste collection."
    ),

    "Paper_straw": (
        "If clean and dry, paper straws can generally be placed with "
        "appropriate paper waste where accepted."
    ),

    "paper_straw": (
        "If clean and dry, paper straws can generally be placed with "
        "appropriate paper waste where accepted."
    ),

    "Ceramic_product": (
        "Ceramic items are generally not accepted in regular glass "
        "recycling. Follow local rules for broken or unwanted ceramics."
    ),

    "ceramic_product": (
        "Ceramic items are generally not accepted in regular glass "
        "recycling. Follow local rules for broken or unwanted ceramics."
    ),

    "Shoes": (
        "Reusable shoes can be donated or taken to a suitable textile "
        "or reuse collection facility."
    ),

    "shoes": (
        "Reusable shoes can be donated or taken to a suitable textile "
        "or reuse collection facility."
    ),

    "Styrofoam_product": (
        "Styrofoam is often not accepted in normal recycling. "
        "Follow local dry-waste or special collection rules."
    ),

    "styrofoam_product": (
        "Styrofoam is often not accepted in normal recycling. "
        "Follow local dry-waste or special collection rules."
    ),


    # --------------------------------------------------------
    # SANITARY WASTE
    # --------------------------------------------------------

    "medical_sanitary": (
        "Wrap the used sanitary item securely in paper or its "
        "original wrapper. Place it in a designated sanitary-waste "
        "or general-waste bin according to local rules. "
        "Do not place used sanitary items in recycling or compost bins."
    ),

    "Medical_sanitary": (
        "Wrap the used sanitary item securely in paper or its "
        "original wrapper. Place it in a designated sanitary-waste "
        "or general-waste bin according to local rules. "
        "Do not place used sanitary items in recycling or compost bins."
    ),

    "medical_sanitary_waste": (
        "Wrap the used sanitary item securely in paper or its "
        "original wrapper. Place it in a designated sanitary-waste "
        "or general-waste bin according to local rules. "
        "Do not place used sanitary items in recycling or compost bins."
    ),

    "Sanitary_napkin": (
        "Wrap the used sanitary napkin securely in paper or its "
        "original wrapper. Place it in a designated sanitary-waste "
        "or general-waste bin according to local rules. "
        "Do not place used sanitary napkins in recycling or compost bins."
    ),

    "sanitary_napkin": (
        "Wrap the used sanitary napkin securely in paper or its "
        "original wrapper. Place it in a designated sanitary-waste "
        "or general-waste bin according to local rules. "
        "Do not place used sanitary napkins in recycling or compost bins."
    ),

    "Diapers": (
        "Wrap the used diaper securely and place it in a designated "
        "sanitary-waste or general-waste bin according to local rules. "
        "Do not place used diapers in recycling or compost bins."
    ),

    "diapers": (
        "Wrap the used diaper securely and place it in a designated "
        "sanitary-waste or general-waste bin according to local rules. "
        "Do not place used diapers in recycling or compost bins."
    ),


    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    "cigarette_butt": (
        "Place cigarette butts in a suitable waste bin. "
        "Do not throw them on the ground or into drains."
    ),

    "metal_scrap_foil": (
        "Collect suitable metal foil and scrap separately for metal "
        "recycling where accepted by the local system."
    ),

    "plastic_other": (
        "Unidentified plastic items should generally be placed in "
        "the appropriate dry-waste collection according to local rules."
    ),

    "other_litter": (
        "For mixed or unidentified litter, use the appropriate "
        "dry-waste collection. Reusable items may be separated for reuse."
    ),
}


# ============================================================
# DEFAULT GUIDANCE
# ============================================================

DEFAULT_GUIDANCE = (
    "No specific guidance is available for this class. "
    "Please follow your local waste-management rules."
)


# ============================================================
# FUNCTIONS
# ============================================================

def get_parent(class_name):
    """
    Return the parent category for a detected waste class.
    Returns 'Unknown' if the class is not defined.
    """
    return PARENT_CATEGORY.get(
        class_name,
        "Unknown"
    )


def get_guidance(class_name):
    """
    Return disposal guidance for a detected waste class.
    """
    return GUIDANCE.get(
        class_name,
        DEFAULT_GUIDANCE
    )
