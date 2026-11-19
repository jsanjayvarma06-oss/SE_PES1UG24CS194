import math


def parse_vitals_summary(vitals_csv):
    if not isinstance(vitals_csv, str):
        raise ValueError("vitals must be a string like 'HR,SpO2,Temp'")
    parts = vitals_csv.split(',')
    if len(parts) < 3:
        raise ValueError("expected three comma-separated values")
    hr = float(parts[0])
    spo2 = float(parts[1])
    temp = float(parts[2])
    if not all(math.isfinite(v) for v in (hr, spo2, temp)):
        raise ValueError("vitals must be finite numbers")
    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    if not isinstance(bmi_string, str):
        raise ValueError("input must be a string like 'weight/height'")
    parts = bmi_string.split('/')
    if len(parts) != 2:
        raise ValueError("expected 'weight/height'")
    weight = float(parts[0])
    height = float(parts[1])
    if not (math.isfinite(weight) and math.isfinite(height)):
        raise ValueError("weight and height must be finite numbers")
    if weight <= 0 or height <= 0:
        raise ValueError("weight and height must be positive")
    try:
        bmi = weight / (height ** 2)
    except (ZeroDivisionError, OverflowError):
        raise ValueError("height is out of range")
    return round(bmi, 2)


def assign_ward_bed(allocation_code):
    if not isinstance(allocation_code, str):
        raise ValueError("allocation code must be a string like 'ICU-05'")
    parts = allocation_code.strip().split('-')
    if len(parts) != 2:
        raise ValueError("expected 'WARD-BED'")
    ward, bed_str = parts
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }
    if ward.upper() not in ward_names:
        raise ValueError(f"unknown ward: {ward!r}")
    bed_num = int(bed_str)
    return f"{ward_names[ward.upper()]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()
