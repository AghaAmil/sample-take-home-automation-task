from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Literal

from playwright.sync_api import Page, expect

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


CellState = Literal["empty", "x", "o"]
MatchResult = Literal["win", "loss", "draw"]


@dataclass(frozen=True)
class MatchPlan:
    result: MatchResult
    human_moves: tuple[int, ...]
    computer_moves: tuple[int, ...]
    final_status_text: str
    final_status_value: str


MATCH_PLANS: Final = (
    MatchPlan(
        result="loss",
        human_moves=(0, 1, 6),
        computer_moves=(3, 4, 5),
        final_status_text="Computer wins.",
        final_status_value="computer",
    ),
    MatchPlan(
        result="draw",
        human_moves=(0, 2, 4, 5, 7),
        computer_moves=(1, 3, 6, 8),
        final_status_text="Draw.",
        final_status_value="draw",
    ),
    MatchPlan(
        result="win",
        human_moves=(0, 1, 2),
        computer_moves=(3, 4),
        final_status_text="You win!",
        final_status_value="human",
    ),
)


def test_play_deterministic_matches_and_verify_profile_and_history(
    app_page: Page,
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
    player_name: str,
) -> None:
    create_account(account_creation_page, play_page, player_name)
    play_page.assert_loaded(player_name)

    expected_history_records: list[dict[str, Any]] = []
    completed_results: list[MatchResult] = []

    for match_index, match_plan in enumerate(MATCH_PLANS):
        if match_index > 0:
            start_new_default_game(play_page)

        record = play_match(app_page, play_page, player_name, match_plan)
        completed_results.append(match_plan.result)
        expected_history_records.insert(0, record)

    if completed_results != ["loss", "draw", "win"]:
        raise AssertionError(f"unexpected completed result order: {completed_results}")

    play_page.open_profile_view()
    assert_profile_after_matches(profile_page, player_name)

    profile_page.open_history_view()
    history_page.assert_populated_loaded(player_name, expected_records=expected_history_records)


def create_account(
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> None:
    account_creation_page.assert_loaded()
    account_creation_page.fill_player_name(player_name)
    account_creation_page.submit_create_account()
    expect(play_page.view_play).to_be_visible()


def start_new_default_game(play_page: GameDashboardViewPlayPage) -> None:
    play_page.start_new_game()
    expect(play_page.status).to_have_attribute("data-status", GameDashboardViewPlayPage.STATUS_DATA_VALUE)
    expect(play_page.select_difficulty).to_have_value(GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE)
    play_page.assert_initial_board_values_are_correct()
    play_page.assert_no_cell_is_highlighted_by_hint()


def play_match(
    page: Page,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
    match_plan: MatchPlan,
) -> dict[str, Any]:
    install_deterministic_random(page, random_values_for_computer_moves(match_plan))
    expected_states = initial_board_state()
    match_started_at_ms = current_browser_timestamp_ms(page)

    for turn_index, human_cell_index in enumerate(match_plan.human_moves):
        play_page.assert_cell_is_empty(
            human_cell_index,
            expected_aria_disabled=GameDashboardViewPlayPage.EMPTY_CELL_ARIA_DISABLED,
            expected_enabled=True,
        )
        play_page.select_cell(human_cell_index)
        expected_states[human_cell_index] = GameDashboardViewPlayPage.PLAYER_CELL_STATE

        if turn_index < len(match_plan.computer_moves):
            computer_cell_index = match_plan.computer_moves[turn_index]
            expected_states[computer_cell_index] = GameDashboardViewPlayPage.COMPUTER_CELL_STATE
            wait_for_board_state(page, expected_states)
            play_page.assert_current_board_state(expected_states)

            if turn_index == 0:
                play_page.assert_cell_occupied_by_user(human_cell_index)
                play_page.assert_cell_occupied_by_computer(computer_cell_index)

            if turn_index == len(match_plan.human_moves) - 1:
                assert_match_finished(play_page, match_plan)
            else:
                assert_user_turn(play_page)
        else:
            wait_for_board_state(page, expected_states)
            play_page.assert_current_board_state(expected_states)
            assert_match_finished(play_page, match_plan)

    match_finished_at_ms = current_browser_timestamp_ms(page)
    latest_record = get_latest_history_record(page, player_name)
    assert_record_matches_completed_match(
        latest_record,
        expected_result=match_plan.result,
        started_at_ms=match_started_at_ms,
        finished_at_ms=match_finished_at_ms,
    )
    return latest_record


def assert_user_turn(play_page: GameDashboardViewPlayPage) -> None:
    expect(play_page.status).to_have_text(GameDashboardViewPlayPage.STATUS_TEXT)
    expect(play_page.status).to_have_attribute("data-status", GameDashboardViewPlayPage.STATUS_DATA_VALUE)


def assert_match_finished(play_page: GameDashboardViewPlayPage, match_plan: MatchPlan) -> None:
    expect(play_page.status).to_have_text(match_plan.final_status_text)
    expect(play_page.status).to_have_attribute("data-status", match_plan.final_status_value)
    expect(play_page.btn_new).to_be_enabled()
    expect(play_page.btn_hint).to_be_disabled()
    expect(play_page.btn_reset).to_be_enabled()


def assert_profile_after_matches(profile_page: GameDashboardProfileViewPage, player_name: str) -> None:
    profile_page.assert_all_initial_elements_are_visible()
    profile_page.assert_header_values_are_correct()
    profile_page.assert_navigation_values_are_correct(player_name)
    profile_page.assert_profile_values_are_correct(player_name)
    profile_page.assert_profile_stats(wins=1, losses=1, draws=1)


def assert_record_matches_completed_match(
    record: dict[str, Any],
    *,
    expected_result: MatchResult,
    started_at_ms: int,
    finished_at_ms: int,
) -> None:
    if record["difficulty"] != GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE:
        raise AssertionError(f"expected default difficulty in history, got {record['difficulty']!r}")

    if record["result"] != expected_result:
        raise AssertionError(f"expected history result {expected_result!r}, got {record['result']!r}")

    assert_timestamp_between(
        timestamp_ms=record["finishedAt"],
        started_at_ms=started_at_ms,
        finished_at_ms=finished_at_ms,
        tolerance_ms=1000,
    )


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


def install_deterministic_random(page: Page, random_values: list[float]) -> None:
    page.evaluate(
        """(values) => {
            let nextIndex = 0;
            Math.random = () => values[nextIndex++] ?? 0;
        }""",
        random_values,
    )


def random_values_for_computer_moves(match_plan: MatchPlan) -> list[float]:
    board_state = initial_board_state()
    random_values: list[float] = []

    for turn_index, human_cell_index in enumerate(match_plan.human_moves):
        board_state[human_cell_index] = GameDashboardViewPlayPage.PLAYER_CELL_STATE

        if turn_index >= len(match_plan.computer_moves):
            break

        computer_cell_index = match_plan.computer_moves[turn_index]
        empty_cells = [index for index, state in enumerate(board_state) if state == "empty"]
        empty_cell_offset = empty_cells.index(computer_cell_index)
        random_values.append((empty_cell_offset + 0.1) / len(empty_cells))
        board_state[computer_cell_index] = GameDashboardViewPlayPage.COMPUTER_CELL_STATE

    return random_values


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
