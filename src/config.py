from pathlib import Path
from typing import Any
from pathlib import Path
from src.check import Check
from dataclasses import fields
from typing import Dict, Type, Tuple, Any, Type, get_origin, get_args
from src.schemas import RuntimeConfig, BenchmarkConfig, PlotConfig, SECTION_MAP

CONFIG_PATH = Path("config/default.cfg")


def parse_config_line(line: str) -> Tuple[str, str]:
    Check.has_equal_sign(line)
    key, value = line.split("=", 1)
    return key.strip().lower(), value.strip()


def coerce_value(field_type: Type, value: str) -> Any:
    origin = get_origin(field_type)

    if field_type == bool:
        return value.strip().lower() == "true"
    elif field_type == int:
        return int(value)
    elif field_type == float:
        return float(value)
    elif field_type == Path:
        return Path(value)
    elif field_type == str:
        return value

    # Handle Tuple[int, int] like '10x5'
    if origin is tuple and get_args(field_type) == (int, int):
        parts = value.lower().replace(" ", "").split("x")
        return tuple(int(x) for x in parts)

    # (Future-proof) Handle List[str], List[int], etc.
    if origin is list:
        subtype = get_args(field_type)[0]
        return [coerce_value(subtype, v.strip()) for v in value.split(",")]

    raise TypeError(f"Unsupported config field type: {field_type}")


def load_config(path: Path) -> Tuple[RuntimeConfig, BenchmarkConfig, PlotConfig]:
    path = Path(path)
    Check.file_exists(path)

    raw_data: Dict[str, Dict[str, str]] = {section: {} for section in SECTION_MAP}
    current_section = None

    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip().lower()
                Check.known_section(section, raw_data)
                current_section = section
                continue
            Check.has_section_before_key(current_section)
            key, value = parse_config_line(line)
            raw_data[current_section][key] = value

    result = {}
    for section, cls in SECTION_MAP.items():
        section_fields = {f.name: f.type for f in fields(cls)}
        section_data = {}
        for key, raw_val in raw_data[section].items():
            Check.known_key(key, section_fields, section)
            field_type = section_fields[key]
            section_data[key] = coerce_value(field_type, raw_val)
        result[section] = cls(**section_data)

    plot_config = result["plot"]
    from src.styles import resolve_style

    plot_config.style_mapped = resolve_style(plot_config.style)

    return result["runtime"], result["benchmark"], plot_config
