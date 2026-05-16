from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import Page, expect

from pages.account_creation_pom import AccountCreationPage
from pages.game_dashboard_history_view_pom import GameDashboardHistoryViewPage
from pages.game_dashboard_play_view_pom import GameDashboardViewPlayPage
from pages.game_dashboard_profile_view_pom import GameDashboardProfileViewPage


@dataclass(frozen=True)
class CreatedAccount:
    player_name: str
    creation_started_at_ms: int
    creation_finished_at_ms: int
    stored_created_at_ms: int


def test_create_new_account_verify_new_user_data_and_logout(
    app_page: Page,
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    profile_page: GameDashboardProfileViewPage,
    history_page: GameDashboardHistoryViewPage,
    player_name: str,
) -> None:
    account_creation_page.assert_loaded()

    created_account = create_account(
        page=app_page,
        account_creation_page=account_creation_page,
        play_page=play_page,
        player_name=player_name,
    )

    play_page.assert_loaded(created_account.player_name)

    play_page.open_profile_view()
    profile_page.assert_loaded(
        created_account.player_name,
        creation_started_at_ms=created_account.creation_started_at_ms,
        creation_finished_at_ms=created_account.creation_finished_at_ms,
    )
    assert_profile_matches_stored_account(profile_page, created_account)

    profile_page.open_history_view()
    history_page.assert_empty_loaded(created_account.player_name)

    history_page.log_out()
    account_creation_page.assert_loaded()


def create_account(
    *,
    page: Page,
    account_creation_page: AccountCreationPage,
    play_page: GameDashboardViewPlayPage,
    player_name: str,
) -> CreatedAccount:
    account_creation_page.fill_player_name(player_name)
    creation_started_at_ms = current_browser_timestamp_ms(page)
    account_creation_page.submit_create_account()
    expect(play_page.view_play).to_be_visible()
    creation_finished_at_ms = current_browser_timestamp_ms(page)

    stored_account = get_stored_account(page, player_name)
    if stored_account is None:
        raise AssertionError(f"created account {player_name!r} was not persisted in local storage")

    assert stored_account["name"] == player_name
    assert stored_account["difficulty"] == GameDashboardViewPlayPage.DEFAULT_DIFFICULTY_VALUE
    assert stored_account["history"] == []

    stored_created_at_ms = stored_account["createdAt"]
    if not isinstance(stored_created_at_ms, int | float):
        raise AssertionError(f"stored createdAt must be a timestamp, got {stored_created_at_ms!r}")

    assert_timestamp_between(
        timestamp_ms=stored_created_at_ms,
        started_at_ms=creation_started_at_ms,
        finished_at_ms=creation_finished_at_ms,
    )

    return CreatedAccount(
        player_name=player_name,
        creation_started_at_ms=creation_started_at_ms,
        creation_finished_at_ms=creation_finished_at_ms,
        stored_created_at_ms=int(stored_created_at_ms),
    )


def get_stored_account(page: Page, player_name: str) -> dict[str, object] | None:
    return page.evaluate(
        """(playerName) => {
            const normalizedPlayerName = playerName.trim().toLowerCase();

            for (const storageKey of Object.keys(localStorage)) {
                const rawValue = localStorage.getItem(storageKey);
                let parsedValue = null;

                try {
                    parsedValue = JSON.parse(rawValue);
                } catch {
                    parsedValue = null;
                }

                const account = parsedValue?.[normalizedPlayerName];

                if (account && typeof account === "object") {
                    return {
                        storageKey,
                        normalizedPlayerName,
                        ...account,
                    };
                }
            }

            return null;
        }""",
        player_name,
    )


def assert_profile_matches_stored_account(
    profile_page: GameDashboardProfileViewPage,
    created_account: CreatedAccount,
) -> None:
    expect(profile_page.input_profile_name).to_have_value(created_account.player_name)
    profile_created_at_ms = profile_page.get_created_at_timestamp_ms()
    assert_timestamps_are_close(
        actual_ms=profile_created_at_ms,
        expected_ms=created_account.stored_created_at_ms,
        tolerance_ms=1000,
    )


def assert_timestamp_between(
    *,
    timestamp_ms: int | float,
    started_at_ms: int,
    finished_at_ms: int,
    tolerance_ms: int = 0,
) -> None:
    if not started_at_ms - tolerance_ms <= timestamp_ms <= finished_at_ms + tolerance_ms:
        raise AssertionError(f"{timestamp_ms} was not between {started_at_ms} and {finished_at_ms}")


def assert_timestamps_are_close(*, actual_ms: int, expected_ms: int, tolerance_ms: int) -> None:
    if abs(actual_ms - expected_ms) > tolerance_ms:
        raise AssertionError(f"{actual_ms} was not within {tolerance_ms}ms of {expected_ms}")


def current_browser_timestamp_ms(page: Page) -> int:
    return int(page.evaluate("Date.now()"))
