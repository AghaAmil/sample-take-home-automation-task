from __future__ import annotations

from playwright.sync_api import Page

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


def test_delete_account_and_reject_future_login(
    app_page: Page,
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    logged_in_player_name: str,
) -> None:
    play_page.assert_loaded(logged_in_player_name)
    assert_account_exists(app_page, logged_in_player_name)

    play_page.open_profile_view()
    profile_page.assert_loaded(logged_in_player_name)

    app_page.once("dialog", lambda dialog: dialog.accept())
    profile_page.delete_account()

    account_creation_page.assert_loaded()
    assert_account_does_not_exist(app_page, logged_in_player_name)
    assert_active_session_is_cleared(app_page)

    account_creation_page.switch_to_login_mode()
    account_creation_page.assert_login_mode_loaded()
    account_creation_page.fill_player_name(logged_in_player_name)
    account_creation_page.submit_login()
    account_creation_page.assert_error_message("No account with this name. Please register.")


def assert_account_exists(page: Page, player_name: str) -> None:
    if get_account(page, player_name) is None:
        raise AssertionError(f"expected account {player_name!r} to exist before deletion")


def assert_account_does_not_exist(page: Page, player_name: str) -> None:
    if get_account(page, player_name) is not None:
        raise AssertionError(f"expected account {player_name!r} to be deleted")


def get_account(page: Page, player_name: str) -> dict[str, object] | None:
    return page.evaluate(
        """(playerName) => {
            const users = JSON.parse(localStorage.getItem("ttt:users") || "{}");
            return users[playerName.trim().toLowerCase()] ?? null;
        }""",
        player_name,
    )


def assert_active_session_is_cleared(page: Page) -> None:
    active_session = page.evaluate("""() => localStorage.getItem("ttt:session")""")
    if active_session is not None:
        raise AssertionError(f"expected active session to be cleared, got {active_session!r}")
