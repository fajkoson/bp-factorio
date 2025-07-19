from src.check import Check

# fmt: off
STYLE_MAP = {
    0: ["classic", "Solarize_Light2", "dark_background", "fast", "bmh"],
    1: ["fivethirtyeight", "ggplot", "grayscale", "petroff10"],
    2: ["seaborn-v0_8", "seaborn-v0_8-deep", "seaborn-v0_8-muted", "seaborn-v0_8-bright", "seaborn-v0_8-colorblind"],
    3: ["seaborn-v0_8-white", "seaborn-v0_8-whitegrid", "seaborn-v0_8-darkgrid"],
    4: ["seaborn-v0_8-dark", "seaborn-v0_8-dark-palette", "seaborn-v0_8-ticks"],
    5: ["seaborn-v0_8-notebook", "seaborn-v0_8-paper", "seaborn-v0_8-talk","seaborn-v0_8-poster", "seaborn-v0_8-pastel"],
    6: ["tableau-colorblind10"],
    7: ["_classic_test_patch", "_mpl-gallery", "_mpl-gallery-nogrid"]
}
# fmt: on


def resolve_style(index: int) -> list[str]:
    Check.style_index_exists(index, STYLE_MAP)
    return STYLE_MAP[index]
