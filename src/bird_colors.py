""" Bird-inspired colors for Chicago eBird data viz

Approximate plumage-inspired HEX selections, design-inspired, not actually scientifically sourced.
Keeping species colors stable across charts; idea is to use graduated palettes for numeric maps.

"""

BIRD_COLORS = {
    "American Robin": "#C8602B",             # orange breast
    "House Sparrow": "#8B5E3C",             # brown plumage
    "Northern Cardinal": "#C41E3A",        # red plumage
    "Canada Goose": "#2B2B2B",             # black neck
    "Ring-billed Gull": "#9AA5AE",         # gray mantle
    "Mallard": "#2F6B3A",                  # green head
    "European Starling": "#3E7C6B",        # green iridescence
    "Black-capped Chickadee": "#B9B1A5",  # buff-gray body
    "Red-winged Blackbird": "#D62828",     # red shoulder patch
    "American Goldfinch": "#F7D117",      # yellow plumage
    "American Crow": "#4A4A55",           # dark sheen
    "Downy Woodpecker": "#D8332A",         # red nape patch
    "Song Sparrow": "#7A5A44",            # streaked brown
    "American Herring Gull": "#8FA0AD",   # gray mantle
    "Common Grackle": "#2A2F4A",          # blue-black sheen
    "House Finch": "#C23B3B",             # red face and breast
    "Chimney Swift": "#5A5650",            # sooty brown-gray
    "Double-crested Cormorant": "#E39A2D",# orange facial skin
    "White-throated Sparrow": "#E3B83A",  # yellow lores
    "Dark-eyed Junco": "#5F6770",          # slate gray
}

# All shades are borrowed from the birds above, including accent colors.
PAPER = "#F4F6F7"        # American Herring Gull white
INK = "#1F2A2E"          # Double-crested Cormorant black
SUBTLE = "#5F6770"       # Dark-eyed Junco gray

# Ordered light to dark: appropriate for numeric counts on choropleths/heatmaps.
# MAP_PALETTES = {
#     "checklists": ["#F4F6F7", "#B9B1A5", "#8B5E3C", "#5A5650", "#2B2B2B"],
#     "species_richness": ["#F4F6F7", "#B9B1A5", "#3E7C6B", "#2F6B3A", "#1F2A2E"],
#     "birds_reported": ["#F4F6F7", "#E3B83A", "#C8602B", "#C41E3A", "#2B2B2B"],
#     "monthly_activity": ["#F4F6F7", "#B9B1A5", "#8B5E3C", "#5A5650", "#2B2B2B"],
# }

MAP_PALETTES = {
    "checklists": [
    "#EEE6DE", "#D5BAA4", "#AE8465", "#805439", "#4B3225"
    ],
    "species_richness": [
        "#ECF3ED", "#B5D4BC", "#75AA8B", "#387753", "#173E2A"
    ],
    "birds_reported": [
        "#FFF1E6", "#F4C9A8", "#E9955E", "#C8602B", "#823716"
    ],
    "monthly_activity": [
    "#FFF5DD",
    "#F7D117",
    "#E39A2D",
    "#C8602B",
    "#7A2137"
],
    "observer_share": [
    "#FFF0F1", "#F1B6C0", "#DC7285", "#C41E3A", "#741127"
],

}
# ouse sparrow
# mallard
# american robin

OBSERVER_COLORS = {
    "Top observer": "#C41E3A",   # northern cardinal red
    "Everyone else": "#E9D9DD"   # soft pale pink-gray
}

TOP_OBSERVER_MAP = [
    "#FCF7F8",
    "#F3D7DE",
    "#E9A8B8",
    "#D86A84",
    "#C41E3A"
]
