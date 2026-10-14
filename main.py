
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("students.csv")
RESULT_FILE = Path("analyzed_results.csv")
CHART_FILE = Path("subject_performance.png")

MARK_COLUMNS = [
    "Python",
    "Mathematics",
    "English",
    "ComputerScience",
]


def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    return "F"


def load_student_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "students.csv was not found in the project folder."
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = ["Name"] + MARK_COLUMNS
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("The CSV file contains no student records.")

    if df["Name"].isna().any() or (
        df["Name"].astype(str).str.strip() == ""
    ).any():
        raise ValueError("Every student must have a name.")

    if df["Name"].duplicated().any():
        raise ValueError(
            "Duplicate student names found. "
            "Please use unique names in this sample project."
        )

    for column in MARK_COLUMNS:
        original = df[column]
        numeric = pd.to_numeric(original, errors="coerce")

        invalid = numeric.isna() | original.isna()

        if invalid.any():
            rows = (df.index[invalid] + 2).tolist()
            raise ValueError(
                f"Missing or non-numeric marks in '{column}', "
                f"CSV row(s): {rows}"
            )

        out_of_range = (numeric < 0) | (numeric > 100)

        if out_of_range.any():
            rows = (df.index[out_of_range] + 2).tolist()
            raise ValueError(
                f"Marks must be between 0 and 100 in '{column}', "
                f"CSV row(s): {rows}"
            )

        df[column] = numeric

    return df


def analyze_students(df):
    df["Total"] = df[MARK_COLUMNS].sum(axis=1)
    df["Average"] = df[MARK_COLUMNS].mean(axis=1).round(2)
    df["Percentage"] = df["Average"].round(2)
    df["Grade"] = df["Percentage"].apply(calculate_grade)

    return df


def display_report(df):
    print("\n===== STUDENT PERFORMANCE REPORT =====\n")

    print(
        df[
            ["Name", "Total", "Average", "Percentage", "Grade"]
        ].to_string(index=False)
    )

    topper = df.loc[df["Total"].idxmax()]
    lowest = df.loc[df["Total"].idxmin()]

    print("\n===== SUMMARY =====")
    print(f"Number of students: {len(df)}")
    print(f"Class average: {df['Average'].mean():.2f}")
    print(f"Highest scorer: {topper['Name']} ({topper['Total']})")
    print(f"Lowest scorer: {lowest['Name']} ({lowest['Total']})")

    print("\n===== SUBJECT AVERAGES =====")
    subject_averages = df[MARK_COLUMNS].mean().round(2)
    print(subject_averages.to_string())


def save_results(df):
    df.to_csv(RESULT_FILE, index=False)
    print(f"\nResults saved to: {RESULT_FILE}")


def create_chart(df):
    subject_averages = df[MARK_COLUMNS].mean()

    plt.figure(figsize=(9, 5))
    subject_averages.plot(kind="bar")
    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks (out of 100)")
    plt.ylim(0, 100)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=150)
    plt.show()

    print(f"Chart saved to: {CHART_FILE}")


def main():
    try:
        students = load_student_data()
        results = analyze_students(students)
        display_report(results)
        save_results(results)
        create_chart(results)

    except (FileNotFoundError, ValueError) as error:
        print(f"\nInput error: {error}")
        print("Fix the issue in students.csv and run again.")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    main()

import pytest
from main import calculate_grade


@pytest.mark.parametrize(
    "percentage, expected",
    [
        (95, "A+"),
        (85, "A"),
        (75, "B"),
        (65, "C"),
        (55, "D"),
        (40, "F"),
        (90, "A+"),
        (0, "F"),
    ],
)
def test_calculate_grade(percentage, expected):
    assert calculate_grade(percentage) == expected
