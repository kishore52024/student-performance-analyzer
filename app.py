
import streamlit as st
import pandas as pd
from pathlib import Path

DATA_FILE = Path("students.csv")
MARK_COLUMNS = [
    "Python",
    "Mathematics",
    "English",
    "ComputerScience",
]

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Student Performance Analyzer")
st.caption("Analyze student marks, grades, and subject performance.")

if not DATA_FILE.exists():
    st.error("students.csv was not found in the project folder.")
    st.stop()

df = pd.read_csv(DATA_FILE)

required = ["Name"] + MARK_COLUMNS
if any(column not in df.columns for column in required):
    st.error("The CSV is missing one or more required columns.")
    st.stop()

if df.empty or df["Name"].isna().any():
    st.error("The CSV must contain student records with names.")
    st.stop()

if df["Name"].astype(str).str.strip().eq("").any():
    st.error("Student names cannot be blank.")
    st.stop()

if df["Name"].duplicated().any():
    st.error("Student names must be unique in this sample app.")
    st.stop()

for column in MARK_COLUMNS:
    numeric = pd.to_numeric(df[column], errors="coerce")
    if numeric.isna().any() or not numeric.between(0, 100).all():
        st.error(f"{column} must contain marks from 0 to 100.")
        st.stop()
    df[column] = numeric

df["Total"] = df[MARK_COLUMNS].sum(axis=1)
df["Average"] = df[MARK_COLUMNS].mean(axis=1).round(2)
df["Percentage"] = df["Average"]
df["Grade"] = df["Percentage"].apply(
    lambda p: (
        "A+" if p >= 90 else
        "A" if p >= 80 else
        "B" if p >= 70 else
        "C" if p >= 60 else
        "D" if p >= 50 else "F"
    )
)

st.sidebar.header("Filters")
selected_students = st.sidebar.multiselect(
    "Select students",
    options=df["Name"].tolist(),
    default=df["Name"].tolist(),
)

filtered = df[df["Name"].isin(selected_students)]

if filtered.empty:
    st.info("Select at least one student from the sidebar.")
    st.stop()

topper = filtered.loc[filtered["Total"].idxmax()]
m1, m2, m3, m4 = st.columns(4)
m1.metric("Students", len(filtered))
m2.metric("Class Average", f"{filtered['Average'].mean():.2f}%")
m3.metric("Highest Scorer", topper["Name"])
m4.metric("Top Total", f"{topper['Total']:.0f}/{len(MARK_COLUMNS) * 100}")

st.subheader("Student Results")
st.dataframe(
    filtered[
        ["Name"] + MARK_COLUMNS
        + ["Total", "Average", "Percentage", "Grade"]
    ],
    use_container_width=True,
    hide_index=True,
)

left, right = st.columns(2)

with left:
    st.subheader("Average Marks by Subject")
    st.bar_chart(filtered[MARK_COLUMNS].mean())

with right:
    st.subheader("Grade Distribution")
    st.bar_chart(filtered["Grade"].value_counts().sort_index())

st.subheader("Download Results")
csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download analyzed results (CSV)",
    data=csv_data,
    file_name="analyzed_results.csv",
    mime="text/csv",
)
