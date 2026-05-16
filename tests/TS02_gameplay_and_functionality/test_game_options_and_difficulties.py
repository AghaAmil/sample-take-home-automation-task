from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Literal

from playwright.sync_api import Page, TimeoutError, expect

from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


CellState = Literal["empty", "x", "o"]


@dataclass(frozen=True)
class MatchPlan:
    human_moves: tuple[int, ...]
    computer_moves: tuple[int, ...]
    random_values: tuple[float, ...]
    result: str
    status_text: str
    status_value: str


MEDIUM_HUMAN_WIN: Final = MatchPlan(
    human_moves=(0, 2, 4, 8),
    computer_moves=(1, 3, 6),
    random_values=(0.0125, 0.016666666666666666),
    result="win",
    status_text="You win!",
    status_value="human",
)


def test_game_options_difficulties_hint_and_medium_match(
    app_page: Page,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
    logged_in_player_name: str,
) -> None:
    play_page.assert_loaded(logged_in_player_name)

    assert_reset_behavior(app_page, play_page, logged_in_player_name)
    assert_new_game_behavior(app_page, play_page, logged_in_player_name)
    assert_active_game_difficulty_confirmation_paths(app_page, play_page, logged_in_player_name)
    assert_hint_button_smoke(play_page)

    start_new_game_and_assert_empty(play_page, expected_difficulty="medium")
    medium_record = play_medium_match(app_page, play_page, logged_in_player_name)

    play_page.open_profile_view()
    assert_profile_stats_after_medium_win(profile_page, logged_in_player_name)

    profile_page.open_history_view()
    history_page.assert_populated_loaded(logged_in_player_name, expected_records=[medium_record])


def assert_reset_behavior(
    page: Page,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> None:
    play_one_turn(page, play_page, human_cell_index=0, computer_cell_index=1)

    play_page.reset_game()
    assert_game_is_empty(play_page, expected_difficulty=GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE)
    assert_no_saved_history(page, player_name)


def assert_new_game_behavior(
    page: Page,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> None:
    play_one_turn(page, play_page, human_cell_index=4, computer_cell_index=0)

    play_page.start_new_game()
    assert_game_is_empty(play_page, expected_difficulty=GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE)
    assert_no_saved_history(page, player_name)


def assert_active_game_difficulty_confirmation_paths(
    page: Page,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> None:
    active_board_state = play_one_turn(page, play_page, human_cell_index=0, computer_cell_index=1)

    page.once("dialog", lambda dialog: dialog.dismiss())
    play_page.change_difficulty("medium")
    expect(play_page.select_difficulty).to_have_value(GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE)
    play_page.assert_current_board_state(active_board_state)
    assert_no_saved_history(page, player_name)

    page.once("dialog", lambda dialog: dialog.accept())
    play_page.change_difficulty("medium")
    assert_game_is_empty(play_page, expected_difficulty="medium")
    assert_saved_difficulty(page, player_name, expected_difficulty="medium")
    assert_no_saved_history(page, player_name)


def assert_hint_button_smoke(play_page: GameDashboardViewPlayPage) -> None:
    expect(play_page.btn_hint).to_be_enabled()
    play_page.get_hint()

    highlighted_cell_index = get_optional_hint_highlighted_cell_index(play_page)
    if highlighted_cell_index is not None:
        play_page.assert_cell_is_highlighted_by_hint(highlighted_cell_index)

    play_page.assert_current_board_state(initial_board_state())


def play_medium_match(
    page: Page,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> dict[str, Any]:
    expect(play_page.select_difficulty).to_have_value("medium")
    install_deterministic_random(page, list(MEDIUM_HUMAN_WIN.random_values))

    expected_states = initial_board_state()
    match_started_at_ms = current_browser_timestamp_ms(page)

    for turn_index, human_cell_index in enumerate(MEDIUM_HUMAN_WIN.human_moves):
        play_page.assert_cell_is_empty(
            human_cell_index,
            expected_aria_disabled=GameDashboardViewPlayPage.EMPTY_CELL_ARIA_DISABLED,
            expected_enabled=True,
        )
        play_page.select_cell(human_cell_index)
        expected_states[human_cell_index] = GameDashboardViewPlayPage.PLAYER_CELL_STATE

        if turn_index < len(MEDIUM_HUMAN_WIN.computer_moves):
            computer_cell_index = MEDIUM_HUMAN_WIN.computer_moves[turn_index]
            expected_states[computer_cell_index] = GameDashboardViewPlayPage.COMPUTER_CELL_STATE
            wait_for_board_state(page, expected_states)
            play_page.assert_current_board_state(expected_states)

            if turn_index == len(MEDIUM_HUMAN_WIN.human_moves) - 1:
                assert_match_finished(play_page, MEDIUM_HUMAN_WIN)
            else:
                assert_user_turn(play_page)
        else:
            wait_for_board_state(page, expected_states)
            play_page.assert_current_board_state(expected_states)
            assert_match_finished(play_page, MEDIUM_HUMAN_WIN)

    match_finished_at_ms = current_browser_timestamp_ms(page)
    record = get_latest_history_record(page, player_name)
    assert_history_record(
        record,
        expected_result=MEDIUM_HUMAN_WIN.result,
        expected_difficulty="medium",
        started_at_ms=match_started_at_ms,
        finished_at_ms=match_finished_at_ms,
    )
    return record


def play_one_turn(
    page: Page,
    play_page: GameDashboardViewPlayPage,
    *,
    human_cell_index: int,
    computer_cell_index: int,
) -> list[CellState]:
    expected_states = initial_board_state()
    install_deterministic_random(page, random_values_for_easy_computer_move(human_cell_index, computer_cell_index))

    play_page.select_cell(human_cell_index)
    expected_states[human_cell_index] = GameDashboardViewPlayPage.PLAYER_CELL_STATE
    expected_states[computer_cell_index] = GameDashboardViewPlayPage.COMPUTER_CELL_STATE
    wait_for_board_state(page, expected_states)
    play_page.assert_current_board_state(expected_states)
    assert_user_turn(play_page)
    return expected_states


def start_new_game_and_assert_empty(
    play_page: GameDashboardViewPlayPage,
    *,
    expected_difficulty: str,
) -> None:
    play_page.start_new_game()
    assert_game_is_empty(play_page, expected_difficulty=expected_difficulty)


def assert_game_is_empty(
    play_page: GameDashboardViewPlayPage,
    *,
    expected_difficulty: str,
) -> None:
    expect(play_page.select_difficulty).to_have_value(expected_difficulty)
    expect(play_page.status).to_have_text(GameDashboardViewPlayPage.STATUS_TEXT)
    expect(play_page.status).to_have_attribute("data-status", GameDashboardViewPlayPage.STATUS_DATA_VALUE)
    play_page.assert_initial_board_values_are_correct()
    play_page.assert_no_cell_is_highlighted_by_hint()


def assert_user_turn(play_page: GameDashboardViewPlayPage) -> None:
    expect(play_page.status).to_have_text(GameDashboardViewPlayPage.STATUS_TEXT)
    expect(play_page.status).to_have_attribute("data-status", GameDashboardViewPlayPage.STATUS_DATA_VALUE)
    expect(play_page.btn_hint).to_be_enabled()


def assert_match_finished(play_page: GameDashboardViewPlayPage, match_plan: MatchPlan) -> None:
    expect(play_page.status).to_have_text(match_plan.status_text)
    expect(play_page.status).to_have_attribute("data-status", match_plan.status_value)
    expect(play_page.btn_hint).to_be_disabled()
    expect(play_page.btn_new).to_be_enabled()
    expect(play_page.btn_reset).to_be_enabled()


def assert_profile_stats_after_medium_win(
    profile_page: GameDashboardProfileViewPage,
    player_name: str,
) -> None:
    profile_page.assert_all_initial_elements_are_visible()
    profile_page.assert_header_values_are_correct()
    profile_page.assert_navigation_values_are_correct(player_name)
    profile_page.assert_profile_values_are_correct(player_name)
    profile_page.assert_profile_stats(wins=1, losses=0, draws=0)


def assert_history_record(
    record: dict[str, Any],
    *,
    expected_result: str,
    expected_difficulty: str,
    started_at_ms: int,
    finished_at_ms: int,
) -> None:
    if record["result"] != expected_result:
        raise AssertionError(f"expected history result {expected_result!r}, got {record['result']!r}")

    if record["difficulty"] != expected_difficulty:
        raise AssertionError(f"expected history difficulty {expected_difficulty!r}, got {record['difficulty']!r}")

    assert_timestamp_between(
        timestamp_ms=record["finishedAt"],
        started_at_ms=started_at_ms,
        finished_at_ms=finished_at_ms,
        tolerance_ms=1000,
    )


def get_optional_hint_highlighted_cell_index(play_page: GameDashboardViewPlayPage) -> int | None:
    try:
        return play_page.wait_for_hint_highlighted_cell_index(timeout_ms=700)
    except TimeoutError:
        return None


def get_latest_history_record(page: Page, player_name: str) -> dict[str, Any]:
    record = page.evaluate(
        """(playerName) => {
            const users = JSON.parse(localStorage.getItem("ttt:users") || "{}");
            const account = users[playerName.trim().toLowerCase()];
            return account?.history?.[0] ?? null;
        }""",
        player_name,
    )

    if not record:
        raise AssertionError(f"no history record was saved for {player_name!r}")

    return record


def assert_no_saved_history(page: Page, player_name: str) -> None:
    history_count = page.evaluate(
        """(playerName) => {
            const users = JSON.parse(localStorage.getItem("ttt:users") || "{}");
            return users[playerName.trim().toLowerCase()]?.history?.length ?? 0;
        }""",
        player_name,
    )

    if history_count != 0:
        raise AssertionError(f"expected no saved history records, got {history_count}")


def assert_saved_difficulty(page: Page, player_name: str, *, expected_difficulty: str) -> None:
    saved_difficulty = page.evaluate(
        """(playerName) => {
            const users = JSON.parse(localStorage.getItem("ttt:users") || "{}");
            return users[playerName.trim().toLowerCase()]?.difficulty ?? null;
        }""",
        player_name,
    )

    if saved_difficulty != expected_difficulty:
        raise AssertionError(f"expected saved difficulty {expected_difficulty!r}, got {saved_difficulty!r}")


def install_deterministic_random(page: Page, random_values: list[float]) -> None:
    page.evaluate(
        """(values) => {
            let nextIndex = 0;
            Math.random = () => values[nextIndex++] ?? 0;
        }""",
        random_values,
    )


def random_values_for_easy_computer_move(human_cell_index: int, computer_cell_index: int) -> list[float]:
    empty_cells = [index for index in range(9) if index != human_cell_index]
    empty_cell_offset = empty_cells.index(computer_cell_index)
    return [(empty_cell_offset + 0.1) / len(empty_cells)]


def wait_for_board_state(page: Page, expected_states: list[CellState]) -> None:
    page.wait_for_function(
        """(expectedStates) => {
            const cells = [...document.querySelectorAll("button[data-testid^='cell-']")];
            return cells.length === expectedStates.length
                && cells.every((cell, index) => cell.dataset.state === expectedStates[index]);
        }""",
        arg=expected_states,
    )


def initial_board_state() -> list[CellState]:
    return [GameDashboardViewPlayPage.EMPTY_CELL_STATE] * 9


def current_browser_timestamp_ms(page: Page) -> int:
    return int(page.evaluate("Date.now()"))


def assert_timestamp_between(
    *,
    timestamp_ms: int | float,
    started_at_ms: int,
    finished_at_ms: int,
    tolerance_ms: int,
) -> None:
    if not started_at_ms - tolerance_ms <= timestamp_ms <= finished_at_ms + tolerance_ms:
        raise AssertionError(f"{timestamp_ms} was not between {started_at_ms} and {finished_at_ms}")
