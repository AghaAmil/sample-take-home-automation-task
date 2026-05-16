from __future__ import annotations

from typing import Final

from playwright.sync_api import Locator, Page, expect


class AccountCreationPage:
    """Page object for the authentication screen."""

    REGISTER_MODE: Final = "register"
    LOGIN_MODE: Final = "login"
    TITLE_TEXT: Final = "Tic-Tac-Toe"
    SUBTITLE_TEXT: Final = "A small game for test automation"
    LANGUAGE_LABEL_TEXT: Final = "Language"
    LANGUAGE_OPTIONS: Final = ("English", "Persian")
    DEFAULT_LANGUAGE_VALUE: Final = "en"
    DEFAULT_THEME_BUTTON_TEXT: Final = "Dark"
    AUTH_TITLE_TEXT: Final = "Welcome"
    AUTH_SUBTITLE_TEXT: Final = "Enter your name to start playing."
    NAME_PLACEHOLDER_TEXT: Final = "e.g. Sara"
    CREATE_ACCOUNT_BUTTON_TEXT: Final = "Create Account"
    LOGIN_BUTTON_TEXT: Final = "Log In"
    SWITCH_TO_LOGIN_TEXT: Final = "Already have an account? Log in"
    SWITCH_TO_REGISTER_TEXT: Final = "New player? Create an account"

    def __init__(self, page: Page) -> None:
        self.page = page

        self.app: Locator = page.locator("div[data-testid='app']")
        self.app_header: Locator = page.locator("header[data-testid='app-header']")
        self.title: Locator = page.locator("h1[data-testid='title']")
        self.subtitle: Locator = page.locator("p[data-testid='subtitle']")
        self.label_language: Locator = page.locator("span[data-testid='label-language']")
        self.select_language: Locator = page.locator("select[data-testid='select-language']")
        self.btn_theme: Locator = page.locator("button[data-testid='btn-theme']")
        self.root: Locator = page.locator("main[data-testid='root']")

        self.auth_form: Locator = page.locator("form[data-testid='auth-form']")
        self.auth_title: Locator = page.locator("h2[data-testid='auth-title']")
        self.auth_subtitle: Locator = page.locator("p[data-testid='auth-subtitle']")
        self.input_name: Locator = page.locator("input[data-testid='input-name']")
        self.auth_error: Locator = page.locator("div[data-testid='auth-error']")
        self.btn_register: Locator = page.locator("button[data-testid='btn-register']")
        self.btn_login: Locator = page.locator("button[data-testid='btn-login']")
        self.btn_switch_mode: Locator = page.locator("button[data-testid='btn-switch-mode']")
        self.auth_submit_button: Locator = self.auth_form.locator("button[type='submit']")

        self.initial_visible_elements: tuple[Locator, ...] = (
            self.app,
            self.app_header,
            self.title,
            self.subtitle,
            self.label_language,
            self.select_language,
            self.btn_theme,
            self.root,
            self.auth_form,
            self.auth_title,
            self.auth_subtitle,
            self.input_name,
            self.btn_register,
            self.btn_switch_mode,
        )
        self.login_visible_elements: tuple[Locator, ...] = (
            self.app,
            self.app_header,
            self.title,
            self.subtitle,
            self.label_language,
            self.select_language,
            self.btn_theme,
            self.root,
            self.auth_form,
            self.auth_title,
            self.auth_subtitle,
            self.input_name,
            self.btn_login,
            self.btn_switch_mode,
        )

    def assert_loaded(self) -> None:
        """Assert the account creation page is visible and contains the expected default values."""
        self.assert_all_initial_elements_are_visible()
        self.assert_all_initial_values_are_correct()

    def assert_all_initial_elements_are_visible(self) -> None:
        for element in self.initial_visible_elements:
            expect(element).to_be_visible()

    def assert_all_initial_values_are_correct(self) -> None:
        self.assert_common_values_are_correct()
        expect(self.auth_form).to_have_attribute("data-mode", self.REGISTER_MODE)
        expect(self.input_name).to_have_value("")
        expect(self.input_name).to_have_attribute("placeholder", self.NAME_PLACEHOLDER_TEXT)
        expect(self.btn_register).to_have_text(self.CREATE_ACCOUNT_BUTTON_TEXT)
        expect(self.auth_submit_button).to_have_text(self.CREATE_ACCOUNT_BUTTON_TEXT)
        expect(self.btn_switch_mode).to_have_text(self.SWITCH_TO_LOGIN_TEXT)
        expect(self.auth_error).not_to_be_visible()

    def assert_login_mode_loaded(self) -> None:
        self.assert_all_login_elements_are_visible()
        self.assert_login_mode_values_are_correct()

    def assert_all_login_elements_are_visible(self) -> None:
        for element in self.login_visible_elements:
            expect(element).to_be_visible()

    def assert_login_mode_values_are_correct(self) -> None:
        self.assert_common_values_are_correct()
        expect(self.auth_form).to_have_attribute("data-mode", self.LOGIN_MODE)
        expect(self.input_name).to_have_value("")
        expect(self.input_name).to_have_attribute("placeholder", self.NAME_PLACEHOLDER_TEXT)
        expect(self.btn_login).to_have_text(self.LOGIN_BUTTON_TEXT)
        expect(self.auth_submit_button).to_have_text(self.LOGIN_BUTTON_TEXT)
        expect(self.btn_switch_mode).to_have_text(self.SWITCH_TO_REGISTER_TEXT)
        expect(self.auth_error).not_to_be_visible()

    def assert_common_values_are_correct(self) -> None:
        expect(self.title).to_have_text(self.TITLE_TEXT)
        expect(self.subtitle).to_have_text(self.SUBTITLE_TEXT)
        expect(self.label_language).to_have_text(self.LANGUAGE_LABEL_TEXT)
        expect(self.select_language.locator("option")).to_have_text(list(self.LANGUAGE_OPTIONS))
        expect(self.select_language).to_have_value(self.DEFAULT_LANGUAGE_VALUE)
        expect(self.btn_theme).to_have_text(self.DEFAULT_THEME_BUTTON_TEXT)
        expect(self.auth_title).to_have_text(self.AUTH_TITLE_TEXT)
        expect(self.auth_subtitle).to_have_text(self.AUTH_SUBTITLE_TEXT)

    def fill_player_name(self, player_name: str) -> None:
        self.input_name.fill(player_name)

    def switch_to_login_mode(self) -> None:
        if self.auth_form.get_attribute("data-mode") != self.LOGIN_MODE:
            self.btn_switch_mode.click()
        expect(self.auth_form).to_have_attribute("data-mode", self.LOGIN_MODE)

    def switch_to_register_mode(self) -> None:
        if self.auth_form.get_attribute("data-mode") != self.REGISTER_MODE:
            self.btn_switch_mode.click()
        expect(self.auth_form).to_have_attribute("data-mode", self.REGISTER_MODE)

    def submit_create_account(self) -> None:
        self.btn_register.click()

    def submit_login(self) -> None:
        self.btn_login.click()

    def assert_error_message(self, expected_text: str) -> None:
        expect(self.auth_error).to_be_visible()
        expect(self.auth_error).to_have_text(expected_text)
