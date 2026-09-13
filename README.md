# LangChain-Multi-Agent-Research-System

## Prerequisites
- `uv` package manager installed

## Setup

Install uv (if not already installed):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Create virtual environment with uv:
```powershell
uv venv langagent --python 3.11
```

Activate the virtual environment:
```powershell
.\langagent\Scripts\Activate.ps1
```

Install dependencies:
```powershell
uv pip install -r requirements.txt
```

## Running the Project

```powershell
python script_name.py
```