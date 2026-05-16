# sample-take-home-automation-task

Python Playwright automation scaffold for the Tic-Tac-Toe take-home application in
`index.html`.

## Application Under Test

The supplied app is a static single-page web application. The automated tests serve
the configured app root through a local HTTP server and open:

```text
http://127.0.0.1:<port>/index.html
```

The original task instructions live in `docs/INSTRUCTIONS.md`.

## Configuration

Runtime test configuration is loaded from `.env` in the project root:

```dotenv
APP_HOST=127.0.0.1
APP_PORT=0
APP_ROOT=.
APP_ENTRYPOINT=index.html
```

`.env` is ignored by Git for local overrides. Keep `.env.example` updated when
configuration keys change.

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
pytest --browser chromium --headed
pytest --browser firefox
pytest --browser webkit
pytest --browser chromium --browser-channel chrome
python tests/server_test.py
```

Playwright runs headless by default. Add `--headed` to watch the browser. Use
`webkit` for Safari-family coverage, or Chromium with `--browser-channel chrome`
to run installed Google Chrome.

Playwright tracing, screenshots, and videos are configured in `pyproject.toml` to
retain artifacts on failures.
