def echo(message: str, level: str = "I") -> None:
    """
    Level: I = Info, S = Success, W = Warning, E = Error
    """
    symbols = {
        "I": "[I]",
        "S": "[✔]",
        "W": "[!]",
        "E": "[✖]",
    }
    print(f"{symbols.get(level, '[I]')} {message}")
