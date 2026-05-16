from __future__ import annotations

from playwright.sync_api import expect

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage


EMPTY_NAME_ERROR_TEXT = "Please enter a name."
TOO_SHORT_NAME_ERROR_TEXT = "Name must be at least 2 characters."
DUPLICATE_NAME_ERROR_TEXT = "This name is already taken. Try logging in."
UNKNOWN_LOGIN_ERROR_TEXT = "No account with this name. Please register."


def test_signup_name_validation_errors(
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> None:
    account_creation_page.assert_loaded()

    submit_register_and_expect_error(account_creation_page, "", EMPTY_NAME_ERROR_TEXT)
    submit_register_and_expect_error(account_creation_page, "A", TOO_SHORT_NAME_ERROR_TEXT)

    account_creation_page.fill_player_name(player_name)
    account_creation_page.submit_create_account()
    play_page.assert_loaded(player_name)

    play_page.log_out()
    account_creation_page.assert_loaded()

    duplicate_name_with_different_case = player_name.upper()
    submit_register_and_expect_error(
        account_creation_page, duplicate_name_with_different_case, DUPLICATE_NAME_ERROR_TEXT
    )
    expect(play_page.view_play).not_to_be_visible()


def test_login_name_validation_errors(
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
) -> None:
    account_creation_page.assert_loaded()
    account_creation_page.switch_to_login_mode()
    account_creation_page.assert_login_mode_loaded()

    submit_login_and_expect_error(account_creation_page, "", EMPTY_NAME_ERROR_TEXT)
    submit_login_and_expect_error(account_creation_page, "A", TOO_SHORT_NAME_ERROR_TEXT)
    submit_login_and_expect_error(account_creation_page, "NotCreatedUser", UNKNOWN_LOGIN_ERROR_TEXT)
    expect(play_page.view_play).not_to_be_visible()


def submit_register_and_expect_error(
    account_creation_page: AccountCreationPage,
    player_name: str,
    expected_error_text: str,
) -> None:
    account_creation_page.fill_player_name(player_name)
    account_creation_page.submit_create_account()
    account_creation_page.assert_error_message(expected_error_text)
    expect(account_creation_page.auth_form).to_have_attribute("data-mode", AccountCreationPage.REGISTER_MODE)


def submit_login_and_expect_error(
    account_creation_page: AccountCreationPage,
    player_name: str,
    expected_error_text: str,
) -> None:
    account_creation_page.fill_player_name(player_name)
    account_creation_page.submit_login()
    account_creation_page.assert_error_message(expected_error_text)
    expect(account_creation_page.auth_form).to_have_attribute("data-mode", AccountCreationPage.LOGIN_MODE)
