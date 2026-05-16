from __future__ import annotations

from collections.abc import Callable
from typing import Any
from uuid import uuid4

from playwright.sync_api import Page, expect

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


def test_profile_rename_validation_and_login_identity(
    app_page: Page,
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
    logged_in_player_name: str,
    seed_accounts: Callable[..., None],
) -> None:
    duplicate_name = f"TakenUser{uuid4().hex[:6]}"
    simple_name = "Mina"
    special_name = f"QA_User-#{uuid4().hex[:4]}"

    seed_accounts(
        [stored_account(duplicate_name, created_at_ms=current_browser_timestamp_ms(app_page))],
        replace=False,
        reload=False,
    )

    play_page.assert_loaded(logged_in_player_name)
    play_page.open_profile_view()
    profile_page.assert_loaded(logged_in_player_name)

    assert_profile_name_input_validation(profile_page, logged_in_player_name)
    rename_profile(profile_page, old_name=logged_in_player_name, new_name=simple_name)
    rename_profile(profile_page, old_name=simple_name, new_name=special_name)
    assert_duplicate_profile_name_is_rejected(profile_page, duplicate_name, current_name=special_name)
    assert_profile_history_and_play_still_work(profile_page, history_page, play_page, special_name)
    assert_login_uses_new_username_only(
        account_creation_page, profile_page, play_page, logged_in_player_name, special_name
    )

    play_page.open_profile_view()
    profile_page.assert_loaded(special_name)
    assert_account_exists(app_page, special_name)
    assert_account_does_not_exist(app_page, logged_in_player_name)


def assert_profile_name_input_validation(
    profile_page: GameDashboardProfileViewPage,
    unchanged_name: str,
) -> None:
    profile_page.fill_display_name("")
    profile_page.assert_display_name_input_is_invalid()
    profile_page.save_profile_changes()
    profile_page.assert_navigation_values_are_correct(unchanged_name)
    expect(profile_page.profile_message).not_to_be_visible()
    expect(profile_page.profile_error).not_to_be_visible()

    profile_page.fill_display_name("A")
    profile_page.assert_display_name_input_is_invalid()
    profile_page.save_profile_changes()
    profile_page.assert_navigation_values_are_correct(unchanged_name)
    expect(profile_page.profile_message).not_to_be_visible()
    expect(profile_page.profile_error).not_to_be_visible()

    profile_page.fill_display_name("  ")
    profile_page.assert_display_name_input_is_valid()
    profile_page.save_profile_changes()
    profile_page.assert_profile_error_message("Please enter a name.")
    profile_page.assert_navigation_values_are_correct(unchanged_name)


def rename_profile(
    profile_page: GameDashboardProfileViewPage,
    *,
    old_name: str,
    new_name: str,
) -> None:
    profile_page.update_display_name(new_name)
    profile_page.assert_display_name_was_updated(new_name)
    assert_account_exists(profile_page.page, new_name)
    assert_account_does_not_exist(profile_page.page, old_name)
    assert_active_session(profile_page.page, new_name)


def assert_duplicate_profile_name_is_rejected(
    profile_page: GameDashboardProfileViewPage,
    duplicate_name: str,
    *,
    current_name: str,
) -> None:
    profile_page.update_display_name(duplicate_name)
    expect(profile_page.profile_error).to_be_visible()
    expect(profile_page.profile_error).to_have_attribute("role", "alert")
    expect(profile_page.profile_error).to_have_text(GameDashboardProfileViewPage.DUPLICATE_NAME_ERROR_TEXT)
    profile_page.assert_navigation_values_are_correct(current_name)
    assert_active_session(profile_page.page, current_name)
    assert_account_exists(profile_page.page, current_name)
    assert_account_exists(profile_page.page, duplicate_name)


def assert_profile_history_and_play_still_work(
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> None:
    profile_page.open_history_view()
    history_page.assert_empty_loaded(player_name)

    history_page.open_play_view()
    play_page.assert_loaded(player_name)


def assert_login_uses_new_username_only(
    account_creation_page: AccountCreationPage,
    profile_page: GameDashboardProfileViewPage,
    play_page: GameDashboardViewPlayPage,
    old_name: str,
    new_name: str,
) -> None:
    profile_page.log_out()
    account_creation_page.assert_loaded()
    account_creation_page.switch_to_login_mode()
    account_creation_page.assert_login_mode_loaded()

    account_creation_page.fill_player_name(old_name)
    account_creation_page.submit_login()
    account_creation_page.assert_error_message("No account with this name. Please register.")

    account_creation_page.fill_player_name(new_name)
    account_creation_page.submit_login()
    play_page.assert_loaded(new_name)


def stored_account(
    player_name: str,
    *,
    created_at_ms: int,
    difficulty: str = GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE,
    history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "name": player_name,
        "createdAt": created_at_ms,
        "difficulty": difficulty,
        "history": history or [],
    }


def assert_account_exists(page: Page, player_name: str) -> None:
    if get_account(page, player_name) is None:
        raise AssertionError(f"expected account {player_name!r} to exist")


def assert_account_does_not_exist(page: Page, player_name: str) -> None:
    if get_account(page, player_name) is not None:
        raise AssertionError(f"expected account {player_name!r} not to exist")


def get_account(page: Page, player_name: str) -> dict[str, Any] | None:
    return page.evaluate(
        """(playerName) => {
            const users = JSON.parse(localStorage.getItem("ttt:users") || "{}");
            return users[playerName.trim().toLowerCase()] ?? null;
        }""",
        player_name,
    )


def assert_active_session(page: Page, player_name: str) -> None:
    active_session = page.evaluate("""() => localStorage.getItem("ttt:session")""")
    if active_session != player_name:
        raise AssertionError(f"expected active session {player_name!r}, got {active_session!r}")


def current_browser_timestamp_ms(page: Page) -> int:
    return int(page.evaluate("Date.now()"))
