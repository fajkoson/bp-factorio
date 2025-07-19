from sys import argv
from src.echo import echo
from pathlib import Path
from typing import Dict, Type, Tuple, List
from src.schemas import BenchmarkConfig, PlotConfig, RuntimeConfig
from src.plotting import plot_combined_boxplot, plot_avg_ups_horizontal, apply_style
from src.check import Check
from src.argparser import parse_args
from src.confprint import print_selected_config
from src.config import load_config


def run_benchmark(runtime_section, benchmark_section, plot_section) -> None:
    pass


def run_template(template_section) -> None:
    pass


def run_plot(
    benchmark: BenchmarkConfig, plot_cfg: PlotConfig, folder: str, csv_file: str
) -> None:
    folder_path = Path("benchmarks") / folder
    csv_path = folder_path / csv_file
    plots_path = folder_path / "plots"

    Check.dir_exists(folder_path)
    Check.file_exists(csv_path)

    plots_path.mkdir(parents=True, exist_ok=True)

    if plot_cfg.combined_boxplot:
        plot_combined_boxplot(csv_path, plots_path, plot_cfg)

    if plot_cfg.average_barplot:
        plot_avg_ups_horizontal(csv_path, plots_path, plot_cfg)


def run_selected_mode(
    mode: list[str],
    args: dict,
    runtime_section: RuntimeConfig,
    benchmark_section: BenchmarkConfig,
    plot_section: PlotConfig,
) -> None:
    if mode == "bench":
        run_benchmark(runtime_section, benchmark_section)
        echo("Benchmark completed successfully.", level="S")
    elif mode == "plot":
        run_plot(benchmark_section, plot_section, args["folder"], args["csv"])
        echo("Plots generated.", level="S")
    elif mode == "template":
        run_template(benchmark_section, args)
        echo("Template exported.", level="S")


def main():
    args = parse_args(argv[1:])
    runtime, benchmark, plot = load_config(args["config"])
    if runtime.showconfiguration:
        print_selected_config(args["mode"], runtime, benchmark, plot)
    run_selected_mode(args["mode"], args, runtime, benchmark, plot)


if __name__ == "__main__":
    main()
