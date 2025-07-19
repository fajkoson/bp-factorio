from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from configparser import ConfigParser


def extract_plot_config(config: ConfigParser) -> dict:
    section = config["plot"]
    return {
        "style": section.get("style", "default"),
        "figsize": tuple(map(int, section.get("figsize", "5x3").lower().split("x"))),
        "dpi": section.getint("dpi", fallback=100),
        "figure_facecolor": section.get("figure_facecolor", fallback="white"),
        "axes_facecolor": section.get("axes_facecolor", fallback="white"),
        "bar_color": section.get("bar_color", fallback="skyblue"),
        "box_color": section.get("box_color", fallback="orange"),
        "show_grid": section.getboolean("show_grid", fallback=True),
        "label_font": section.get("label_font", fallback="monospace"),
        "label_font_size": section.getint("label_font_size", fallback=10),
        "label_font_color": section.get("label_font_color", fallback="white"),
        "axis_color": section.get("axis_color", fallback="white"),
        "spine_color": section.get("spine_color", fallback="white"),
        "spine_width": section.getint("spine_width", fallback=1),
    }


def plot_combined_boxplot(csv_path: Path, output_path: Path, cfg: dict) -> None:

    df = pd.read_csv(csv_path)
    map_names = df["map_name"].unique()
    data = [df[df["map_name"] == name]["effective_ups"].tolist() for name in map_names]

    plt.style.use(cfg["style"])
    fig, ax = plt.subplots(
        figsize=cfg["figsize"], dpi=cfg["dpi"], facecolor=cfg["figure_facecolor"]
    )
    ax.set_facecolor(cfg["axes_facecolor"])

    for spine in ax.spines.values():
        spine.set_color(cfg["spine_color"])
        spine.set_linewidth(cfg["spine_width"])
    ax.tick_params(axis="both", colors=cfg["axis_color"])

    # adjust here how the candle should look like
    ax.boxplot(
        data,
        patch_artist=True,
        notch=False,
        widths=0.5,
        whis=1.5,
        showmeans=True,
        meanprops=dict(marker="D", markerfacecolor="yellow", markeredgecolor="black"),
        boxprops=dict(facecolor=cfg["box_color"], color=cfg["box_color"]),
        whiskerprops=dict(color=cfg["box_color"]),
        capprops=dict(color=cfg["box_color"]),
        medianprops=dict(color=cfg["box_color"]),
        flierprops=dict(marker="o", color="red", markersize=6, linestyle="none"),
    )

    ax.set_title("UPS Distribution per Map", color=cfg["label_font_color"])
    ax.set_ylabel("Effective UPS", color=cfg["label_font_color"])

    # candle start from 1 not 0, so we need to move the text
    ax.set_xticks([i + 1 for i in range(len(map_names))])
    ax.set_xticklabels(
        [Path(name).stem for name in map_names],
        rotation=45,
        ha="right",
        fontdict={
            "family": cfg["label_font"],
            "fontsize": cfg["label_font_size"],
            "color": cfg["label_font_color"],
        },
    )

    if cfg["show_grid"]:
        ax.grid(True, axis="y")

    plt.tight_layout()
    plt.savefig(output_path / "ups_candlesticks.png")
    plt.close()


def plot_avg_ups_bar(csv_path: Path, output_path: Path, cfg: dict) -> None:
    df = pd.read_csv(csv_path)
    avg_ups = df.groupby("map_name")["effective_ups"].mean().reset_index()
    avg_ups["map_name"] = avg_ups["map_name"].apply(lambda x: Path(x).stem)

    plt.style.use(cfg["style"])
    fig, ax = plt.subplots(
        figsize=cfg["figsize"], dpi=cfg["dpi"], facecolor=cfg["figure_facecolor"]
    )
    ax.set_facecolor(cfg["axes_facecolor"])

    for spine in ax.spines.values():
        spine.set_color(cfg["spine_color"])
        spine.set_linewidth(cfg["spine_width"])
    ax.tick_params(axis="both", colors=cfg["axis_color"])

    bars = ax.bar(
        avg_ups["map_name"],
        avg_ups["effective_ups"],
        color=cfg["bar_color"],
        width=0.4,
    )
    # Increase vertical headroom by 15%
    max_val = max([bar.get_height() for bar in bars])
    ax.set_ylim(top=max_val * 1.15)

    ax.set_title("Average UPS per Map", color=cfg["label_font_color"])
    ax.set_ylabel("Average Effective UPS", color=cfg["label_font_color"])

    ax.set_xticks(range(len(avg_ups["map_name"])))
    ax.set_xticklabels(
        avg_ups["map_name"],
        rotation=45,
        ha="right",
        fontdict={
            "family": cfg["label_font"],
            "fontsize": cfg["label_font_size"],
            "color": cfg["label_font_color"],
        },
    )

    if cfg["show_grid"]:
        ax.grid(True, axis="y")

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=cfg["label_font_size"],
            color=cfg["label_font_color"],
            fontname=cfg["label_font"],
        )

    plt.tight_layout()
    plt.savefig(output_path / "ups_avg_bar.png")
    plt.close()


def plot_avg_ups_horizontal(csv_path: Path, output_path: Path, cfg: dict) -> None:
    df = pd.read_csv(csv_path)
    avg_ups = df.groupby("map_name")["effective_ups"].mean().reset_index()
    avg_ups["map_name"] = avg_ups["map_name"].apply(lambda x: Path(x).stem)
    avg_ups.sort_values(by="effective_ups", ascending=False, inplace=True)

    plt.style.use(cfg["style"])
    fig, ax = plt.subplots(
        figsize=cfg["figsize"], dpi=cfg["dpi"], facecolor=cfg["figure_facecolor"]
    )
    ax.set_facecolor(cfg["axes_facecolor"])

    # Apply axis & spine styling
    for spine in ax.spines.values():
        spine.set_color(cfg["spine_color"])
        spine.set_linewidth(cfg["spine_width"])
    ax.tick_params(axis="both", colors=cfg["axis_color"])

    bars = ax.barh(
        avg_ups["map_name"],
        avg_ups["effective_ups"],
        color=cfg["bar_color"],
        height=0.5,
    )

    # Annotate each bar with its value
    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f"{int(width)}",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            fontsize=cfg["label_font_size"],
            color=cfg["label_font_color"],
            fontname=cfg["label_font"],
        )

    # Set title and labels
    ax.set_title(
        "Average UPS per Map",
        color=cfg["label_font_color"],
        fontsize=cfg["label_font_size"] + 2,
    )
    ax.set_xlabel(
        "Average Effective UPS (Higher is better)",
        color=cfg["label_font_color"],
        fontsize=cfg["label_font_size"] + 2,
    )
    ax.set_ylabel(
        "Control strategy",
        color=cfg["label_font_color"],
        fontsize=cfg["label_font_size"] + 2,
    )

    # Set axis tick font
    ax.set_yticks(range(len(avg_ups["map_name"])))
    ax.set_yticklabels(
        avg_ups["map_name"],
        fontdict={
            "family": cfg["label_font"],
            "fontsize": cfg["label_font_size"],
            "color": cfg["label_font_color"],
        },
    )

    if cfg["show_grid"]:
        ax.grid(True, axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path / "ups_avg_bar_horizontal.png")
    plt.close()
