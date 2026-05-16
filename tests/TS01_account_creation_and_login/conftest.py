from __future__ import annotations

from uuid import uuid4

import pytest
from playwright.sync_api import Page

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


@pytest.fixture
def player_name() -> str:
    return f"Auto Player {uuid4().hex[:8]}"


@pytest.fixture
def account_creation_page(app_page: Page) -> AccountCreationPage:
    return AccountCreationPage(app_page)


@pytest.fixture
def play_page(app_page: Page) -> GameDashboardViewPlayPage:
    return GameDashboardViewPlayPage(app_page)


@pytest.fixture
def profile_page(app_page: Page) -> GameDashboardProfileViewPage:
    return GameDashboardProfileViewPage(app_page)


@pytest.fixture
def history_page(app_page: Page) -> GameDashboardHistoryViewPage:
    return GameDashboardHistoryViewPage(app_page)
