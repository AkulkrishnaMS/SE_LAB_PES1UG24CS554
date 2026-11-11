import math

VALID_ANTIGENS = {"A", "B", "AB", "O"}
RH_MAP = {"+": "Positive", "-": "Negative"}


def validate_blood_type(blood_code):
    """
    Standardizes blood group and Rh factor (e.g. 'O+', 'AB-').
    Returns an error message instead of crashing on invalid input.
    """
    if blood_code is None or not isinstance(blood_code, str):
        return "Invalid Input"

    cleaned = blood_code.strip().upper().replace(" ", "")
    if len(cleaned) < 2:
        return "Invalid Blood Type"

    antigen = cleaned[:-1]
    rh_char = cleaned[-1]

    if antigen not in VALID_ANTIGENS:
        return "Invalid Blood Type"
    if rh_char not in RH_MAP:
        return "Invalid Rh Factor"

    return f"{antigen} {RH_MAP[rh_char]}"


def calculate_pulse_pressure(bp_string):
    """
    Calculates pulse pressure (systolic - diastolic) and arterial ratio.
    Expects 'systolic/diastolic' (e.g. '120/80'); invalid input returns a message.
    """
    if bp_string is None or not isinstance(bp_string, str):
        return "Invalid Input"

    parts = bp_string.strip().split('/')
    if len(parts) != 2:
        return "Invalid BP Format"

    try:
        systolic = int(parts[0].strip())
        diastolic = int(parts[1].strip())
    except ValueError:
        return "Invalid BP Values"

    if systolic <= 0 or diastolic <= 0:
        return "Invalid BP Values"
    if systolic < diastolic:
        return "Invalid BP: systolic must be >= diastolic"

    pulse_diff = systolic - diastolic
    ratio = round(systolic / diastolic, 2)
    return f"Diff: {pulse_diff}, Ratio: {ratio}"


def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Invalid / incomplete records return a message instead of crashing.
    """
    if donor_entry is None or not isinstance(donor_entry, str):
        return "Invalid Record"

    fields = donor_entry.split('|')
    if len(fields) != 3:
        return "Invalid Record Format"

    donor_id = fields[0].strip()
    if not donor_id:
        return "Invalid Donor ID"

    try:
        weight = float(fields[1].strip())
        hemoglobin = float(fields[2].strip())
    except ValueError:
        return "Invalid Numeric Values"

    if not (math.isfinite(weight) and math.isfinite(hemoglobin)):
        return "Invalid Numeric Values"
    if weight <= 0 or hemoglobin <= 0:
        return "Invalid Numeric Values"

    eligible = weight >= 50.0 and hemoglobin >= 12.5
    return f"Donor {donor_id}: {'Eligible' if eligible else 'Deferred'}"


def main():
    print("==== Running validate_blood_type ====")
    b_input = input("Enter blood type (e.g. A+, O-, AB+): ")
    print("Validated:", validate_blood_type(b_input))

    print("\n==== Running calculate_pulse_pressure ====")
    bp_input = input("Enter BP (e.g. 120/80): ")
    print("BP Metrics:", calculate_pulse_pressure(bp_input))

    print("\n==== Running parse_donor_registry ====")
    d_input = input("Enter record (ID|Weight|Hemoglobin): ")
    print("Status:", parse_donor_registry(d_input))


if __name__ == "__main__":
    main()
