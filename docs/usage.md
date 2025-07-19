# CLI SPECIFICATION

This document defines how to use the script and how each mode behaves.

---

## ⚙️ Defaults and Rules

- If no mode is specified, `--bench` is selected by default
- If `--config` is not provided, `default.cfg` will be used automatically
- Modes are **mutually** exclusive — only one of `--bench`, `--plot`, or `--template`
  
## 🅰️ Benchmark Mode

### 🔧 Usage

```bash
python benchmark.py <folder_name> [--config=<name.cfg>]
```

### 📝 Description

- Runs a benchmark on a given folder: `benchmarks/<folder_name>/`
- Uses config from `config/<name.cfg>` (default: `default.cfg`)
- If no mode is given, `--bench` is assumed automatically

### 🧪 Examples

```bash
python benchmark.py 0001-iron-smelter
python benchmark.py 0023-copper --config=hardcore.cfg
```

---

## 🅱️ Plot Mode

### 🔧 Usage

```bash
python benchmark.py --plot <folder_name> [--config=<name.cfg>] [--csv=<file.csv>]
```

### 📝 Description

- Generates plots from a `.csv` file inside `benchmarks/<folder_name>/`
- Uses plot config from `config/<name.cfg>` (default: `default.cfg`)
- Can specify an alternate CSV file via `--csv`

### 🧪 Examples

```bash
python benchmark.py --plot 0001-iron-smelter
python benchmark.py --plot 0023-copper --csv=results_final.csv
```

---

## 🅲️ Template Mode

### 🔧 Usage

```bash
python benchmark.py --template <folder_name> [--config=<name.cfg>] [--template=<template.md>] [--csv=<file.csv>]
```

### 📝 Description

- Fills a Markdown template with data from a `.csv`
- Inputs:
  - Template file from `template/<template>.md` (default: `report.md`)
  - CSV file from `benchmarks/<folder_name>/<file>.csv` (default: `results.csv`)
- Output is written to:
  - `benchmarks/<folder_name>/generated.md`
- Mode is **exclusive** (cannot combine with other modes)

### 🧪 Examples

```bash
python benchmark.py --template 0001-iron-smelter
python benchmark.py --template 0023-copper --template=compact.md --csv=alt.csv
```

---

## 📁 Project Structure

```text
proj_root/
├── benchmarks/
│   └── 0001-iron-smelter/
│       ├── iron_smelter_enable_clocked.zip
│       ├── ...
│       └── results.csv             # Generated output file
│
├── config/
│   ├── default.cfg                 # Default config
│   └── your_random.cfg             # Custom override config
│ 
├── docs
│   ├── commands.md                 # Factorio commands
│   └── usage.md                    # how to use this script
│ 
├── mods
│   └── mod-list.json               # not implemented yet
│    
│
├── resource/                       # Keeping some old blueprints just for sake of keeping
│
├── src/                            # Relevant import modules for benchmark.py
│
├── template/                       # Templates for generating .md into benchmark folders
│
├── tool/                           
│   └── requirements.txt            # Modules installed via pip install into .env
│
├── benchmark.py                    # Main benchmarking logic (Python)
├── benchmark.bat                   # Windows-friendly launcher
├── install_env.bat                 # Installation of virtual environment
└── README.md                       # Project overview
```
