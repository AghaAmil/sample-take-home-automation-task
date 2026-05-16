from __future__ import annotations

from datetime import datetime
from typing import Final

from playwright.sync_api import Locator, Page, expect


class GameDashboardProfileViewPage:
    """Page object for the game dashboard Profile view."""

    TITLE_TEXT: Final = "Tic-Tac-Toe"
    SUBTITLE_TEXT: Final = "A small game for test automation"
    LANGUAGE_LABEL_TEXT: Final = "Language"
    LANGUAGE_OPTIONS: Final = ("English", "Persian")
    DEFAULT_LANGUAGE_VALUE: Final = "en"
    DEFAULT_THEME_BUTTON_TEXT: Final = "Dark"
    DEFAULT_THEME_ARIA_LABEL: Final = "Theme: Dark"

    NAV_PLAY_TEXT: Final = "Play"
    NAV_PROFILE_TEXT: Final = "Profile"
    NAV_HISTORY_TEXT: Final = "History"
    LOGOUT_BUTTON_TEXT: Final = "Log Out"

    PROFILE_TITLE_TEXT: Final = "Your Profile"
    DISPLAY_NAME_LABEL_TEXT: Final = "Display name"
    SAVE_CHANGES_BUTTON_TEXT: Final = "Save Changes"
    SAVE_SUCCESS_TEXT: Final = "Saved."
    DUPLICATE_NAME_ERROR_TEXT: Final = "Another account already uses this name."
    DELETE_ACCOUNT_BUTTON_TEXT: Final = "Delete Account"

    CREATED_LABEL_TEXT: Final = "Created"
    WINS_LABEL_TEXT: Final = "Win"
    LOSSES_LABEL_TEXT: Final = "Loss"
    DRAWS_LABEL_TEXT: Final = "Draw"
    DEFAULT_STAT_VALUE: Final = "0"
    MIN_DISPLAY_NAME_LENGTH: Final = "2"

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

        self.nav: Locator = page.locator("nav[data-testid='nav']")
        self.avatar: Locator = page.locator("div[data-testid='avatar']")
        self.hello_user: Locator = page.locator("div[data-testid='hello-user']")
        self.nav_play: Locator = page.locator("button[data-testid='nav-play']")
        self.nav_profile: Locator = page.locator("button[data-testid='nav-profile']")
        self.nav_history: Locator = page.locator("button[data-testid='nav-history']")
        self.btn_logout: Locator = page.locator("button[data-testid='btn-logout']")

        self.view_profile: Locator = page.locator("section[data-testid='view-profile']")
        self.profile_title: Locator = page.locator("h2[data-testid='profile-title']")
        self.profile_form: Locator = page.locator("form[data-testid='profile-form']")
        self.input_profile_name: Locator = page.locator("input[data-testid='input-profile-name']")
        self.profile_error: Locator = page.locator("div[data-testid='profile-error']")
        self.profile_message: Locator = page.locator("div[data-testid='profile-message']")
        self.btn_save_profile: Locator = page.locator("button[data-testid='btn-save-profile']")
        self.profile_stats: Locator = page.locator("dl[data-testid='profile-stats']")
        self.profile_created: Locator = page.locator("dd[data-testid='profile-created']")
        self.profile_wins: Locator = page.locator("dd[data-testid='profile-wins']")
        self.profile_losses: Locator = page.locator("dd[data-testid='profile-losses']")
        self.profile_draws: Locator = page.locator("dd[data-testid='profile-draws']")
        self.btn_delete_account: Locator = page.locator("button[data-testid='btn-delete-account']")

        self.initial_visible_elements: tuple[Locator, ...] = (
            self.app,
            self.app_header,
            self.title,
            self.subtitle,
            self.label_language,
            self.select_language,
            self.btn_theme,
            self.root,
            self.nav,
            self.avatar,
            self.hello_user,
            self.nav_play,
            self.nav_profile,
            self.nav_history,
            self.btn_logout,
            self.view_profile,
            self.profile_title,
            self.profile_form,
            self.input_profile_name,
            self.btn_save_profile,
            self.profile_stats,
            self.profile_created,
            self.profile_wins,
            self.profile_losses,
            self.profile_draws,
            self.btn_delete_account,
        )

    def assert_loaded(
        self,
        player_name: str,
        *,
        creation_started_at_ms: int | float | datetime | None = None,
        creation_finished_at_ms: int | float | datetime | None = None,
    ) -> None:
        """Assert the Profile view is visible and contains the expected initial account values."""
        self.assert_all_initial_elements_are_visible()
        self.assert_all_initial_values_are_correct(
            player_name,
            creation_started_at_ms=creation_started_at_ms,
            creation_finished_at_ms=creation_finished_at_ms,
        )

    def assert_all_initial_elements_are_visible(self) -> None:
        for element in self.initial_visible_elements:
            expect(element).to_be_visible()

    def assert_all_initial_values_are_correct(
        self,
        player_name: str,
        *,
        creation_started_at_ms: int | float | datetime | None = None,
        creation_finished_at_ms: int | float | datetime | None = None,
    ) -> None:
        self.assert_header_values_are_correct()
        self.assert_navigation_values_are_correct(player_name)
        self.assert_profile_values_are_correct(player_name)
        self.assert_profile_stats_are_zero()
        self.assert_created_at_is_parseable()

        if creation_started_at_ms is not None and creation_finished_at_ms is not None:
            self.assert_created_at_is_between(creation_started_at_ms, creation_finished_at_ms)

    def assert_header_values_are_correct(self) -> None:
        expect(self.title).to_have_text(self.TITLE_TEXT)
        expect(self.subtitle).to_have_text(self.SUBTITLE_TEXT)
        expect(self.label_language).to_have_text(self.LANGUAGE_LABEL_TEXT)
        expect(self.select_language.locator("option")).to_have_text(list(self.LANGUAGE_OPTIONS))
        expect(self.select_language).to_have_value(self.DEFAULT_LANGUAGE_VALUE)
        expect(self.btn_theme).to_have_text(self.DEFAULT_THEME_BUTTON_TEXT)
        expect(self.btn_theme).to_have_attribute("aria-label", self.DEFAULT_THEME_ARIA_LABEL)

    def assert_navigation_values_are_correct(self, player_name: str) -> None:
        expect(self.avatar).to_have_text(self.expected_avatar_text(player_name))
        expect(self.hello_user).to_have_text(f"Hello, {player_name}")
        expect(self.nav_play).to_have_text(self.NAV_PLAY_TEXT)
        expect(self.nav_play).to_have_attribute("data-active", "false")
        expect(self.nav_profile).to_have_text(self.NAV_PROFILE_TEXT)
        expect(self.nav_profile).to_have_attribute("data-active", "true")
        expect(self.nav_history).to_have_text(self.NAV_HISTORY_TEXT)
        expect(self.nav_history).to_have_attribute("data-active", "false")
        expect(self.btn_logout).to_have_text(self.LOGOUT_BUTTON_TEXT)

    def assert_profile_values_are_correct(self, player_name: str) -> None:
        expect(self.profile_title).to_have_text(self.PROFILE_TITLE_TEXT)
        expect(self.profile_form).to_contain_text(self.DISPLAY_NAME_LABEL_TEXT)
        expect(self.input_profile_name).to_have_value(player_name)
        expect(self.input_profile_name).to_have_attribute("type", "text")
        expect(self.input_profile_name).to_have_attribute("required", "")
        expect(self.input_profile_name).to_have_attribute("minlength", self.MIN_DISPLAY_NAME_LENGTH)
        expect(self.btn_save_profile).to_have_text(self.SAVE_CHANGES_BUTTON_TEXT)
        expect(self.btn_save_profile).to_be_enabled()
        expect(self.profile_stats).to_contain_text(self.CREATED_LABEL_TEXT)
        expect(self.profile_stats).to_contain_text(self.WINS_LABEL_TEXT)
        expect(self.profile_stats).to_contain_text(self.LOSSES_LABEL_TEXT)
        expect(self.profile_stats).to_contain_text(self.DRAWS_LABEL_TEXT)
        expect(self.btn_delete_account).to_have_text(self.DELETE_ACCOUNT_BUTTON_TEXT)
        expect(self.btn_delete_account).to_be_enabled()
        expect(self.profile_error).not_to_be_visible()
        expect(self.profile_message).not_to_be_visible()

    def assert_profile_stats_are_zero(self) -> None:
        self.assert_profile_stats(wins=0, losses=0, draws=0)

    def assert_profile_stats(self, *, wins: int, losses: int, draws: int) -> None:
        expect(self.profile_wins).to_have_text(str(wins))
        expect(self.profile_losses).to_have_text(str(losses))
        expect(self.profile_draws).to_have_text(str(draws))

    def assert_created_at_is_parseable(self) -> None:
        self.get_created_at_timestamp_ms()

    def assert_created_at_is_between(
        self,
        creation_started_at_ms: int | float | datetime,
        creation_finished_at_ms: int | float | datetime,
        *,
        tolerance_ms: int = 1000,
    ) -> None:
        created_at_timestamp_ms = self.get_created_at_timestamp_ms()
        started_at_ms = self.timestamp_ms(creation_started_at_ms)
        finished_at_ms = self.timestamp_ms(creation_finished_at_ms)

        if not started_at_ms - tolerance_ms <= created_at_timestamp_ms <= finished_at_ms + tolerance_ms:
            raise AssertionError(
                "profile-created timestamp was outside the expected account creation window: "
                f"{created_at_timestamp_ms} not between {started_at_ms} and {finished_at_ms}"
            )

    def get_created_at_text(self) -> str:
        return self.profile_created.inner_text().strip()

    def get_created_at_timestamp_ms(self) -> int:
        created_at_text = self.get_created_at_text()
        created_at_timestamp_ms = self.page.evaluate(
            """(createdAtText) => {
                const timestamp = Date.parse(createdAtText);
                return Number.isNaN(timestamp) ? null : timestamp;
            }""",
            created_at_text,
        )

        if created_at_timestamp_ms is None:
            raise AssertionError(f"profile-created value is not parseable as a date: {created_at_text!r}")

        return int(created_at_timestamp_ms)

    def fill_display_name(self, display_name: str) -> None:
        self.input_profile_name.fill(display_name)

    def save_profile_changes(self) -> None:
        self.btn_save_profile.click()

    def update_display_name(self, display_name: str) -> None:
        self.fill_display_name(display_name)
        self.save_profile_changes()

    def assert_profile_saved_message(self) -> None:
        expect(self.profile_message).to_be_visible()
        expect(self.profile_message).to_have_attribute("role", "status")
        expect(self.profile_message).to_have_text(self.SAVE_SUCCESS_TEXT)
        expect(self.profile_error).not_to_be_visible()

    def assert_display_name_was_updated(self, display_name: str) -> None:
        expect(self.input_profile_name).to_have_value(display_name)
        self.assert_navigation_values_are_correct(display_name)
        self.assert_profile_saved_message()

    def assert_profile_error_message(self, expected_text: str) -> None:
        expect(self.profile_error).to_be_visible()
        expect(self.profile_error).to_have_attribute("role", "alert")
        expect(self.profile_error).to_have_text(expected_text)
        expect(self.profile_message).not_to_be_visible()

    def assert_duplicate_name_error_message(self) -> None:
        self.assert_profile_error_message(self.DUPLICATE_NAME_ERROR_TEXT)

    def assert_display_name_input_is_invalid(self) -> None:
        if self.input_profile_name.evaluate("input => input.validity.valid"):
            raise AssertionError("expected input-profile-name to be invalid")

    def assert_display_name_input_is_valid(self) -> None:
        if not self.input_profile_name.evaluate("input => input.validity.valid"):
            validation_message = self.get_display_name_validation_message()
            raise AssertionError(f"expected input-profile-name to be valid, got: {validation_message!r}")

    def get_display_name_validation_message(self) -> str:
        return self.input_profile_name.evaluate("input => input.validationMessage")

    def open_play_view(self) -> None:
        self.nav_play.click()

    def open_history_view(self) -> None:
        self.nav_history.click()

    def delete_account(self) -> None:
        self.btn_delete_account.click()

    def log_out(self) -> None:
        self.btn_logout.click()

    @staticmethod
    def current_browser_timestamp_ms(page: Page) -> int:
        return int(page.evaluate("Date.now()"))

    @staticmethod
    def timestamp_ms(value: int | float | datetime) -> int:
        if isinstance(value, datetime):
            return int(value.timestamp() * 1000)
        return int(value)

    @staticmethod
    def expected_avatar_text(player_name: str) -> str:
        stripped_name = player_name.strip()
        return stripped_name[0].upper() if stripped_name else "?"
