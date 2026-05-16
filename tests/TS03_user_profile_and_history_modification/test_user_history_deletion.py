from __future__ import annotations

from collections.abc import Callable
from typing import Any

from playwright.sync_api import Page

from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


def test_clear_history_resets_history_and_profile_totals(
    app_page: Page,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
    player_name: str,
    seed_accounts: Callable[..., None],
) -> None:
    now_ms = current_browser_timestamp_ms(app_page)
    records = completed_history_records(now_ms)

    seed_accounts(
        [
            {
                "name": player_name,
                "createdAt": now_ms - days_in_ms(30),
                "difficulty": GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE,
                "history": records,
            }
        ],
        active_player_name=player_name,
    )

    play_page.assert_loaded(player_name)

    play_page.open_profile_view()
    assert_profile_shows_completed_totals(profile_page, player_name)

    profile_page.open_history_view()
    history_page.assert_populated_loaded(player_name, expected_records=records)
    assert_stored_history_count(app_page, player_name, expected_count=len(records))

    history_page.clear_history(confirm=False)
    history_page.assert_populated_loaded(player_name, expected_records=records)
    assert_stored_history_count(app_page, player_name, expected_count=len(records))

    history_page.clear_history(confirm=True)
    history_page.assert_empty_loaded(player_name)
    assert_stored_history_count(app_page, player_name, expected_count=0)

    history_page.open_profile_view()
    assert_profile_totals_are_reset(profile_page, player_name)


def assert_profile_shows_completed_totals(
    profile_page: GameDashboardProfileViewPage,
    player_name: str,
) -> None:
    profile_page.assert_all_initial_elements_are_visible()
    profile_page.assert_header_values_are_correct()
    profile_page.assert_navigation_values_are_correct(player_name)
    profile_page.assert_profile_values_are_correct(player_name)
    profile_page.assert_profile_stats(wins=2, losses=1, draws=1)


def assert_profile_totals_are_reset(
    profile_page: GameDashboardProfileViewPage,
    player_name: str,
) -> None:
    profile_page.assert_all_initial_elements_are_visible()
    profile_page.assert_header_values_are_correct()
    profile_page.assert_navigation_values_are_correct(player_name)
    profile_page.assert_profile_values_are_correct(player_name)
    profile_page.assert_profile_stats_are_zero()


def completed_history_records(now_ms: int) -> list[dict[str, Any]]:
    return [
        {
            "finishedAt": now_ms - days_in_ms(1),
            "difficulty": "hard",
            "result": "win",
        },
        {
            "finishedAt": now_ms - days_in_ms(2),
            "difficulty": "medium",
            "result": "draw",
        },
        {
            "finishedAt": now_ms - days_in_ms(3),
            "difficulty": "easy",
            "result": "loss",
        },
        {
            "finishedAt": now_ms - days_in_ms(4),
            "difficulty": "medium",
            "result": "win",
        },
    ]


def assert_stored_history_count(page: Page, player_name: str, *, expected_count: int) -> None:
    actual_count = page.evaluate(
        """(playerName) => {
            const users = JSON.parse(localStorage.getItem("ttt:users") || "{}");
            return users[playerName.trim().toLowerCase()]?.history?.length ?? 0;
        }""",
        player_name,
    )

    if actual_count != expected_count:
        raise AssertionError(f"expected {expected_count} stored history records, got {actual_count}")


def current_browser_timestamp_ms(page: Page) -> int:
    return int(page.evaluate("Date.now()"))


def days_in_ms(days: int) -> int:
    return days * 24 * 60 * 60 * 1000
