# sample-take-home-automation-task

Python Playwright automation scaffold for the Tic-Tac-Toe take-home application in
`task_instructions/index.html`.

## Application Under Test

The supplied app is a static single-page web application. The automated tests serve
`task_instructions/` through a local HTTP server and open:

```text
http://127.0.0.1:<port>/index.html
```

## Setup

### Option 1: uv

```bash
uv sync
uv run playwright install chromium
uv run pytest --browser chromium
```

### Option 2: pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest --browser chromium
```

## Useful Commands

```bash
ruff format --check .
ruff check .
pytest --browser chromium
```

Playwright tracing, screenshots, and videos are configured in `pyproject.toml` to
retain artifacts on failures.
