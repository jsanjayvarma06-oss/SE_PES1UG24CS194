import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, accepting=True, tier="general", icu=False):
    return {"is_accepting": accepting, "tier": tier,
            "icu_standby": icu, "patients": patients}


# ---------- process_triage_wards ----------
def test_single_normal_patient():
    wards = [make_ward([{"spo2": 98, "hr": 72, "unconscious": False}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_invalid_wards_not_list():
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)


def test_ward_not_accepting_is_skipped():
    wards = [make_ward([{"spo2": 98, "hr": 72}], accepting=False)]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_sensor_reading_is_flagged_and_skipped():
    wards = [make_ward([{"spo2": 0, "hr": 80}])]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_patient_in_general_ward():
    wards = [make_ward([{"spo2": 95, "hr": 80, "unconscious": True}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_patient_in_outpatient_resets_score():
    wards = [make_ward([{"spo2": 95, "hr": 80, "unconscious": True}],
                       tier="outpatient")]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_low_spo2_adds_60():
    wards = [make_ward([{"spo2": 85, "hr": 80}])]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_icu_standby_adds_25():
    wards = [make_ward([{"spo2": 98, "hr": 72}], icu=True)]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 35


def test_ward_alert_when_more_than_four_flagged():
    patients = [{"spo2": 0, "hr": 80}] * 5
    result = process_triage_wards([make_ward(patients)], 10)
    assert result["status"] == "WARD_ALERT"


# ---------- monitor_oxygen_manifolds ----------
def test_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_pressure_failure_two_consecutive_drops():
    assert monitor_oxygen_manifolds([[5.0, 3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_pressure_normal():
    assert monitor_oxygen_manifolds([[5.0, 4.5, 6.0]]) == "PRESSURE_NORMAL"
