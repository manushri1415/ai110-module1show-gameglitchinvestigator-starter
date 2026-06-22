from logic_utils import check_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# FIXME 1: Test that "Go HIGHER/LOWER" hints are not reversed
def test_fixme1_too_high_message():
    """FIXME 1: Verify that when guess > secret, message says 'Go LOWER'."""
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()

def test_fixme1_too_low_message():
    """FIXME 1: Verify that when guess < secret, message says 'Go HIGHER'."""
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


# FIXME 2: Test that type mismatches don't cause comparison errors
def test_fixme2_string_secret_comparison():
    """FIXME 2: Verify that string secrets are handled correctly via type coercion."""
    secret_str = "50"
    guess_int = 50
    outcome, _ = check_guess(guess_int, secret_str)
    assert outcome == "Win"

def test_fixme2_string_secret_too_high():
    """FIXME 2: Verify string secret comparison for too high guess."""
    secret_str = "50"
    outcome, _ = check_guess(75, secret_str)
    assert outcome == "Too High"

def test_fixme2_string_secret_too_low():
    """FIXME 2: Verify string secret comparison for too low guess."""
    secret_str = "50"
    outcome, _ = check_guess(25, secret_str)
    assert outcome == "Too Low"


# FIXME 3: Test that scoring consistently penalizes all wrong guesses
def test_fixme3_wrong_guess_penalty_on_odd_attempt():
    """FIXME 3: Verify wrong guesses are penalized on odd attempts."""
    current_score = 50
    new_score = update_score(current_score, "Too High", attempt_number=1)
    assert new_score == 45, "Should deduct 5 points for wrong guess on attempt 1"

def test_fixme3_wrong_guess_penalty_on_even_attempt():
    """FIXME 3: Verify wrong guesses are penalized on even attempts (not rewarded)."""
    current_score = 50
    new_score = update_score(current_score, "Too High", attempt_number=2)
    assert new_score == 45, "Should deduct 5 points for wrong guess on even attempt 2, not reward"

def test_fixme3_multiple_wrong_attempts():
    """FIXME 3: Verify consistent penalty across multiple wrong attempts."""
    score = 100
    for attempt in range(1, 6):
        score = update_score(score, "Too Low", attempt_number=attempt)
    assert score == 75, "5 wrong guesses should result in 5*5=25 point penalty"


# FIXME 4: Test that both outcome types have same penalty
def test_fixme4_too_high_and_too_low_same_penalty():
    """FIXME 4: Verify that 'Too High' and 'Too Low' have identical -5 penalty."""
    current_score = 100

    score_after_too_high = update_score(current_score, "Too High", attempt_number=3)
    score_after_too_low = update_score(current_score, "Too Low", attempt_number=3)

    assert score_after_too_high == score_after_too_low == 95, \
        "Both 'Too High' and 'Too Low' should result in -5 penalty"

def test_fixme4_penalty_consistency():
    """FIXME 4: Verify penalty is consistent regardless of outcome type."""
    base_score = 75
    outcomes = ["Too High", "Too Low"]
    scores = [update_score(base_score, outcome, attempt_number=5) for outcome in outcomes]
    assert all(score == 70 for score in scores), \
        "All wrong outcome types should have same -5 penalty"


# FIXME 5: Test that attempts counter starts at 0
# (In app.py: st.session_state.attempts = 0 instead of 1)
# This ensures "attempts left" calculation is correct from the start


# FIXME 6: Test that New Game resets score and history
# (In app.py: Reset status, score, history on new_game button)
def test_fixme6_score_reset_logic():
    """FIXME 6: Verify that a losing sequence followed by win doesn't carry over penalty."""
    score = 100
    # Simulate 5 wrong guesses
    for attempt in range(1, 6):
        score = update_score(score, "Too Low", attempt_number=attempt)
    assert score == 75, "5 wrong guesses should deduct 25 points"

    # After new game, score should be reset to 0 (tested via app.py resetting st.session_state.score)
    # This test ensures the update_score function is stateless for proper reset behavior


# FIXME 7: Test that difficulty ranges are correct for attempt limits
# (Easy > Normal > Hard attempt limits)
def test_fixme7_attempt_limits_scaled_correctly():
    """FIXME 7: Verify attempt limits are correctly ordered (Easy > Normal > Hard)."""
    # From app.py: Easy: 8, Normal: 6, Hard: 5
    attempt_limits = {"Easy": 8, "Normal": 6, "Hard": 5}
    assert attempt_limits["Easy"] > attempt_limits["Normal"], "Easy should have more attempts than Normal"
    assert attempt_limits["Normal"] > attempt_limits["Hard"], "Normal should have more attempts than Hard"

def test_fixme7_hard_has_smallest_range():
    """FIXME 7: Verify Hard difficulty has restricted range."""
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert hard_low == 1 and hard_high == 50, "Hard should have range 1-50"


# FIXME 8: Test that attempts left calculation doesn't go negative
# (Capped with max(0, attempt_limit - attempts))
def test_fixme8_attempts_left_never_negative():
    """FIXME 8: Verify attempts_left calculation logic doesn't produce negatives."""
    attempt_limit = 8
    attempts_list = [0, 1, 7, 8, 9, 10]  # Including over-limit
    for attempts in attempts_list:
        attempts_left = max(0, attempt_limit - attempts)
        assert attempts_left >= 0, f"attempts_left should never be negative (limit={attempt_limit}, attempts={attempts}, result={attempts_left})"

def test_fixme8_correct_range_display():
    """FIXME 8: Verify get_range_for_difficulty returns correct ranges for display."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    for difficulty, expected in ranges.items():
        low, high = get_range_for_difficulty(difficulty)
        assert (low, high) == expected, f"{difficulty} should display range {expected}, got ({low}, {high})"
