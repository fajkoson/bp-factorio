import subprocess
import re
import csv
import sys
from configparser import ConfigParser
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path
import matplotlib.style as mplstyle
from src.benchmark_tools import (
    extract_plot_config,
    plot_combined_boxplot,
    plot_avg_ups_bar,
    plot_avg_ups_horizontal,
)


def parse_locale_float(value: str) -> float:
    return float(value.replace(",", "."))


@dataclass
class BenchmarkResult:
    map_name: str
    run_index: int
    startup_time: str
    end_time: str
    avg_ms: str
    min_ms: str
    max_ms: str
    ticks: int
    actual_ticks: int
    execution_time: str
    effective_ups: float
    factorio_version: str
    platform: str


class BenchmarkRunner:
    def __init__(self, benchmark_dir: Path, config_path: Path):
        self.benchmark_dir = benchmark_dir
        self.config_path = config_path
        self.results: list[BenchmarkResult] = []
        self.maps: list[Path] = []
        self._load_config()

    def _load_config(self):
        config = ConfigParser(comment_prefixes=("#", ";"))
        config.read(self.config_path)
        plot = config["plot"]
        runtime = config["runtime"]
        bench = config["benchmark"]
        debug = config["debug"]

        self.factorio_exe = runtime.get("factorio_executable")
        self.disable_audio = runtime.getboolean("disable_audio")
        self.no_log_rotation = runtime.getboolean("no_log_rotation")
        self.disable_auto_updates = runtime.getboolean("disable_auto_updates")
        self.use_mod_directory = runtime.getboolean("mod_directory")

        self.ticks = bench.getint("ticks")
        self.runs = bench.getint("runs")
        self.platform = bench.get("platform")
        self.map_pattern = bench.get("map_pattern")
        self.output_file = self.benchmark_dir / bench.get("output_file")
        self.verbose = debug.getboolean("verbose")
        self.plot_label_font = plot.get("label_font", fallback="monospace")
        self.plot_label_font_size = plot.getint("label_font_size", fallback=10)
        self.plot_label_font_color = plot.get("label_font_color", fallback="white")
        self.plot_axis_color = plot.get("axis_color", fallback="white")
        self.plot_spine_color = plot.get("spine_color", fallback="white")
        self.plot_spine_width = plot.getint("spine_width", fallback=1)

        style_raw = plot.get("style", fallback="default").strip()

        if style_raw.startswith("style[") and style_raw.endswith("]"):
            try:
                stylelist_key = style_raw
                stylelist_section = config["stylelist"]
                style_options = stylelist_section.get(stylelist_key, fallback="").split(
                    ","
                )

                style_options = [s.strip() for s in style_options if s.strip()]
                self.plot_style = style_options[0] if style_options else "default"

            except Exception as e:
                print(
                    f"[W] Failed to load style from {style_raw}, falling back to default. Reason: {e}"
                )
                self.plot_style = "default"
        else:
            self.plot_style = style_raw

        self.plot_enabled = plot.getboolean("enable_plots")
        self.plot_combined_boxplot = plot.getboolean("combined_boxplot")
        self.plot_avg_bar = plot.getboolean("average_barplot")
        self.plot_avg_ups_horizontal = plot.getboolean("average_barplot")

        self.plot_bar_color = plot.get("bar_color")
        self.plot_box_color = plot.get("box_color")
        self.plot_show_grid = plot.getboolean("show_grid")
        self.plot_figure_facecolor = plot.get("figure_facecolor", fallback="white")
        self.plot_axes_facecolor = plot.get("axes_facecolor", fallback="white")

        self.plot_dpi = plot.getint("dpi")

        # Parse figsize like "10x6"
        raw_figsize = plot.get("figsize")
        try:
            self.plot_figsize = tuple(int(x) for x in raw_figsize.lower().split("x"))
        except Exception:
            self.plot_figsize = (10, 6)

    def _collect_maps(self):
        self.maps = sorted(self.benchmark_dir.glob(f"*{self.map_pattern}"))

    def _run_benchmark(self, map_path: Path) -> str:
        print(f"[DEBUG] Running benchmark with {self.ticks} ticks on {map_path.name}")
        args = [
            self.factorio_exe,
            "--benchmark",
            str(map_path),
            "--benchmark-ticks",
            str(self.ticks),
        ]

        if self.disable_audio:
            args.append("--disable-audio")
        if self.no_log_rotation:
            args.append("--no-log-rotation")
        if self.disable_auto_updates:
            args.append("--disable-auto-updates")
        if self.use_mod_directory:
            args += ["--mod-directory", "mods"]

        if self.verbose:
            print(f"[CMD] {' '.join(args)}")

        process = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False
        )
        stdout, stderr = process.communicate()

        if self.verbose:
            print(f"[DEBUG] Benchmark raw output for {map_path.name}:\n{stdout}")

        if process.returncode != 0:
            print(f"[E] Factorio failed on {map_path.name}:\n{stderr}")
            return ""

        return stdout

    def _parse_benchmark_output(
        self, output: str, map_name: str, run_index: int
    ) -> Optional[BenchmarkResult]:
        lines = [re.sub(r"\s+", " ", line.strip()) for line in output.splitlines()]
        try:
            avg_line = next(l for l in lines if "avg:" in l)
            perf_line = next(l for l in lines if "Performed" in l)

            updates_match = re.search(r"Performed\s+(\d+)\s+updates", perf_line)
            if not updates_match:
                raise ValueError(
                    f"Could not extract tick count\n→ perf_line: '{perf_line}'"
                )
            actual_ticks = int(updates_match.group(1))
            print(f"[DEBUG] Actual performed ticks: {actual_ticks}")

            load_line = next(l for l in lines if "Loading script.dat" in l)

            avg_match = re.search(
                r"avg:\s*([\d.,]+)[^\d]+min:\s*([\d.,]+)[^\d]+max:\s*([\d.,]+)",
                avg_line,
            )
            if not avg_match:
                raise ValueError(
                    f"Could not parse avg/min/max line\n→ avg_line: '{avg_line}'"
                )

            avg_ms_str, min_ms_str, max_ms_str = avg_match.groups()
            avg_ms = parse_locale_float(avg_ms_str)
            min_ms = parse_locale_float(min_ms_str)
            max_ms = parse_locale_float(max_ms_str)

            perf_match = re.search(
                r"Performed\s+\d+\s+updates\s+in\s+([\d.,]+)", perf_line
            )
            if not perf_match:
                raise ValueError(
                    f"Could not parse execution time\n→ perf_line: '{perf_line}'"
                )

            execution_time_str = perf_match.group(1)
            execution_time = parse_locale_float(execution_time_str)

            startup_time = load_line.split()[0]
            end_time = lines[-1].split()[0]
            factorio_version = lines[0].split()[4]

            effective_ups = round((1000 * self.ticks) / execution_time, 2)

            return BenchmarkResult(
                map_name=map_name,
                run_index=run_index,
                startup_time=startup_time,
                end_time=end_time,
                avg_ms=avg_ms,
                min_ms=min_ms,
                max_ms=max_ms,
                ticks=self.ticks,
                actual_ticks=actual_ticks,
                execution_time=execution_time_str.replace(",", "."),
                effective_ups=effective_ups,
                factorio_version=factorio_version,
                platform=self.platform,
            )

        except Exception as e:
            print(f"[E] Error parsing benchmark output for '{map_name}': {e}")
            return None

    def _write_results(self):
        with self.output_file.open("w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=BenchmarkResult.__annotations__.keys()
            )
            writer.writeheader()
            for r in self.results:
                writer.writerow(asdict(r))

    def run(self):
        self._collect_maps()
        total_maps = len(self.maps)

        print(f"[I] Starting {self.runs} runs per map for {total_maps} maps.\n")

        for map_path in self.maps:
            map_name = map_path.name
            print(f"[M] Benchmarking: {map_name}")

            for run_index in range(1, self.runs + 1):
                print(f"[I] Run {run_index}/{self.runs}")
                output = self._run_benchmark(map_path)
                result = self._parse_benchmark_output(output, map_name, run_index)
                if result:
                    self.results.append(result)

        self._write_results()
        print(f"\n[I] Benchmarking complete. Results saved to '{self.output_file}'\n")


def run_benchmark_and_generate_plots(benchmark_name: str, config_name: str) -> None:
    benchmark_dir = Path("benchmarks") / benchmark_name
    config_path = Path("config") / f"{config_name}.cfg"

    # Run benchmark first (this loads and resolves full config)
    runner = BenchmarkRunner(benchmark_dir, config_path)
    runner.run()

    # Extract plot config, then inject resolved style
    config_parser = ConfigParser(comment_prefixes=("#", ";"))
    config_parser.read(config_path)
    cfg = extract_plot_config(config_parser)
    cfg["style"] = runner.plot_style

    if cfg["style"] not in mplstyle.available:
        raise ValueError(
            f"Invalid style '{cfg['style']}' — not in matplotlib.style.available"
        )

    output_dir = benchmark_dir / "plots"
    output_dir.mkdir(exist_ok=True)

    if runner.plot_enabled:
        if runner.plot_combined_boxplot:
            plot_combined_boxplot(runner.output_file, output_dir, cfg)
        # if runner.plot_avg_bar:
        #    plot_avg_ups_bar(runner.output_file, output_dir, cfg)
        if runner.plot_avg_ups_horizontal:
            plot_avg_ups_horizontal(runner.output_file, output_dir, cfg)

        print(f"[I] Plots saved to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: benchmark_new.py <benchmark_folder> <config_file>")
        sys.exit(1)

    run_benchmark_and_generate_plots(sys.argv[1], sys.argv[2])
