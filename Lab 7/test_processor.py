from hypothesis import given, settings, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed

# Inputs: random text, None, plus "almost valid" shaped strings, because purely
# random text almost never contains the right separators (',', '/', '-').
VITALS_LIKE = st.from_regex(r"[-+0-9.eEnaifNAIF]{0,6},[-+0-9.eEnaifNAIF]{0,6},[-+0-9.eEnaifNAIF]{0,6}",
                            fullmatch=True)
BMI_LIKE = st.from_regex(r"[-+0-9.eEnaifNAIF]{0,8}/[-+0-9.eEnaifNAIF]{0,8}", fullmatch=True)
BED_LIKE = st.from_regex(r"[A-Za-z]{0,4}-[0-9]{0,4}", fullmatch=True)


@settings(max_examples=500)
@given(st.text() | st.none() | VITALS_LIKE)
def test_parse_vitals_summary_no_crash(s):
    try:
        result = parse_vitals_summary(s)
    except ValueError:
        return                      # expected: bad input is rejected cleanly
    # any exception other than ValueError is NOT caught -> Hypothesis reports a bug
    assert isinstance(result, str)
    assert result.endswith("CRITICAL") or result.endswith("STABLE")


@settings(max_examples=500)
@given(st.text() | st.none() | BMI_LIKE)
def test_compute_patient_bmi_safe(s):
    try:
        result = compute_patient_bmi(s)
    except ValueError:
        return
    assert isinstance(result, float)
    assert result == result and result >= 0     # not NaN, non-negative


@settings(max_examples=500)
@given(st.text() | st.none() | BED_LIKE)
def test_assign_ward_bed_safe(s):
    try:
        result = assign_ward_bed(s)
    except ValueError:
        return
    assert isinstance(result, str)
    assert "Bed #" in result
