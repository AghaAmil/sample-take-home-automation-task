# Test Plan: Web-Based Tic-Tac-Toe Application

## Application Overview

The System Under Test is a single-file, browser-based Tic-Tac-Toe application implemented in `index.html`. It can be opened directly in a modern browser or served from a static local server. The application has no backend service; user profiles and statistics are stored in the browser's local storage.

It includes account creation and login, a player dashboard, AI opponent difficulty levels, hints, match result tracking, profile management, history, language selection, and theme selection.

## Test Objectives

- Verify that all critical user flows required to play and manage the game work correctly.
- Validate Tic-Tac-Toe rules, turn handling, win/lose/draw detection, and game completion behavior.
- Confirm that account creation, login, logout, profile update, account deletion, and local storage persistence work as expected.
- Confirm that user states and data updates are accurate across Play, Profile, and History views.
- Identify high-value, repeatable scenarios for automation using stable selectors and repeatable game states.

## Test Scope

### In Scope

- Application launch, navigation, and primary user flows from authentication through gameplay.
- Account creation, login, logout, profile management, session persistence, and local storage behavior.
- Core Tic-Tac-Toe gameplay, including board interactions, turn handling, difficulty selection, hints, win/loss/draw outcomes, invalid actions, and reset/new-game behavior.
- Match history and player statistics, including recording, display, clearing, and account deletion impacts.
- UI behavior across theme and language settings, including basic layout, readability, and state updates.
- Automation candidates for unit, component, and end-to-end coverage.

### Out of Scope

As this project is a take-home assignment and not a real application, not all aspects of the Application Under Test are thoroughly tested and verified. The list of untested and unverified aspects is summarized below: 

- The application will not undergo testing, verification, or automation in Persian language. However, translation issues or any other issue in Persian language will be addressed in the bug report.
- Detailed design and element validation, as no design specification was provided.
- Security validation beyond local storage risk identification because no real authentication or server-side storage exists.
- Detailed evaluation of AI algorithm and game difficulty. **(It has serious bugs)**
- Testing the web application on a mobile device.

## 4. Test Approach and Strategy

Testing should begin with exploratory testing to understand the complete workflow and identify risks before formal test case execution. Additionally human judgment and manual activities are required to test the computer behavior and game difficulty.

- **Manual testing:** Use manual test execution for visual behavior, language/theme checks, confirmation dialogs, and exploratory edge cases.
- **Exploratory testing:** Explore account setup, local storage persistence, active game interruption, repeated resets, difficulty changes, and browser reload behavior.
- **Functional testing:** Validate each user-facing feature against observed behavior in the source code and screenshots.
- **UI testing:** Confirm page layout, visual state changes, disabled states, status text, winning highlights, and table rendering.

Recommended E2E automation coverage for the assignment:

- Create account, verify Play view, and log out.
- Login with an existing account and verify persisted session.
- Validate empty, too-short, duplicate, and unknown-login errors.
- Play a deterministic game to a human win and verify history/profile.
- Play or set up a draw path and verify draw recording.
- Verify reset/new-game behavior.
- Verify hint button highlights an available cell.
- Verify difficulty selection and active-game confirmation accept/cancel paths.
- Rename profile and confirm all user-facing names update.
- Clear history and verify profile totals reset.
- Delete account and verify login no longer succeeds.

## Test Environment

- **Application environment:** Local static web application opened directly from `index.html` or served from a local static server.
- **Data storage:** Browser local storage only. Testers should clear local storage before clean test runs.
- **Desktop browsers:** Current stable Chrome, Safari, Firefox, or Edge.
- **Framework:** Playwright with Python (Playwright Pytest) 

## Risk Analysis

| Risk                                                          | Impact                                                                                  |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Responsive behavior is CSS-based with compact layout changes. | Mobile view may have wrapping, spacing, or table readability issues.                    |
| Local storage is the only data store.                         | Data can be cleared, corrupted, or manipulated by users and differs by browser profile. |

## Defect Management

Defects should be logged as soon as they are confirmed and should include enough detail for a developer or evaluator to reproduce the issue without additional context. Severity should reflect user impact, while priority should reflect fix order for the assignment.

**Suggested severity definitions:**

- **Critical:** Prevents app launch, account access, board play, result detection, or causes data loss in normal use.
- **High:** Breaks a major feature such as login, win/draw detection, reset, history recording, or invalid move prevention.
- **Medium:** Causes incorrect UI state, accessibility gap, browser-specific issue, or non-critical persistence problem.
- **Low:** Cosmetic issue, minor copy issue, or low-impact layout inconsistency.

**Suggested defect report format:**

| Field              | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| Defect ID          | Unique identifier, for example `BUG-001`.                              |
| Title              | Short summary of the problem.                                          |
| Severity/Priority  | Business and testing impact.                                           |
| Environment        | Browser, OS, viewport, and app launch method.                          |
| Preconditions      | Account, local storage state, selected language/theme, or board state. |
| Steps to Reproduce | Numbered steps from a clean starting point.                            |
| Expected Result    | What should happen.                                                    |
| Actual Result      | What happened instead.                                                 |
| Evidence           | Screenshot, video, console error, or automation trace.                 |
| Notes              | Suspected area, frequency, workaround, or related defect links.        |
