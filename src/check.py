from pathlib import Path


class Check:
    @staticmethod
    def file_exists(path: Path, msg: str = None) -> None:
        if not path.is_file():
            raise FileNotFoundError(msg or f"Missing file: {path}")

    @staticmethod
    def dir_exists(path: Path, msg: str = None) -> None:
        if not path.is_dir():
            raise NotADirectoryError(msg or f"Missing directory: {path}")

    @staticmethod
    def condition(value: bool, msg: str = None) -> None:
        if not value:
            raise ValueError(msg or "Condition failed.")

    @staticmethod
    def has_equal_sign(line: str, msg: str = None) -> None:
        if "=" not in line:
            raise ValueError(msg or f"Invalid config line (no '='): {line}")

    @staticmethod
    def known_section(section: str, valid: set) -> None:
        if section not in valid:
            raise ValueError(f"Unknown section: [{section}]")

    @staticmethod
    def has_section_before_key(current_section: str) -> None:
        if current_section is None:
            raise ValueError("Config must start with a section header.")

    @staticmethod
    def known_key(key: str, valid_keys: set, section: str) -> None:
        if key not in valid_keys:
            raise KeyError(f"Unknown key '{key}' in section [{section}]")

    @staticmethod
    def style_index_exists(index: int, style_map: dict, msg: str = None) -> None:
        if index not in style_map:
            raise ValueError(msg or f"Unknown style index: {index}")

    @staticmethod
    def folder_required(mode: str, folder: str) -> None:
        if mode in ("bench", "plot", "template") and not folder:
            raise ValueError("Missing folder name (e.g. '0001-iron-smelter')")

    @staticmethod
    def valid_style_list(styles: list[str]) -> None:
        if not styles:
            raise ValueError(
                "[E] No valid styles provided. Check style index mapping or matplotlib installation."
            )
