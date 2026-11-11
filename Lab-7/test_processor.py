from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry


@given(st.text() | st.none())
def test_validate_blood_type_no_crash(s):
    try:
        result = validate_blood_type(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"validate_blood_type crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_calculate_pulse_pressure_safe(s):
    try:
        result = calculate_pulse_pressure(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"calculate_pulse_pressure crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_donor_registry_safe(s):
    try:
        result = parse_donor_registry(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"parse_donor_registry crashed with: {type(e).__name__}: {e}"


# Extra: fuzz well-formed "sys/dia" strings with random integers
@given(st.integers(min_value=-1000, max_value=1000),
       st.integers(min_value=-1000, max_value=1000))
def test_calculate_pulse_pressure_numeric(sys_val, dia_val):
    try:
        result = calculate_pulse_pressure(f"{sys_val}/{dia_val}")
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"calculate_pulse_pressure crashed on '{sys_val}/{dia_val}': {type(e).__name__}: {e}"


# Extra: fuzz well-formed "ID|Weight|Hb" records with any float values
@given(st.text(alphabet=st.characters(blacklist_characters="|"), max_size=10),
       st.floats(allow_nan=True, allow_infinity=True),
       st.floats(allow_nan=True, allow_infinity=True))
def test_parse_donor_registry_structured(donor_id, weight, hb):
    try:
        result = parse_donor_registry(f"{donor_id}|{weight}|{hb}")
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"parse_donor_registry crashed: {type(e).__name__}: {e}"
