# Student Performance Analyzer

A Python-based project that analyzes student marks, calculates academic performance, assigns grades, and visualizes subject-wise averages.

## Features

- Calculates total marks, average, percentage, and grades.
- Identifies the highest- and lowest-performing students.
- Calculates average marks for each subject.
- Validates missing, non-numeric, and out-of-range marks.
- Exports analyzed results to CSV.
- Generates a subject-performance chart.

## Tech Stack

- Python
- Pandas
- Matplotlib
- CSV

## Project Structure

```text
student-performance-analyzer/
├── main.py
├── students.csv
├── README.md
└── .gitignore
```

## Installation and Usage

1. Install Python 3.
2. Install dependencies:

   ```bash
   python -m pip install pandas matplotlib
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. View the generated `analyzed_results.csv` and `subject_performance.png` files.

## Learning Outcomes

This project demonstrates Python functions, conditional statements, exception handling, CSV data processing, Pandas DataFrames, data visualization, and Git version control.

## Future Improvements

- Add a graphical dashboard.
- Support student search and filtering.
- Generate PDF reports.
- Add a Streamlit web interface.

