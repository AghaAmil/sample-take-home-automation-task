from __future__ import annotations

from pathlib import Path
from urllib.request import urlopen


def test_project_paths_match_app_server(project_root: Path, src_root: Path) -> None:
    from utils.app_server import PROJECT_ROOT as APP_SERVER_PROJECT_ROOT

    assert APP_SERVER_PROJECT_ROOT == project_root
    assert src_root == project_root / "src"
    assert (src_root / "utils" / "app_server.py").is_file()


def test_application_server_serves_entrypoint(app_url: str) -> None:
    with urlopen(app_url, timeout=5) as response:
        page_source = response.read().decode("utf-8")

    assert response.status == 200
    assert "<title>Tic-Tac-Toe</title>" in page_source


if __name__ == "__main__":
    # Applies the shared test path setup when this file is run directly.
    import conftest  # noqa: F401
    from utils.app_server import launch_application_server

    launch_application_server()
