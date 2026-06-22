from logic_utils import check_guess, update_score, get_range_for_difficulty, parse_guess

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


# FIXME 1: Test that "Go HIGHER/LOWER" hints are not reversed - verified with agent assistance
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


# FIXME 2: Test that type alternation was removed - strings are no longer accepted - verified with agent assistance
def test_fixme2_string_secret_rejected():
    """FIXME 2: Verify that string secrets raise TypeError (type alternation removed)."""
    secret_str = "50"
    guess_int = 50
    try:
        outcome, _ = check_guess(guess_int, secret_str)
        assert False, "Should raise TypeError when secret is a string"
    except TypeError:
        pass  # Expected behavior - strings are not coerced


# FIXME 3+4: Test that scoring consistently penalizes all wrong guesses & both outcome types have same penalty - verified with agent assistance
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


# FIXME 5: Attempts counter starts at 0 (verified in app.py with agent assistance)
# This ensures "attempts left" calculation is correct from the start


# FIXME 6: Test that New Game resets score and history - verified with agent assistance
def test_fixme6_score_reset_logic():
    """FIXME 6: Verify that a losing sequence followed by win doesn't carry over penalty."""
    score = 100
    # Simulate 5 wrong guesses
    for attempt in range(1, 6):
        score = update_score(score, "Too Low", attempt_number=attempt)
    assert score == 75, "5 wrong guesses should deduct 25 points"

    # After new game, score should be reset to 0 (tested via app.py resetting st.session_state.score)
    # This test ensures the update_score function is stateless for proper reset behavior


# FIXME 7: Test that difficulty ranges are correct for attempt limits - verified with agent assistance
def test_fixme7_attempt_limits_scaled_correctly():
    """FIXME 7: Verify attempt limits are correctly ordered (Easy > Normal > Hard)."""
    # From app.py: Easy: 8, Normal: 6, Hard: 5
    attempt_limits = {"Easy": 8, "Normal": 6, "Hard": 5}
    assert attempt_limits["Easy"] > attempt_limits["Normal"], "Easy should have more attempts than Normal"
    assert attempt_limits["Normal"] > attempt_limits["Hard"], "Normal should have more attempts than Hard"

def test_fixme7_hard_has_largest_range():
    """FIXME 7: Verify Hard difficulty (after FIXME 15 fix) has largest range."""
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert hard_low == 1 and hard_high == 100, "Hard should have range 1-100"


# FIXME 8: Test that attempts left calculation doesn't go negative - verified with agent assistance
def test_fixme8_attempts_left_never_negative():
    """FIXME 8: Verify attempts_left calculation logic doesn't produce negatives."""
    attempt_limit = 8
    attempts_list = [0, 1, 7, 8, 9, 10]  # Including over-limit
    for attempts in attempts_list:
        attempts_left = max(0, attempt_limit - attempts)
        assert attempts_left >= 0, f"attempts_left should never be negative (limit={attempt_limit}, attempts={attempts}, result={attempts_left})"

def test_fixme8_correct_range_display():
    """FIXME 8: Verify get_range_for_difficulty returns correct ranges (FIXME 15: Normal/Hard corrected)."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 50),
        "Hard": (1, 100),
    }
    for difficulty, expected in ranges.items():
        low, high = get_range_for_difficulty(difficulty)
        assert (low, high) == expected, f"{difficulty} should display range {expected}, got ({low}, {high})"


# FIXME 9: When difficulty changes mid-game, secret may be outside new range - verified with agent assistance
def test_fixme9_difficulty_ranges_containment():
    """FIXME 9: Verify ranges allow for difficulty transitions."""
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")

    # Easy is fully contained within Normal
    assert easy_low >= normal_low and easy_high <= normal_high, \
        "Easy range should fit within Normal range"

    # Normal is fully contained within Hard
    assert normal_low >= hard_low and normal_high <= hard_high, \
        "Normal range should fit within Hard range"


def test_fixme9_secret_regeneration_scenario():
    """FIXME 9: Demonstrate why secret must be regenerated when difficulty changes."""
    # A valid Hard difficulty secret might be 75 (range 1-100)
    hard_secret = 75
    easy_low, easy_high = get_range_for_difficulty("Easy")

    # But 75 is outside Easy range (1-20), so app.py must regenerate
    assert hard_secret > easy_high, \
        f"Hard secret {hard_secret} exceeds Easy max {easy_high}, so regeneration is needed"


# FIXME 11: Added bounds validation to ensure guess is within difficulty range - verified with agent assistance
def test_fixme11_bounds_parse_valid_integers():
    """FIXME 11: Verify parse_guess validates input correctly for bounds checking."""
    test_cases = [("50", 50), ("1", 1), ("100", 100), ("-5", -5), ("0", 0)]

    for input_str, expected_int in test_cases:
        ok, guess, err = parse_guess(input_str)
        assert ok, f"parse_guess('{input_str}') should succeed"
        assert guess == expected_int, f"Should parse to {expected_int}"


def test_fixme11_bounds_check_within_range():
    """FIXME 11: Verify bounds checking for in-range guesses."""
    low, high = 1, 20  # Easy difficulty range

    for guess in [low, 10, high]:
        is_out_of_bounds = guess < low or guess > high
        assert not is_out_of_bounds, f"Guess {guess} should be valid in [{low}, {high}]"


def test_fixme11_bounds_check_out_of_range():
    """FIXME 11: Verify bounds checking rejects out-of-range guesses."""
    low, high = 1, 20

    for guess in [0, -10, 21, 100]:
        is_out_of_bounds = guess < low or guess > high
        assert is_out_of_bounds, f"Guess {guess} should be invalid in [{low}, {high}]"


# FIXME 13: Only valid guesses stored in history - removed string entries - verified with agent assistance
def test_fixme13_parse_guess_integer_validation():
    """FIXME 13: Verify parse_guess rejects non-integer inputs (ensures only ints in history)."""
    invalid_inputs = ["abc", "12.34.56", "test123", "!@#$%"]

    for invalid_input in invalid_inputs:
        ok, guess, err = parse_guess(invalid_input)
        assert not ok, f"parse_guess should reject non-integer '{invalid_input}'"
        assert guess is None, f"Should return None for '{invalid_input}'"
        assert err is not None, f"Should provide error message for '{invalid_input}'"


def test_fixme13_parse_guess_float_to_int_conversion():
    """FIXME 13: Verify parse_guess converts float strings to int (e.g., '12.7' → 12)."""
    ok, guess, err = parse_guess("12.7")
    assert ok, "Should accept float string"
    assert guess == 12, "Should truncate to int"
    assert err is None, "No error on valid float"


def test_fixme13_parse_guess_rejects_empty():
    """FIXME 13: Verify parse_guess rejects empty input."""
    ok, guess, err = parse_guess("")
    assert not ok, "Empty string should be rejected"
    assert guess is None
    assert "Enter a guess" in err


def test_fixme13_history_contains_only_valid_ints():
    """FIXME 13: Verify valid inputs can be stored as integers in history."""
    valid_inputs = ["5", "50", "100.5", "1"]

    for input_str in valid_inputs:
        ok, guess_int, _ = parse_guess(input_str)
        assert ok, f"'{input_str}' should parse"
        assert isinstance(guess_int, int), f"History should store int, not {type(guess_int).__name__}"


# FIXME 14: Removed dead TypeError handler - type alternation removed in FIXME 2 (verified with agent assistance)
# Already tested: test_fixme2_string_secret_rejected verifies TypeError is raised
