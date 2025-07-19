from src.echo import echo
from src.config import (
    RuntimeConfig,
    BenchmarkConfig,
    PlotConfig,
)

# fmt: off

def print_runtime_config(runtime: RuntimeConfig) -> None:
    echo("── Runtime Configuration ─────────────")
    echo(f"Executable:       {runtime.factorio_executable}")
    echo(f"Audio Disabled:   {runtime.disable_audio}")


def print_benchmark_config(benchmark: BenchmarkConfig) -> None:
    echo("── Benchmark Configuration ───────────")
    echo(f"Ticks:            {benchmark.ticks}")
    echo(f"Runs:             {benchmark.runs}")
    echo(f"Platform:         {benchmark.platform}")
    echo(f"Map pattern:      {benchmark.map_pattern}")
    echo(f"Output file:      {benchmark.output_file}")



def print_plot_config(plot: PlotConfig) -> None:
    echo("── Plot Configuration ─────────────────")
    echo(f"Plots Enabled:    {plot.enable_plots}")
    echo(f"Boxplot Enabled:  {plot.combined_boxplot}")
    echo(f"Barplot Enabled:  {plot.average_barplot}")
    echo(f"Label Font:       {plot.label_font} ({plot.label_font_size}px, {plot.label_font_color})")
    echo(f"Axis Color:       {plot.axis_color}")
    echo(f"Spine:            {plot.spine_color}, width {plot.spine_width}")
    echo(f"Figure Color:     {plot.figure_facecolor}")
    echo(f"Axes Color:       {plot.axes_facecolor}")
    echo(f"Bar Color:        {plot.bar_color}")
    echo(f"Box Color:        {plot.box_color}")
    echo(f"Grid:             {plot.show_grid}")
    echo(f"DPI:              {plot.dpi}")
    echo(f"Figsize:          {plot.figsize[0]}x{plot.figsize[1]}")
    echo(f"Style Index:      {plot.style}")


# fmt: on


def print_selected_config(
    selected_modes: list[str],
    runtime: RuntimeConfig,
    benchmark: BenchmarkConfig,
    plot: PlotConfig,
) -> None:
    if not runtime.showconfiguration:
        return

    echo("Showing configuration:")
    if "bench" in selected_modes:
        print_runtime_config(runtime)
        print_benchmark_config(benchmark)

    if "plot" in selected_modes:
        print_plot_config(plot)

    if "template" in selected_modes:
        pass
