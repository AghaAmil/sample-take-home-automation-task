# Test Cases

## General Notes

- Unless a test case states otherwise, start from a clean browser state with application local storage cleared.
- Use the English UI for baseline execution unless a test case specifically covers Persian.
- Board cell references use this 3x3 index map:

| 0 | 1 | 2 |
|---|---|---|
| 3 | 4 | 5 |
| 6 | 7 | 8 |

### TC-01

**Title/Description:** Open the Tic-Tac-Toe application in a modern browser.

**Priority:** High

**Preconditions:**
- Browser local storage is cleared.

**Test Steps:**
1. Open `index.html` directly in a modern browser or serve it from a static local server.
2. Observe the initial page content.

**Expected Result:**
- The title `Tic-Tac-Toe` and subtitle `A small game for test automation` are visible.
- The language selector, theme button, player name field, and account creation view are visible.

### TC-02

**Title/Description:** Switch between Create Account and Login modes.

**Priority:** High

**Preconditions:**
- The application is open on the initial authentication screen.

**Test Steps:**
1. Verify that the initial auth mode shows the `Create Account` button.
2. Click `Already have an account? Log in`.
3. Verify that the primary button changes to `Log In`.
4. Click `New player? Create an account`.
5. Verify that the primary button changes back to `Create Account`.

**Expected Result:**
- The auth mode switches correctly in both directions.
- The player name field remains visible and usable.
- No layout break or stale validation message remains after switching modes.

### TC-03

**Title/Description:** Validate account creation with an empty player name.

**Priority:** High

**Preconditions:**
- The application is open in Create Account mode.

**Test Steps:**
1. Leave the `Player Name` field empty.
2. Click `Create Account`.

**Expected Result:**
- The account is not created.
- The user remains on the authentication screen.
- A proper error message is shown *"Please enter a name."*.

### TC-04

**Title/Description:** Validate account creation with a one-character player name.

**Priority:** High

**Preconditions:**
- The application is open in Create Account mode.

**Test Steps:**
1. Enter `A` in the `Player Name` field.
2. Click `Create Account`.

**Expected Result:**
- The account is not created.
- A proper error message is shown *"Name must be at least 2 characters."*.
- The Play dashboard is not opened.

### TC-05

**Title/Description:** Create an account with a valid new player name.

**Priority:** Critical

**Preconditions:**
- The application is open in Create Account mode.
- No account exists for `Sara`.

**Test Steps:**
1. Enter `Sara` in the `Player Name` field.
2. Click `Create Account`.

**Expected Result:**
- The account is created successfully.
- The Play view opens.
- The navigation bar displays a greeting for `Sara`.
- The board, difficulty selector, status message, `New Game`, `Get Hint`, and `Reset` controls are visible.

### TC-06

**Title/Description:** Prevent duplicate account creation using a normalized existing name.

**Priority:** High

**Preconditions:**
- An account named `Sara` already exists.
- The user is logged out and the app is in Create Account mode.

**Test Steps:**
1. Enter `sara` or `SARA` in the `Player Name` field.
2. Click `Create Account`.

**Expected Result:**
- The duplicate account is not created.
- A proper error message is shown *"This name is already taken. Try logging in."*.
- The user remains on the authentication screen.

### TC-07

**Title/Description:** Log out after account creation.

**Priority:** High

**Preconditions:**
- A user is logged in and the Play view is displayed.

**Test Steps:**
1. Click `Log Out` in the navigation bar.

**Expected Result:**
- The current session is cleared.
- The authentication screen is displayed.

### TC-08

**Title/Description:** Log in with an existing account.

**Priority:** Critical

**Preconditions:**
- An account named `Sara` already exists.
- The user is logged out.

**Test Steps:**
1. Click `Already have an account? Log in`.
2. Enter `sara` or `SARA` in the `Player Name` field.
3. Click `Log In`.

**Expected Result:**
- The user is logged in successfully.
- The Play view opens.
- The navigation bar displays a greeting for `Sara`.
- Existing account data, such as selected difficulty and history, remains available.

### TC-09

**Title/Description:** Reject login with a non-existing account name.

**Priority:** High

**Preconditions:**
- No account exists for `NotCreatedUser`.
- The application is in Login mode.

**Test Steps:**
1. Enter `NotCreatedUser` in the `Player Name` field.
2. Click `Log In`.

**Expected Result:**
- Login is rejected.
- A proper error message is shown *"No account with this name. Please register."*.
- The user remains on the authentication screen.

### TC-10

**Title/Description:** Restore the logged-in session after page reload.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The Play view is displayed.

**Test Steps:**
1. Reload the browser page.

**Expected Result:**
- The user remains logged in after reload.
- The Play view is displayed.
- The greeting, selected preference state, and local account data are restored from local storage.

### TC-11

**Title/Description:** Toggle between light and dark themes.

**Priority:** Medium

**Preconditions:**
- The application is open.

**Test Steps:**
1. Observe the current theme label on the theme button.
2. Click the theme button.
3. Verify that the page colors change.
4. Reload the page.

**Expected Result:**
- The theme switches between light and dark modes.
- Text, controls, and board cells remain readable.
- The selected theme remains unchanged after reload.
- The theme change applies to all application pages.

### TC-12

**Title/Description:** Change application language from English to Persian.

**Priority:** Medium

**Preconditions:**
- The application is open in English.

**Test Steps:**
1. Open the language selector.
2. Select `Persian`.
3. Observe the header, auth or navigation labels, buttons, and layout direction.

**Expected Result:**
- Visible labels are translated to Persian.
- The page language and direction update for Persian.
- The layout remains usable without overlapping or clipped primary controls.

### TC-13

**Title/Description:** Navigate between Play, Profile, and History views.

**Priority:** High

**Preconditions:**
- A user is logged in.

**Test Steps:**
1. Click `Profile`.
2. Verify that the Profile view is displayed.
3. Click `History`.
4. Verify that the History view is displayed.
5. Click `Play`.
6. Verify that the Play view is displayed.

**Expected Result:**
- Each selected view renders correctly.
- The active navigation state updates for the selected tab.
- The user session and account context remain intact.

### TC-14

**Title/Description:** Verify the initial Play view for a new user.

**Priority:** Critical

**Preconditions:**
- A new user account has just been created.

**Test Steps:**
1. Observe the Play view.
2. Inspect the difficulty selector.
3. Inspect the board cells.
4. Inspect the game status and action buttons.

**Expected Result:**
- The selected difficulty defaults to `Easy`.
- All nine board cells are empty.
- The status shows `Your turn (X)`.
- `New Game`, `Get Hint`, and `Reset` buttons are visible.

### TC-15

**Title/Description:** Place a mark on an empty board cell during the player turn.

**Priority:** Critical

**Preconditions:**
- A user is logged in.
- The Play view is displayed.
- The board is empty and status is `Your turn (X)`.

**Test Steps:**
1. Click any empty board cell, for example cell 0.
2. Observe the clicked cell immediately.
3. Wait for the computer move to complete.

**Expected Result:**
- The clicked cell displays `X`.
- Board cells are disabled while the computer is thinking.
- If the game is still active, one empty cell is marked with `O`.
- The game returns to the player turn.

### TC-16

**Title/Description:** Prevent the user from changing an occupied cell.

**Priority:** Critical

**Preconditions:**
- A user is logged in.
- At least one board cell is already occupied.
- The game is active and it is the player turn.

**Test Steps:**
1. Click an occupied `X` or `O` cell.
2. Observe the board state.

**Expected Result:**
- The occupied cell value does not change.
- No additional `X` is placed.
- The user does not receive an extra turn.

### TC-17

**Title/Description:** Prevent user moves while the computer is thinking.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The game is active and it is the player turn.

**Test Steps:**
1. Click an empty board cell.
2. Immediately click another empty board cell before the computer move finishes.

**Expected Result:**
- Only the first player move is accepted.
- The second click is ignored while the board is disabled.
- The computer makes one legal move.

### TC-18

**Title/Description:** Record and display a player win.

**Priority:** Critical

**Preconditions:**
- A user is logged in.
- The Play view is displayed.
- Any difficulty can be selected.

**Test Steps:**
1. Complete a winning line for X.
2. Observe the status message and board state.
3. Open the History view.
4. Open the Profile view.

**Expected Result:**
- The status changes to `You win!`.
- The winning cells are highlighted in green.
- Board input is disabled after the result.
- A `Win` record is added to History.
- The Profile win count increases by one.

### TC-19

**Title/Description:** Record and display a computer win.

**Priority:** Critical

**Preconditions:**
- A user is logged in.
- The Play view is displayed.
- Any difficulty can be selected.

**Test Steps:**
1. Make a player move that allows the computer to complete a winning line.
2. Wait for the computer move.
3. Observe the status message and board state.
4. Open the History and Profile views.

**Expected Result:**
- The status changes to `Computer wins.`
- The winning cells are highlighted in green.
- Board input is disabled after the result.
- A `Loss` record is added to History.
- The Profile loss count increases by one.

### TC-20

**Title/Description:** Record and display a draw result.

**Priority:** Critical

**Preconditions:**
- A user is logged in.
- The Play view is displayed.
- Any difficulty can be selected.

**Test Steps:**
1. Complete the game so all cells are filled without any winning line.
2. Observe the status message.
3. Open the History view.
4. Open the Profile view.

**Expected Result:**
- The status changes to `Draw.`
- Board input is disabled after the result.
- A `Draw` record is added to History.
- The Profile draw count increases by one.

### TC-21

**Title/Description:** Start a new game during or after gameplay.

**Priority:** High

**Preconditions:**
- A user is logged in.
- A game is active with at least one move, or a completed game is displayed.

**Test Steps:**
1. Note the selected difficulty.
2. Click `New Game`.
3. Observe the board and status.

**Expected Result:**
- The board resets to nine empty cells.
- The same difficulty remains selected.
- The status returns to `Your turn (X)`.
- Previously completed history records remain available in user profile and history page.

### TC-22

**Title/Description:** Reset the current game without deleting previous history.

**Priority:** High

**Preconditions:**
- A user is logged in.
- At least one completed game exists in History.
- The Play view is displayed with moves on the board or a completed result.

**Test Steps:**
1. Click `Reset`.
2. Observe the board and status.
3. Open the History view.

**Expected Result:**
- The board resets to nine empty cells.
- The status returns to `Your turn (X)`.
- Existing completed history records are not deleted in user profile and history page.

### TC-23

**Title/Description:** Request a hint during the player turn.

**Priority:** Medium

**Preconditions:**
- A user is logged in.
- The game is active.
- It is the player's turn.
- At least one empty cell is available.

**Test Steps:**
1. Click `Get Hint`.
2. Observe the board.
3. Wait for the hint highlight to disappear.

**Expected Result:**
- One available cell is visually highlighted as a recommended move.
- The hint does not place an `X` or `O`.
- The highlight clears after a short time.

### TC-24

**Title/Description:** Verify Hint is disabled when it is not available.

**Priority:** Medium

**Preconditions:**
- A user is logged in.

**Test Steps:**
1. Click an empty cell to trigger the computer turn.
2. Observe the `Get Hint` button while the computer is thinking.
3. Complete a game to a win, loss, or draw.
4. Observe the `Get Hint` button after the game result.

**Expected Result:**
- `Get Hint` is disabled while the computer is thinking.
- `Get Hint` is disabled after the game is complete.
- No hint can be requested outside the player's active turn.

### TC-25

**Title/Description:** Change difficulty before making any move.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The board is empty.

**Test Steps:**
1. Open the difficulty selector.
2. Select `Medium`.
3. Verify the selected value.
4. Open the difficulty selector again.
5. Select `Hard`.

**Expected Result:**
- The selected difficulty updates without confirmation because no moves have been made.
- The board remains empty.
- The selected difficulty is retained for the new game state.

### TC-26

**Title/Description:** Cancel difficulty change during an active game.

**Priority:** Medium

**Preconditions:**
- A user is logged in.
- A game is active and at least one board cell is occupied.

**Test Steps:**
1. Open the difficulty selector.
2. Select a different difficulty.
3. When the confirmation dialog appears *"Change difficulty and start a new game?"*, choose `Cancel`.

**Expected Result:**
- The difficulty is not changed.
- The current board state remains unchanged.
- The active game continues.

### TC-27

**Title/Description:** Accept difficulty change during an active game.

**Priority:** Medium

**Preconditions:**
- A user is logged in.
- A game is active and at least one board cell is occupied.

**Test Steps:**
1. Open the difficulty selector.
2. Select a different difficulty.
3. When the confirmation dialog appears *"Change difficulty and start a new game?"*, choose `OK`.

**Expected Result:**
- The selected difficulty is applied.
- The current board resets to an empty board.
- The status returns to `Your turn (X)`.

### TC-28

**Title/Description:** Verify a completed game is recorded only once.

**Priority:** High

**Preconditions:**
- A user is logged in.
- A game has just completed with a win, loss, or draw.

**Test Steps:**
1. Observe the final result status.
2. Click completed board cells several times.
3. Navigate to Profile and back to Play.
4. Navigate to History.

**Expected Result:**
- Board clicks after completion do not change the game state.
- Only one history record is created for the completed game.
- Profile totals increase by only one result.

### TC-29

**Title/Description:** Verify Profile statistics after multiple games.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The account has completed at least one win, one loss, and one draw.

**Test Steps:**
1. Open the History view.
2. Count the visible `Win`, `Loss`, and `Draw` records and timing.
3. Open the Profile view.
4. Compare Profile totals to the History records.

**Expected Result:**
- The Profile win count matches the number of win records.
- The Profile loss count matches the number of loss records.
- The Profile draw count matches the number of draw records.

### TC-30

**Title/Description:** Update the profile display name to a valid unique name.

**Priority:** High

**Preconditions:**
- A user named `Sara` is logged in.
- No account exists for `Sara QA`.

**Test Steps:**
1. Open the Profile view.
2. Replace the display name with `Sara QA`.
3. Click `Save Changes`.
4. Observe the success message *"Saved."* and navigation greeting.
5. Reload the page.

**Expected Result:**
- The profile name is updated successfully.
- The greeting and avatar update to reflect the new name.
- The session remains active.
- Existing history and statistics are preserved after the rename and reload.

### TC-31

**Title/Description:** Reject invalid profile display name updates.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The Profile view is displayed.

**Test Steps:**
1. Clear the display name field.
2. Click `Save Changes`.
3. Enter `A` in the display name field.
4. Click `Save Changes`.

**Expected Result:**
- Empty and one-character names are rejected.
- An appropriate validation or error message *"Use at least 2 characters"* is shown.
- The original profile name remains unchanged.

### TC-32

**Title/Description:** Reject profile rename to an existing account name.

**Priority:** High

**Preconditions:**
- Accounts named `Sara` and `Amir` exist.
- The user is logged in as `Sara`.

**Test Steps:**
1. Open the Profile view.
2. Change the display name to `Amir`.
3. Click `Save Changes`.

**Expected Result:**
- The rename is rejected.
- A duplicate-name error message *"Another account already uses this name."* is displayed.
- The current account name and session remain unchanged.

### TC-33

**Title/Description:** Delete an account after confirmation.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The Profile view is displayed.

**Test Steps:**
1. Open the Profile page.
2. Click `Delete Account`.
3. In the confirmation dialog, choose `OK`.
4. Attempt to log in again with the deleted account name.

**Expected Result:**
- The account is deleted.
- The session ends and the authentication screen is displayed.
- Login with the deleted account name fails because the account no longer exists.
- A proper error message is shown *"No account with this name. Please register."*.

### TC-34

**Title/Description:** Cancel account deletion.

**Priority:** Medium

**Preconditions:**
- A user is logged in.
- The Profile view is displayed.

**Test Steps:**
1. Open the Profile page.
2. Click `Delete Account`.
3. In the confirmation dialog, choose `Cancel`.

**Expected Result:**
- The account is not deleted.
- The user remains logged in.
- Profile data, history, and statistics remain unchanged.

### TC-35

**Title/Description:** Verify History view for a user with no completed games.

**Priority:** Medium

**Preconditions:**
- A new user is logged in.
- No games have been completed.

**Test Steps:**
1. Click `History`.
2. Observe the History view.

**Expected Result:**
- An empty-history message *"No games yet. Play one!"* is displayed.
- No history table rows are shown.
- `Clear History` is not displayed.

### TC-36

**Title/Description:** Verify History view after several completed games.

**Priority:** High

**Preconditions:**
- A user is logged in.
- The account has multiple completed games across one or more difficulty levels.

**Test Steps:**
1. Open the History view.
2. Review each visible row.
3. Compare the latest completed game to the first row.

**Expected Result:**
- The table shows Date, Difficulty, and Result columns.
- Each completed game appears as a row.
- The newest result appears first.
- Result text and visual indicators match win, loss, or draw outcomes.

### TC-37

**Title/Description:** Clear match history after confirmation.

**Priority:** High

**Preconditions:**
- A user is logged in.
- At least one history record exists.
- The History view is displayed.

**Test Steps:**
1. Click `Clear History`.
2. In the confirmation dialog, choose `OK`.
3. Observe the History view.
4. Open the Profile view.

**Expected Result:**
- All history records are removed.
- The empty-history message is displayed.
- Profile win, loss, and draw totals return to zero.

### TC-38

**Title/Description:** Cancel clearing match history.

**Priority:** Medium

**Preconditions:**
- A user is logged in.
- At least one history record exists.
- The History view is displayed.

**Test Steps:**
1. Click `Clear History`.
2. In the confirmation dialog, choose `Cancel`.

**Expected Result:**
- Existing history records remain visible.
- Profile statistics remain unchanged.
- The user remains on the History view.

### TC-39

**Title/Description:** Smoke test the critical flow across modern browsers.

**Priority:** Medium

**Preconditions:**
- Chrome, Safari, Firefox, and Edge are available, or the available browser matrix is documented.

**Test Steps:**
1. Open the application in each target browser.
2. Create a valid account.
3. Place at least one player move and wait for the computer move.
4. Navigate to Profile and History.
5. Log out.

**Expected Result:**
- The critical flow works consistently in each tested browser.
- Local storage, form validation, click handling, and navigation behave as expected.
- Any browser-specific differences are documented as defects or test notes.

### TC-40

**Title/Description:** Clear browser local storage and reload the application.

**Priority:** Medium

**Preconditions:**
- A user account and session exist in local storage.

**Test Steps:**
1. Use browser developer tools or browser settings to clear local storage for the application.
2. Reload the page.

**Expected Result:**
- The application returns to the clean authentication state.
- No JavaScript error prevents the page from rendering.
- Previously stored account/session data is no longer available in that browser profile.
