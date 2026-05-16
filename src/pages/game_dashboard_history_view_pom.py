from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Final

from playwright.sync_api import Locator, Page, expect


class GameDashboardHistoryViewPage:
    """Page object for the game dashboard History view."""

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

    HISTORY_TITLE_TEXT: Final = "Game History"
    HISTORY_EMPTY_TEXT: Final = "No games yet. Play one!"
    HISTORY_TABLE_HEADERS: Final = ("Date", "Difficulty", "Result")
    CLEAR_HISTORY_BUTTON_TEXT: Final = "Clear History"
    VALID_DIFFICULTIES: Final = ("easy", "medium", "hard")
    VALID_RESULTS: Final = ("win", "loss", "draw")

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

        self.view_history: Locator = page.locator("section[data-testid='view-history']")
        self.history_title: Locator = page.locator("h2[data-testid='history-title']")
        self.history_empty: Locator = page.locator("p[data-testid='history-empty']")
        self.history_table: Locator = page.locator("table[data-testid='history-table']")
        self.history_rows: Locator = page.locator("tr[data-testid^='history-row-']")
        self.btn_clear_history: Locator = page.locator("button[data-testid='btn-clear-history']")

        self.common_visible_elements: tuple[Locator, ...] = (
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
            self.view_history,
            self.history_title,
        )

    def assert_empty_loaded(self, player_name: str) -> None:
        """Assert the History view is loaded with no completed match records."""
        self.assert_common_elements_are_visible()
        self.assert_common_values_are_correct(player_name)
        self.assert_history_is_empty()

    def assert_populated_loaded(
        self,
        player_name: str,
        expected_records: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        """Assert the History view is loaded with completed match records."""
        self.assert_common_elements_are_visible()
        self.assert_common_values_are_correct(player_name)
        self.assert_history_is_populated()

        if expected_records is not None:
            self.assert_history_records(expected_records)

    def assert_common_elements_are_visible(self) -> None:
        for element in self.common_visible_elements:
            expect(element).to_be_visible()

    def assert_common_values_are_correct(self, player_name: str) -> None:
        self.assert_header_values_are_correct()
        self.assert_navigation_values_are_correct(player_name)
        expect(self.history_title).to_have_text(self.HISTORY_TITLE_TEXT)

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
        expect(self.nav_profile).to_have_attribute("data-active", "false")
        expect(self.nav_history).to_have_text(self.NAV_HISTORY_TEXT)
        expect(self.nav_history).to_have_attribute("data-active", "true")
        expect(self.btn_logout).to_have_text(self.LOGOUT_BUTTON_TEXT)

    def assert_history_is_empty(self) -> None:
        expect(self.history_empty).to_be_visible()
        expect(self.history_empty).to_have_text(self.HISTORY_EMPTY_TEXT)
        expect(self.history_table).to_have_count(0)
        expect(self.history_rows).to_have_count(0)
        expect(self.btn_clear_history).to_have_count(0)

    def assert_history_is_populated(self) -> None:
        expect(self.history_empty).to_have_count(0)
        expect(self.history_table).to_be_visible()
        expect(self.history_table.locator("th")).to_have_text(list(self.HISTORY_TABLE_HEADERS))
        expect(self.history_rows.first).to_be_visible()
        expect(self.btn_clear_history).to_be_visible()
        expect(self.btn_clear_history).to_have_text(self.CLEAR_HISTORY_BUTTON_TEXT)
        expect(self.btn_clear_history).to_be_enabled()

    def assert_history_records(self, expected_records: Sequence[Mapping[str, Any]]) -> None:
        expect(self.history_rows).to_have_count(len(expected_records))

        for row_index, expected_record in enumerate(expected_records):
            self.assert_history_record(row_index, expected_record)

    def assert_history_record(self, row_index: int, expected_record: Mapping[str, Any]) -> None:
        difficulty = str(expected_record["difficulty"])
        result = str(expected_record["result"])
        self.validate_difficulty(difficulty)
        self.validate_result(result)

        row = self.history_row(row_index)
        expect(row).to_be_visible()
        expect(row).to_have_attribute("data-result", result)
        expect(self.history_difficulty(row_index)).to_have_text(self.display_difficulty(difficulty))
        expect(self.history_result(row_index)).to_have_text(self.display_result(result))

        if "finishedAt" in expected_record:
            expect(self.history_date(row_index)).to_have_text(self.format_history_date(expected_record["finishedAt"]))
            self.assert_history_date_is_parseable(row_index)

    def assert_history_date_is_parseable(self, row_index: int) -> None:
        self.get_history_date_timestamp_ms(row_index)

    def assert_history_dates_are_parseable(self) -> None:
        for row_index in range(self.get_history_row_count()):
            self.assert_history_date_is_parseable(row_index)

    def get_history_row_count(self) -> int:
        return self.history_rows.count()

    def get_history_records_from_page(self) -> list[dict[str, str]]:
        records: list[dict[str, str]] = []
        for row_index in range(self.get_history_row_count()):
            records.append(
                {
                    "date": self.history_date(row_index).inner_text().strip(),
                    "difficulty": self.history_difficulty(row_index).inner_text().strip(),
                    "result": self.history_result(row_index).inner_text().strip(),
                    "data_result": self.history_row(row_index).get_attribute("data-result") or "",
                }
            )
        return records

    def get_history_date_timestamp_ms(self, row_index: int) -> int:
        date_text = self.history_date(row_index).inner_text().strip()
        timestamp_ms = self.page.evaluate(
            """(dateText) => {
                const timestamp = Date.parse(dateText);
                return Number.isNaN(timestamp) ? null : timestamp;
            }""",
            date_text,
        )

        if timestamp_ms is None:
            raise AssertionError(f"history-date-{row_index} is not parseable as a date: {date_text!r}")

        return int(timestamp_ms)

    def history_row(self, row_index: int) -> Locator:
        self.validate_row_index(row_index)
        return self.page.locator(f"tr[data-testid='history-row-{row_index}']")

    def history_date(self, row_index: int) -> Locator:
        self.validate_row_index(row_index)
        return self.page.locator(f"td[data-testid='history-date-{row_index}']")

    def history_difficulty(self, row_index: int) -> Locator:
        self.validate_row_index(row_index)
        return self.page.locator(f"td[data-testid='history-difficulty-{row_index}']")

    def history_result(self, row_index: int) -> Locator:
        self.validate_row_index(row_index)
        return self.page.locator(f"td[data-testid='history-result-{row_index}']")

    def clear_history(self, *, confirm: bool = True) -> None:
        self.page.once("dialog", lambda dialog: dialog.accept() if confirm else dialog.dismiss())
        self.btn_clear_history.click()

    def open_play_view(self) -> None:
        self.nav_play.click()

    def open_profile_view(self) -> None:
        self.nav_profile.click()

    def log_out(self) -> None:
        self.btn_logout.click()

    def format_history_date(self, value: Any) -> str:
        timestamp_ms = self.timestamp_ms(value)
        return str(self.page.evaluate("(timestamp) => new Date(timestamp).toLocaleString('en-US')", timestamp_ms))

    @classmethod
    def validate_difficulty(cls, difficulty: str) -> None:
        if difficulty not in cls.VALID_DIFFICULTIES:
            raise ValueError(f"difficulty must be one of {cls.VALID_DIFFICULTIES}")

    @classmethod
    def validate_result(cls, result: str) -> None:
        if result not in cls.VALID_RESULTS:
            raise ValueError(f"result must be one of {cls.VALID_RESULTS}")

    @staticmethod
    def validate_row_index(row_index: int) -> None:
        if row_index < 0:
            raise ValueError("row_index must be 0 or greater")

    @staticmethod
    def display_difficulty(difficulty: str) -> str:
        return difficulty.capitalize()

    @staticmethod
    def display_result(result: str) -> str:
        return result.capitalize()

    @staticmethod
    def timestamp_ms(value: Any) -> int:
        if isinstance(value, datetime):
            return int(value.timestamp() * 1000)
        return int(value)

    @staticmethod
    def expected_avatar_text(player_name: str) -> str:
        stripped_name = player_name.strip()
        return stripped_name[0].upper() if stripped_name else "?"
