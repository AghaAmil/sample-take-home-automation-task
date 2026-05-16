from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Final

from playwright.sync_api import Locator, Page, expect


class GameDashboardViewPlayPage:
    """Page object for the initial game dashboard Play view."""

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

    DIFFICULTY_LABEL_TEXT: Final = "Difficulty"
    DIFFICULTY_OPTIONS: Final = ("Easy", "Medium", "Hard")
    DEFAULT_DIFFICULTY_VALUE: Final = "easy"
    STATUS_TEXT: Final = "Your turn (X)"
    STATUS_DATA_VALUE: Final = "your-turn"
    BOARD_ARIA_LABEL: Final = "Tic-Tac-Toe board"
    EMPTY_CELL_STATE: Final = "empty"
    PLAYER_CELL_STATE: Final = "x"
    COMPUTER_CELL_STATE: Final = "o"
    HINT_CELL_CLASS: Final = "is-hint"
    EMPTY_CELL_ARIA_DISABLED: Final = "false"
    OCCUPIED_CELL_ARIA_DISABLED: Final = "true"
    NEW_GAME_BUTTON_TEXT: Final = "New Game"
    HINT_BUTTON_TEXT: Final = "Get Hint"
    RESET_BUTTON_TEXT: Final = "Reset"

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

        self.view_play: Locator = page.locator("section[data-testid='view-play']")
        self.toolbar: Locator = page.locator("section[data-testid='toolbar']")
        self.label_difficulty: Locator = page.locator("span[data-testid='label-difficulty']")
        self.select_difficulty: Locator = page.locator("select[data-testid='select-difficulty']")
        self.status: Locator = page.locator("div[data-testid='status']")
        self.board: Locator = page.locator("div[data-testid='board']")
        self.cells: tuple[Locator, ...] = tuple(
            page.locator(f"button[data-testid='cell-{cell_index}']") for cell_index in range(9)
        )
        self.hint_cell: Locator = page.locator("button[data-testid^='cell-'].is-hint")
        self.actions: Locator = page.locator("div[data-testid='actions']")
        self.btn_new: Locator = page.locator("button[data-testid='btn-new']")
        self.btn_hint: Locator = page.locator("button[data-testid='btn-hint']")
        self.btn_reset: Locator = page.locator("button[data-testid='btn-reset']")

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
            self.view_play,
            self.toolbar,
            self.label_difficulty,
            self.select_difficulty,
            self.status,
            self.board,
            *self.cells,
            self.actions,
            self.btn_new,
            self.btn_hint,
            self.btn_reset,
        )

    def assert_loaded(self, player_name: str) -> None:
        """Assert the initial Play view is visible and contains the expected values."""
        self.assert_all_initial_elements_are_visible()
        self.assert_all_initial_values_are_correct(player_name)

    def assert_all_initial_elements_are_visible(self) -> None:
        for element in self.initial_visible_elements:
            expect(element).to_be_visible()

    def assert_all_initial_values_are_correct(self, player_name: str) -> None:
        self.assert_header_values_are_correct()
        self.assert_navigation_values_are_correct(player_name)
        self.assert_play_view_values_are_correct()

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
        expect(self.nav_play).to_have_attribute("data-active", "true")
        expect(self.nav_profile).to_have_text(self.NAV_PROFILE_TEXT)
        expect(self.nav_profile).to_have_attribute("data-active", "false")
        expect(self.nav_history).to_have_text(self.NAV_HISTORY_TEXT)
        expect(self.nav_history).to_have_attribute("data-active", "false")
        expect(self.btn_logout).to_have_text(self.LOGOUT_BUTTON_TEXT)

    def assert_play_view_values_are_correct(self) -> None:
        expect(self.label_difficulty).to_have_text(self.DIFFICULTY_LABEL_TEXT)
        expect(self.select_difficulty.locator("option")).to_have_text(list(self.DIFFICULTY_OPTIONS))
        expect(self.select_difficulty).to_have_value(self.DEFAULT_DIFFICULTY_VALUE)
        expect(self.status).to_have_text(self.STATUS_TEXT)
        expect(self.status).to_have_attribute("role", "status")
        expect(self.status).to_have_attribute("data-status", self.STATUS_DATA_VALUE)
        expect(self.board).to_have_attribute("role", "grid")
        expect(self.board).to_have_attribute("aria-label", self.BOARD_ARIA_LABEL)
        expect(self.btn_new).to_have_text(self.NEW_GAME_BUTTON_TEXT)
        expect(self.btn_new).to_be_enabled()
        expect(self.btn_hint).to_have_text(self.HINT_BUTTON_TEXT)
        expect(self.btn_hint).to_be_enabled()
        expect(self.btn_reset).to_have_text(self.RESET_BUTTON_TEXT)
        expect(self.btn_reset).to_be_enabled()
        self.assert_initial_board_values_are_correct()

    def assert_initial_board_values_are_correct(self) -> None:
        for cell_index, cell in enumerate(self.cells):
            self.assert_cell_is_empty(
                cell_index,
                expected_aria_disabled=self.EMPTY_CELL_ARIA_DISABLED,
                expected_enabled=True,
            )

    def cell_by_index(self, cell_index: int) -> Locator:
        self.validate_cell_index(cell_index)
        return self.cells[cell_index]

    def select_cell(self, cell_index: int) -> None:
        self.cell_by_index(cell_index).click()

    def assert_cell_is_empty(
        self,
        cell_index: int,
        *,
        expected_aria_disabled: str | None = None,
        expected_enabled: bool | None = None,
    ) -> None:
        cell = self.cell_by_index(cell_index)
        expect(cell).to_have_text("")
        expect(cell).to_have_attribute("role", "gridcell")
        expect(cell).to_have_attribute("data-index", str(cell_index))
        expect(cell).to_have_attribute("data-state", self.EMPTY_CELL_STATE)
        expect(cell).to_have_attribute("aria-label", self.expected_cell_aria_label(cell_index, self.EMPTY_CELL_STATE))

        if expected_aria_disabled is not None:
            expect(cell).to_have_attribute("aria-disabled", expected_aria_disabled)

        if expected_enabled is True:
            expect(cell).to_be_enabled()
        elif expected_enabled is False:
            expect(cell).to_be_disabled()

    def assert_cell_occupied_by_user(self, cell_index: int) -> None:
        self.assert_cell_occupied_by_marker(cell_index, self.PLAYER_CELL_STATE)

    def assert_cell_occupied_by_computer(self, cell_index: int) -> None:
        self.assert_cell_occupied_by_marker(cell_index, self.COMPUTER_CELL_STATE)

    def assert_cell_occupied_by_marker(self, cell_index: int, marker: str) -> None:
        self.validate_cell_marker(marker)

        cell = self.cell_by_index(cell_index)
        expected_text = marker.upper()

        expect(cell).to_have_text(expected_text)
        expect(cell).to_have_attribute("role", "gridcell")
        expect(cell).to_have_attribute("data-index", str(cell_index))
        expect(cell).to_have_attribute("data-state", marker)
        expect(cell).to_have_attribute("aria-label", self.expected_cell_aria_label(cell_index, marker))
        expect(cell).to_have_attribute("aria-disabled", self.OCCUPIED_CELL_ARIA_DISABLED)
        expect(cell).to_be_disabled()

    def assert_cell_is_highlighted_by_hint(self, cell_index: int) -> None:
        cell = self.cell_by_index(cell_index)
        self.assert_cell_is_empty(
            cell_index,
            expected_aria_disabled=self.EMPTY_CELL_ARIA_DISABLED,
            expected_enabled=True,
        )
        expect(cell).to_have_class(re.compile(rf"(^|\s){self.HINT_CELL_CLASS}(\s|$)"))

    def assert_no_cell_is_highlighted_by_hint(self) -> None:
        expect(self.hint_cell).to_have_count(0)

    def assert_exact_occupied_cells(
        self,
        user_cell_indexes: set[int] | tuple[int, ...] | list[int],
        computer_cell_indexes: set[int] | tuple[int, ...] | list[int],
    ) -> None:
        user_cells = self.normalized_cell_indexes(user_cell_indexes)
        computer_cells = self.normalized_cell_indexes(computer_cell_indexes)
        overlapping_cells = user_cells & computer_cells
        if overlapping_cells:
            raise ValueError(f"cells cannot be occupied by both players: {sorted(overlapping_cells)}")

        for cell_index in range(9):
            if cell_index in user_cells:
                self.assert_cell_occupied_by_user(cell_index)
            elif cell_index in computer_cells:
                self.assert_cell_occupied_by_computer(cell_index)
            else:
                self.assert_cell_is_empty(cell_index)

    def assert_current_board_state(self, expected_states: Sequence[str]) -> None:
        if len(expected_states) != 9:
            raise ValueError("expected_states must include exactly 9 cell states")

        for cell_index, expected_state in enumerate(expected_states):
            self.validate_cell_state(expected_state)
            if expected_state == self.PLAYER_CELL_STATE:
                self.assert_cell_occupied_by_user(cell_index)
            elif expected_state == self.COMPUTER_CELL_STATE:
                self.assert_cell_occupied_by_computer(cell_index)
            else:
                self.assert_cell_is_empty(cell_index)

    def get_current_board_state(self) -> list[str]:
        return [cell.get_attribute("data-state") or self.EMPTY_CELL_STATE for cell in self.cells]

    def get_hint_highlighted_cell_index(self) -> int | None:
        highlighted_cells = self.get_hint_highlighted_cell_indexes()
        if not highlighted_cells:
            return None

        if len(highlighted_cells) > 1:
            raise AssertionError(f"expected one highlighted hint cell, found {highlighted_cells}")

        return highlighted_cells[0]

    def get_hint_highlighted_cell_indexes(self) -> list[int]:
        highlighted_cell_indexes: list[int] = []

        for cell_index, cell in enumerate(self.cells):
            class_name = cell.get_attribute("class") or ""
            if self.HINT_CELL_CLASS in class_name.split():
                highlighted_cell_indexes.append(cell_index)

        return highlighted_cell_indexes

    def wait_for_hint_highlighted_cell_index(self, timeout_ms: int = 1000) -> int:
        self.page.wait_for_function(
            """() => Boolean(document.querySelector("button[data-testid^='cell-'].is-hint"))""",
            timeout=timeout_ms,
        )

        highlighted_cell_index = self.get_hint_highlighted_cell_index()
        if highlighted_cell_index is None:
            raise AssertionError("expected one highlighted hint cell, found none")

        self.assert_cell_is_highlighted_by_hint(highlighted_cell_index)
        return highlighted_cell_index

    def get_occupied_cell_indexes_by_marker(self, marker: str) -> list[int]:
        self.validate_cell_marker(marker)
        occupied_cell_indexes: list[int] = []

        for cell_index, cell in enumerate(self.cells):
            if cell.get_attribute("data-state") == marker:
                occupied_cell_indexes.append(cell_index)

        return occupied_cell_indexes

    def get_user_occupied_cell_indexes(self) -> list[int]:
        return self.get_occupied_cell_indexes_by_marker(self.PLAYER_CELL_STATE)

    def get_computer_occupied_cell_indexes(self) -> list[int]:
        return self.get_occupied_cell_indexes_by_marker(self.COMPUTER_CELL_STATE)

    def change_difficulty(self, difficulty_value: str) -> None:
        self.select_difficulty.select_option(difficulty_value)

    def start_new_game(self) -> None:
        self.btn_new.click()

    def get_hint(self) -> None:
        self.btn_hint.click()

    def get_hint_highlighted_cell(self, timeout_ms: int = 1000) -> int:
        self.get_hint()
        return self.wait_for_hint_highlighted_cell_index(timeout_ms=timeout_ms)

    def reset_game(self) -> None:
        self.btn_reset.click()

    def open_profile_view(self) -> None:
        self.nav_profile.click()

    def open_history_view(self) -> None:
        self.nav_history.click()

    def log_out(self) -> None:
        self.btn_logout.click()

    @staticmethod
    def validate_cell_index(cell_index: int) -> None:
        if cell_index not in range(9):
            raise ValueError("cell_index must be between 0 and 8")

    @classmethod
    def validate_cell_marker(cls, marker: str) -> None:
        if marker not in {cls.PLAYER_CELL_STATE, cls.COMPUTER_CELL_STATE}:
            raise ValueError("marker must be 'x' or 'o'")

    @classmethod
    def validate_cell_state(cls, state: str) -> None:
        if state not in {cls.PLAYER_CELL_STATE, cls.COMPUTER_CELL_STATE, cls.EMPTY_CELL_STATE}:
            raise ValueError("state must be 'x', 'o', or 'empty'")

    @classmethod
    def normalized_cell_indexes(cls, cell_indexes: set[int] | tuple[int, ...] | list[int]) -> set[int]:
        normalized_indexes = set(cell_indexes)
        for cell_index in normalized_indexes:
            cls.validate_cell_index(cell_index)
        return normalized_indexes

    @staticmethod
    def expected_avatar_text(player_name: str) -> str:
        stripped_name = player_name.strip()
        return stripped_name[0].upper() if stripped_name else "?"

    @staticmethod
    def expected_empty_cell_aria_label(cell_index: int) -> str:
        return GameDashboardViewPlayPage.expected_cell_aria_label(
            cell_index, GameDashboardViewPlayPage.EMPTY_CELL_STATE
        )

    @staticmethod
    def expected_cell_aria_label(cell_index: int, marker: str) -> str:
        row = (cell_index // 3) + 1
        column = (cell_index % 3) + 1
        marker_label = marker.upper() if marker in {"x", "o"} else "empty"
        return f"row {row}, column {column}, {marker_label}"
