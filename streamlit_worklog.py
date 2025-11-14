import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ----------------------------
# Constants
# ----------------------------
CSV_FILE = "worklog.csv"  # local CSV file to store work logs

# ----------------------------
# Functions
# ----------------------------
def ensure_csv():
    """Ensure CSV file exists"""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["date", "start", "end", "hours"])
        df.to_csv(CSV_FILE, index=False)

def add_shift(date, start_time, end_time):
    """Add a work shift"""
    ensure_csv()
    df = pd.read_csv(CSV_FILE)

    hours = ""

    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    delta = end - start
    total_seconds = delta.seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    hours = f"{hours}h {minutes}m"

    date_str = date.strftime("%Y-%m-%d")

    new_row = {
        "date": date_str,
        "start": start_time,
        "end": end_time,
        "hours": hours
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success(f"Shift added. [{date_str}] {start_time} - {end_time}")

def calculate_total_hours(df):
    total_seconds = 0
    for val in df["hours"]:
        if pd.isna(val) or val == "":
            continue
        parts = val.split(" ")
        h = int(parts[0].replace("h", ""))
        m = int(parts[1].replace("m", ""))
        total_seconds += h * 3600 + m * 60

    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    return f"{total_hours}h {total_minutes}m"

def view_records():
    """Display all records and total hours"""
    ensure_csv()
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        st.info("No work records yet.")
        return
    st.table(df)
    total = calculate_total_hours(df)
    st.write(f"**Total Work Hours**: {total}")

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("Clocky :alien::briefcase::alarm_clock:")
st.markdown("##### - Your Work Hours Tracker -")

# Add Shift
st.subheader("Add Shift")
shift = st.date_input("Select Date", value=datetime.now())
start_time = st.text_input("Clock In (HH:MM)", value="09:00")
end_time = st.text_input("Clock Out (HH:MM)", value="17:00")

if st.button("Submit"):
    add_shift(shift, start_time, end_time)

# View records
st.subheader("Manage Work Records")
if st.button("View Work Records"):
    view_records()

# Cleanup records
if st.button("Clear All Records"):
    if os.path.exists(CSV_FILE):
        # Overwrite CSV with empty dataframe
        pd.DataFrame(columns=["date", "start", "end", "hours"]).to_csv(CSV_FILE, index=False)
        st.success("All records cleared!")
    else:
        st.warning("No record found.")

# st.balloons()
