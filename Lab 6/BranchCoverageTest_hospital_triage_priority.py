import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, accepting=True, tier="general", icu=False):
    return {"is_accepting": accepting, "tier": tier,
            "icu_standby": icu, "patients": patients}


# ================= process_triage_wards =================

# --- Line 2: `not isinstance(wards, list) or default_acuity_score < 0` ---
def test_wards_not_list_raises():                      # 1st operand True
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)


def test_negative_default_score_raises():              # 1st False, 2nd True
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_zero_default_score_is_valid():                # boundary: 0 is allowed
    assert process_triage_wards([], 0) == {"acuity_score": 0,
                                           "status": "NO_URGENT_CASES"}


# --- Line 8-10: ward loop (zero iterations / skipped / accepted) ---
def test_empty_wards_list():
    assert process_triage_wards([], 10)["status"] == "NO_URGENT_CASES"


def test_ward_not_accepting_skipped():
    result = process_triage_wards(
        [make_ward([{"spo2": 98, "hr": 72}], accepting=False, icu=True)], 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_ward_missing_is_accepting_defaults_to_false():
    result = process_triage_wards([{"patients": [{"spo2": 98, "hr": 72}]}], 10)
    assert result["acuity_score"] == 0


# --- Line 12-13: defaults for tier / patients ---
def test_ward_with_no_patients_key_but_icu_standby():
    result = process_triage_wards([{"is_accepting": True, "icu_standby": True}], 10)
    assert result == {"acuity_score": 25, "status": "TRIAGE_STABLE"}


def test_accepting_ward_with_empty_patients():
    result = process_triage_wards([make_ward([])], 10)
    assert result["status"] == "NO_URGENT_CASES"


# --- Line 16-18: patient field defaults (spo2=95, hr=75, conscious) ---
def test_patient_defaults_used_when_fields_missing():
    result = process_triage_wards([make_ward([{}])], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


# --- Line 20: `spo2 <= 0 or heart_rate <= 0` ---
def test_spo2_zero_flagged():
    r = process_triage_wards([make_ward([{"spo2": 0, "hr": 80}])], 10)
    assert r["acuity_score"] == 0


def test_hr_zero_flagged_with_valid_spo2():
    r = process_triage_wards([make_ward([{"spo2": 98, "hr": 0}])], 10)
    assert r["acuity_score"] == 0


def test_negative_spo2_flagged():
    r = process_triage_wards([make_ward([{"spo2": -5, "hr": 80}])], 10)
    assert r["acuity_score"] == 0


def test_spo2_and_hr_both_valid_boundary_one():
    r = process_triage_wards([make_ward([{"spo2": 1, "hr": 1}])], 10)
    assert r["acuity_score"] == 60          # spo2 1 < 90 -> +60


# --- Line 24-29: unconscious branches ---
def test_unconscious_general_ward_adds_100():
    r = process_triage_wards(
        [make_ward([{"spo2": 95, "hr": 80, "unconscious": True}])], 10)
    assert r == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_outpatient_resets_and_breaks():
    patients = [{"spo2": 98, "hr": 72},                       # +10
                {"spo2": 95, "hr": 80, "unconscious": True},  # reset + break
                {"spo2": 98, "hr": 72}]                       # never reached
    r = process_triage_wards([make_ward(patients, tier="outpatient")], 10)
    assert r == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_unconscious_outpatient_break_still_applies_icu_bonus():
    # break exits only the inner loop, so icu_standby bonus is still added
    r = process_triage_wards(
        [make_ward([{"unconscious": True}], tier="outpatient", icu=True)], 10)
    assert r == {"acuity_score": 25, "status": "TRIAGE_STABLE"}


def test_conscious_patient_in_outpatient_is_normal():
    r = process_triage_wards(
        [make_ward([{"spo2": 98, "hr": 72}], tier="outpatient")], 10)
    assert r["acuity_score"] == 10


# --- Line 30: `spo2 < 90 or heart_rate > 120` (with boundaries) ---
def test_spo2_89_is_critical():
    assert process_triage_wards(
        [make_ward([{"spo2": 89, "hr": 80}])], 10)["acuity_score"] == 60


def test_spo2_90_is_not_critical():                     # boundary
    assert process_triage_wards(
        [make_ward([{"spo2": 90, "hr": 80}])], 10)["acuity_score"] == 10


def test_hr_121_is_critical():
    assert process_triage_wards(
        [make_ward([{"spo2": 98, "hr": 121}])], 10)["acuity_score"] == 60


def test_hr_120_is_not_critical():                      # boundary
    assert process_triage_wards(
        [make_ward([{"spo2": 98, "hr": 120}])], 10)["acuity_score"] == 10


# --- Line 35: icu_standby True / False ---
def test_icu_standby_true_adds_25():
    assert process_triage_wards(
        [make_ward([{"spo2": 98, "hr": 72}], icu=True)], 10)["acuity_score"] == 35


def test_icu_standby_false_adds_nothing():
    assert process_triage_wards(
        [make_ward([{"spo2": 98, "hr": 72}], icu=False)], 10)["acuity_score"] == 10


# --- Multiple wards accumulate ---
def test_multiple_wards_accumulate():
    wards = [make_ward([{"spo2": 98, "hr": 72}]),
             make_ward([{"spo2": 80, "hr": 72}], icu=True)]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10 + 60 + 25


# --- Line 38: `flagged_entries > 4` (boundary 4 vs 5) ---
def test_exactly_four_flagged_is_not_alert():
    r = process_triage_wards([make_ward([{"spo2": 0, "hr": 80}] * 4)], 10)
    assert r["status"] == "NO_URGENT_CASES"


def test_five_flagged_triggers_ward_alert():
    r = process_triage_wards([make_ward([{"spo2": 0, "hr": 80}] * 5)], 10)
    assert r == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_ward_alert_keeps_nonzero_score():
    patients = [{"unconscious": True}] * 5                # 5 flagged, +500
    r = process_triage_wards([make_ward(patients)], 10)
    assert r == {"acuity_score": 500, "status": "WARD_ALERT"}


# --- Line 40: total_acuity == 0 vs not ---
def test_zero_default_score_with_normal_patient_gives_no_urgent_cases():
    r = process_triage_wards([make_ward([{"spo2": 98, "hr": 72}])], 0)
    assert r == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


# ================= monitor_oxygen_manifolds =================

# --- Line 46: empty / None input ---
def test_empty_streams_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_none_streams_no_data():
    assert monitor_oxygen_manifolds(None) == "NO_DATA"


# --- Line 51: empty manifold (inner loop zero iterations) ---
def test_empty_manifold_is_normal():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"


# --- Lines 52-57 ---
def test_two_consecutive_low_readings_fail():
    assert monitor_oxygen_manifolds([[3.9, 3.9]]) == "PRESSURE_FAILURE"


def test_single_low_reading_is_normal():                # streak 1 < 2
    assert monitor_oxygen_manifolds([[3.0]]) == "PRESSURE_NORMAL"


def test_exactly_4_bar_is_not_low():                    # boundary
    assert monitor_oxygen_manifolds([[4.0, 4.0, 4.0]]) == "PRESSURE_NORMAL"


def test_streak_resets_after_normal_reading():
    assert monitor_oxygen_manifolds([[3.0, 5.0, 3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_failure_in_second_manifold():
    assert monitor_oxygen_manifolds([[5.0, 5.0], [3.0, 3.0]]) == "PRESSURE_FAILURE"


def test_streak_does_not_carry_across_manifolds():
    assert monitor_oxygen_manifolds([[5.0, 3.0], [3.0, 5.0]]) == "PRESSURE_NORMAL"
