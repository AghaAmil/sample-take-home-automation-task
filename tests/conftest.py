import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import Page

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from utils.app_server import StaticAppServer  # noqa: E402
from utils.app_server import create_app_server  # noqa: E402


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def src_root() -> Path:
    return SRC_ROOT


@pytest.fixture(scope="session", autouse=True)
def app_server() -> Generator[StaticAppServer]:
    app_server = create_app_server()
    app_server.start()

    try:
        yield app_server
    finally:
        app_server.stop()


@pytest.fixture(scope="session")
def app_url(app_server: StaticAppServer) -> str:
    return app_server.url


@pytest.fixture
def app_page(page: Page, app_url: str) -> Page:
    """
    Fixture to initialize and return a web page instance for testing.

    Navigate the mentioned URL, clears the local
    storage to ensure a clean state, and reloads the page.

    :param page: A Playwright `Page` object representing the browser page.
    :param app_url: A string representing the URL of the application to be tested.
    :return: A Playwright `Page` object with the specified application loaded.
    """
    page.goto(app_url)
    page.evaluate("localStorage.clear()")
    page.reload(wait_until="networkidle")
    return page
