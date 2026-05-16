from __future__ import annotations

from pathlib import Path
import sys
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def test_application_server_serves_entrypoint(app_url: str) -> None:
    with urlopen(app_url, timeout=5) as response:
        page_source = response.read().decode("utf-8")

    assert response.status == 200
    assert "<title>Tic-Tac-Toe</title>" in page_source


if __name__ == "__main__":
    from utils.app_server import launch_application_server

    launch_application_server()
