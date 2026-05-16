from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import pytest
from playwright.sync_api import Page


@pytest.fixture
def seed_accounts(app_page: Page) -> Callable[..., None]:
    def _seed_accounts(
        accounts: Sequence[dict[str, Any]],
        *,
        active_player_name: str | None = None,
        reload: bool = True,
        replace: bool = True,
    ) -> None:
        app_page.evaluate(
            """({accounts, activePlayerName, replace}) => {
                const users = replace ? {} : JSON.parse(localStorage.getItem("ttt:users") || "{}");

                for (const account of accounts) {
                    users[account.name.trim().toLowerCase()] = account;
                }

                localStorage.setItem("ttt:users", JSON.stringify(users));

                if (activePlayerName !== null) {
                    localStorage.setItem("ttt:session", activePlayerName);
                } else if (replace) {
                    localStorage.removeItem("ttt:session");
                }
            }""",
            {
                "accounts": list(accounts),
                "activePlayerName": active_player_name,
                "replace": replace,
            },
        )

        if reload:
            app_page.reload(wait_until="networkidle")

    return _seed_accounts
