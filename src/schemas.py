from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Type, Tuple, List


@dataclass
class RuntimeConfig:
    factorio_executable: Path
    disable_audio: bool
    showconfiguration: bool


@dataclass
class BenchmarkConfig:
    ticks: int
    runs: int
    platform: str
    map_pattern: str
    output_file: str


@dataclass
class PlotConfig:
    enable_plots: bool
    combined_boxplot: bool
    average_barplot: bool

    label_font: str
    label_font_size: int
    label_font_color: str

    axis_color: str
    spine_color: str
    spine_width: float

    figure_facecolor: str
    axes_facecolor: str
    bar_color: str
    box_color: str

    show_grid: bool
    gr_color: str
    dpi: int
    figsize: Tuple[int, int]

    style: int


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


SECTION_MAP: Dict[str, Type] = {
    "runtime": RuntimeConfig,
    "benchmark": BenchmarkConfig,
    "plot": PlotConfig,
}
