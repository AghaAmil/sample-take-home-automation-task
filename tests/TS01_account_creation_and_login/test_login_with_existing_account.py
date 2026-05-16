from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


@dataclass(frozen=True)
class ExistingAccount:
    player_name: str
    login_name: str
    created_at_ms: int
    difficulty: str
    history: tuple[dict[str, Any], ...]


@pytest.fixture
def existing_account(app_page: Page) -> ExistingAccount:
    now_ms = current_browser_timestamp_ms(app_page)
    player_name = f"Existing Player {uuid4().hex[:8]}"
    account = ExistingAccount(
        player_name=player_name,
        login_name=player_name.upper(),
        created_at_ms=now_ms - days_in_ms(14),
        difficulty="hard",
        history=(
            {
                "finishedAt": now_ms - days_in_ms(3),
                "difficulty": "hard",
                "result": "win",
            },
            {
                "finishedAt": now_ms - days_in_ms(2),
                "difficulty": "medium",
                "result": "loss",
            },
            {
                "finishedAt": now_ms - days_in_ms(1),
                "difficulty": "easy",
                "result": "draw",
            },
        ),
    )

    seed_existing_account(app_page, account)
    app_page.reload(wait_until="networkidle")
    return account


def test_login_with_existing_account_restores_saved_account_data(
    app_page: Page,
    existing_account: ExistingAccount,
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
) -> None:
    account_creation_page.assert_loaded()

    account_creation_page.switch_to_login_mode()
    account_creation_page.assert_login_mode_loaded()
    account_creation_page.fill_player_name(existing_account.login_name)
    account_creation_page.submit_login()

    assert_play_view_loaded_with_existing_account(play_page, existing_account)
    assert_active_session_matches_account(app_page, existing_account)

    play_page.open_profile_view()
    assert_profile_view_loaded_with_existing_account(profile_page, existing_account)

    profile_page.open_history_view()
    history_page.assert_populated_loaded(
        existing_account.player_name,
        expected_records=existing_account.history,
    )


def seed_existing_account(page: Page, account: ExistingAccount) -> None:
    page.evaluate(
        """(account) => {
            const normalizedPlayerName = account.player_name.trim().toLowerCase();
            const storedAccount = {
                name: account.player_name,
                createdAt: account.created_at_ms,
                difficulty: account.difficulty,
                history: account.history,
            };

            localStorage.setItem("ttt:users", JSON.stringify({[normalizedPlayerName]: storedAccount}));
            localStorage.removeItem("ttt:session");
        }""",
        asdict(account),
    )


def assert_play_view_loaded_with_existing_account(
    play_page: GameDashboardViewPlayPage,
    account: ExistingAccount,
) -> None:
    play_page.assert_all_initial_elements_are_visible()
    play_page.assert_header_values_are_correct()
    play_page.assert_navigation_values_are_correct(account.player_name)
    expect(play_page.select_difficulty).to_have_value(account.difficulty)
    expect(play_page.status).to_have_text(GameDashboardViewPlayPage.STATUS_TEXT)
    expect(play_page.status).to_have_attribute("data-status", GameDashboardViewPlayPage.STATUS_DATA_VALUE)
    expect(play_page.board).to_have_attribute("aria-label", GameDashboardViewPlayPage.BOARD_ARIA_LABEL)
    play_page.assert_initial_board_values_are_correct()
    expect(play_page.btn_new).to_have_text(GameDashboardViewPlayPage.NEW_GAME_BUTTON_TEXT)
    expect(play_page.btn_hint).to_have_text(GameDashboardViewPlayPage.HINT_BUTTON_TEXT)
    expect(play_page.btn_reset).to_have_text(GameDashboardViewPlayPage.RESET_BUTTON_TEXT)


def assert_profile_view_loaded_with_existing_account(
    profile_page: GameDashboardProfileViewPage,
    account: ExistingAccount,
) -> None:
    profile_page.assert_all_initial_elements_are_visible()
    profile_page.assert_header_values_are_correct()
    profile_page.assert_navigation_values_are_correct(account.player_name)
    profile_page.assert_profile_values_are_correct(account.player_name)
    profile_page.assert_profile_stats(wins=1, losses=1, draws=1)
    profile_page.assert_created_at_is_between(account.created_at_ms, account.created_at_ms, tolerance_ms=1000)


def assert_active_session_matches_account(page: Page, account: ExistingAccount) -> None:
    active_session = page.evaluate("""() => localStorage.getItem("ttt:session")""")
    if active_session != account.player_name:
        raise AssertionError(f"expected active session {account.player_name!r}, got {active_session!r}")


def current_browser_timestamp_ms(page: Page) -> int:
    return int(page.evaluate("Date.now()"))


def days_in_ms(days: int) -> int:
    return days * 24 * 60 * 60 * 1000
