import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.schemas import PlotConfig
from src.styles import resolve_style
from src.check import Check
from matplotlib.ticker import MultipleLocator


def apply_style(plot_cfg: PlotConfig) -> None:
    styles = plot_cfg.style_mapped
    Check.valid_style_list(styles)

    for s in styles:
        try:
            plt.style.use(s)
            return
        except OSError:
            continue

    Check.valid_style_list([])


def plot_combined_boxplot(csv_path: Path, output_path: Path, cfg: PlotConfig) -> None:
    apply_style(cfg)
    df = pd.read_csv(csv_path)
    map_names = df["map_name"].unique()
    data = [df[df["map_name"] == name]["effective_ups"].tolist() for name in map_names]

    # figure_facecolor - color of backgraound arround the graph - the biggest layer
    fig, ax = plt.subplots(
        figsize=cfg.figsize, dpi=cfg.dpi, facecolor=cfg.figure_facecolor
    )
    # color of the graph background
    ax.set_facecolor(cfg.axes_facecolor)

    # ── Styling Setup ───────────────────────
    # spine is thin line arround the graph
    for spine in ax.spines.values():
        # spine.set_visible(False)
        spine.set_color(cfg.spine_color)
        spine.set_linewidth(cfg.spine_width)

    # this removes the gridlines!
    ax.tick_params(
        axis="both",
        length=0,
        width=0,
        color=cfg.axis_color,
        labelcolor=cfg.label_font_color,
        # or grid color = "None"
        grid_color=cfg.gr_color,
        # grid_alpha=0,
        # grid_linewidth=0,
    )

    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_major_locator(MultipleLocator(50))

    if cfg.show_grid:
        ax.grid(True, axis="y", color=cfg.axis_color)

    # ── Plot Data ───────────────────────────
    ax.boxplot(
        data,
        patch_artist=True,
        showmeans=False,
        widths=0.5,
        notch=False,
        whis=1.5,
        meanprops=dict(marker="D", markerfacecolor="yellow", markeredgecolor="black"),
        boxprops=dict(facecolor=cfg.box_color, color=cfg.box_color),
        whiskerprops=dict(color=cfg.box_color),
        capprops=dict(color=cfg.box_color),
        medianprops=dict(color=cfg.box_color),
        flierprops=dict(marker="o", color="red", markersize=6, linestyle="none"),
    )

    ax.set_title("UPS Distribution per Map", color=cfg.label_font_color)
    ax.set_ylabel("Effective UPS", color=cfg.label_font_color)
    ax.set_xticks([i + 1 for i in range(len(map_names))])
    ax.set_xticklabels(
        [Path(name).stem for name in map_names],
        rotation=45,
        ha="right",
        fontdict={
            "family": cfg.label_font,
            "fontsize": cfg.label_font_size,
            "color": cfg.label_font_color,
        },
    )

    plt.tight_layout()
    plt.savefig(output_path / "ups_candlesticks.png")
    plt.close()


def plot_avg_ups_horizontal(csv_path: Path, output_path: Path, cfg: PlotConfig) -> None:
    apply_style(cfg)
    df = pd.read_csv(csv_path)
    avg_ups = df.groupby("map_name")["effective_ups"].mean().reset_index()
    avg_ups["map_name"] = avg_ups["map_name"].apply(lambda x: Path(x).stem)
    avg_ups.sort_values(by="effective_ups", ascending=False, inplace=True)

    # figure_facecolor - color of backgraound arround the graph - the biggest layer
    fig, ax = plt.subplots(
        figsize=cfg.figsize, dpi=cfg.dpi, facecolor=cfg.figure_facecolor
    )
    # color of the graph background
    ax.set_facecolor(cfg.axes_facecolor)

    # ── Styling Setup ───────────────────────
    # spine is thin line arround the graph
    for spine in ax.spines.values():
        # spine.set_visible(False)
        spine.set_color(cfg.spine_color)
        spine.set_linewidth(cfg.spine_width)

    # this removes the gridlines!
    ax.tick_params(
        axis="both",
        length=0,
        width=0,
        color=cfg.axis_color,
        labelcolor=cfg.label_font_color,
        # or grid color = "None"
        grid_color=cfg.gr_color,
        # grid_alpha=0,
        # grid_linewidth=0,
    )

    ax.yaxis.set_major_locator(MultipleLocator(200))
    ax.xaxis.set_major_locator(MultipleLocator(200))

    if cfg.show_grid:
        ax.grid(True, axis="y", color=cfg.axis_color)

    # ── Plot Data ───────────────────────────
    bars = ax.barh(
        avg_ups["map_name"], avg_ups["effective_ups"], color=cfg.bar_color, height=0.5
    )

    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f"{int(width)}",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=cfg.label_font_size,
            color=cfg.label_font_color,
            fontname=cfg.label_font,
        )

    ax.set_title("Average UPS per Map", color=cfg.label_font_color)
    ax.set_xlabel("Average Effective UPS", color=cfg.label_font_color)
    ax.set_ylabel("Control Strategy", color=cfg.label_font_color)
    ax.set_yticks(range(len(avg_ups["map_name"])))
    ax.set_yticklabels(
        avg_ups["map_name"],
        fontdict={
            "family": cfg.label_font,
            "fontsize": cfg.label_font_size,
            "color": cfg.label_font_color,
        },
    )

    plt.tight_layout()
    plt.savefig(output_path / "ups_horizontal.png")
    plt.close()
