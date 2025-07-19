import sys
from pathlib import Path
from src.check import Check


def parse_args(argv: list[str] = None) -> dict:
    """
    Parses command-line arguments and returns a dictionary of options.
    - Mode:       --bench (default), --plot, or --template (mutually exclusive)
    - Folder:     First non-flag argument is treated as the benchmark folder
    - Config:     --config <name> → looks for config/<name>.cfg
    - CSV File:   --csv <filename> (optional, for plot/template)
    - Template:   --template <name> (only for --template mode)

    Usage examples:
    - python benchmark.py 0001-iron-smelter
    - python benchmark.py --plot 0001-iron-smelter --csv results.csv
    - python benchmark.py --template report --config hardcore --csv results.csv 0001-iron-smelter
    """

    argv = argv or sys.argv[1:]
    args = {
        "mode": "bench",
        "config": "default.cfg",
        "csv": "test_results.csv",
        "template": None,
        "folder": None,
    }

    try:
        i = 0
        while i < len(argv):
            arg = argv[i]
            if arg in ("--bench", "--plot", "--template"):
                args["mode"] = arg.lstrip("-")
            elif arg == "--config":
                i += 1
                args["config"] = argv[i]
            elif arg == "--csv":
                i += 1
                args["csv"] = argv[i]
            elif arg == "--template":
                i += 1
                args["template"] = argv[i]
            elif not arg.startswith("--") and args["folder"] is None:
                args["folder"] = arg
            i += 1

    except IndexError as e:
        raise ValueError(f"Missing value for argument: {arg}") from e

    # Validate folder is passed for relevant modes
    Check.folder_required(args["mode"], args["folder"])

    # If config path doesn't already start with config/, prepend it
    config_path = Path(args["config"])
    if not config_path.parent.parts:
        args["config"] = str(Path("config") / config_path)

    return args
