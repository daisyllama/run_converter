import streamlit as st
from math import floor

def format_seconds_to_mmss(total_seconds):
    if total_seconds is None:
        return "N/A"
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def format_seconds_to_hhmmss(total_seconds):
    if total_seconds is None:
        return "N/A"
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

st.set_page_config(
    page_title="Running Metric Converter",
    page_icon="🏃",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🏃 Running Metric Converter")

tabs = st.tabs(["Convert Speed", "Calculate Time"])

with tabs[0]:
    st.header("Input Your Run Deets")
    unit = st.radio("Distance Unit", ["Kilometers (km)", "Miles (mi)"], index=0, key="unit1")
    if unit == "Kilometers (km)":
        distance = st.number_input(
            "Total Distance (km)",
            min_value=0.01,
            value=5.0,
            step=0.1,
            format="%.2f",
            help="Enter the total distance you ran in kilometers.",
            key="distance1"
        )
        distance_km = distance
    else:
        distance = st.number_input(
            "Total Distance (mi)",
            min_value=0.01,
            value=3.11,
            step=0.01,
            format="%.2f",
            help="Enter the total distance you ran in miles.",
            key="distance1"
        )
        distance_km = distance * 1.60934
col1, col2 = st.columns(2)
with col1:
    input_minutes = st.number_input(
        "Minutes",
        min_value=0,
        value=30,
        step=1,
        help="Enter the minutes part of your total run time.",
        key="minutes1"
    )
    with col2:
        input_seconds = st.number_input(
            "Seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            help="Enter the seconds part of your total run time.",
            key="seconds1"
        )
        total_minutes = input_minutes + input_seconds / 60
if distance_km > 0 and total_minutes > 0:
    total_seconds = total_minutes * 60
    pace_per_km_seconds = total_seconds / distance_km
    pace_per_400m_seconds = pace_per_km_seconds * 0.4
    pace_400m_formatted = format_seconds_to_mmss(pace_per_400m_seconds)
    if unit == "Kilometers (km)":
        pace_per_unit_seconds = pace_per_km_seconds
        pace_per_unit_label = "Pace per 1km"
    else:
        pace_per_unit_seconds = total_seconds / (distance_km / 1.60934)
        pace_per_unit_label = "Pace per 1mi"
    pace_per_unit_formatted = format_seconds_to_mmss(pace_per_unit_seconds)
    if unit == "Kilometers (km)":
        speed = distance_km / (total_minutes / 60) if total_minutes > 0 else 0
        speed_formatted = f"{speed:.2f} km/h"
    else:
        distance_mi = distance_km / 1.60934
        speed = distance_mi / (total_minutes / 60) if total_minutes > 0 else 0
        speed_formatted = f"{speed:.2f} mi/h"
    total_time_hhmmss = format_seconds_to_hhmmss(total_seconds)
    st.header("Calculated Metrics")
    st.markdown("Here are your converted running metrics:")
    m1, m2, m3 = st.columns(3)
    m1.metric("Pace per 400m", pace_400m_formatted)
    m2.metric(pace_per_unit_label, pace_per_unit_formatted)
    m3.metric(f"Speed ({'km/h' if unit == 'Kilometers (km)' else 'mi/h'})", speed_formatted)
else:
    st.warning("Please enter valid positive numbers for both distance and time to see the calculations.")

# with tabs[1]:
#     st.header("Predict Time for a Run")
#     unit2 = st.radio("Distance Unit", ["Kilometers (km)", "Miles (mi)"], index=0, key="unit2")
#     col1, col2 = st.columns(2)
#     with col1:
#         if unit2 == "Kilometers (km)":
#             distance2 = st.number_input(
#                 "Total Distance (km)",
#                 min_value=0.01,
#                 value=5.0,
#                 step=0.1,
#                 format="%.2f",
#                 help="Enter the total distance you want to run in kilometers.",
#                 key="distance2"
#             )
#             distance2_km = distance2
#         else:
#             distance2 = st.number_input(
#                 "Total Distance (mi)",
#                 min_value=0.01,
#                 value=3.11,
#                 step=0.01,
#                 format="%.2f",
#                 help="Enter the total distance you want to run in miles.",
#                 key="distance2"
#             )
#             distance2_km = distance2 * 1.60934
#     with col2:
#         method = st.radio("Input Type", ["Speed", "Pace"], key="method")
#         if method == "Speed":
#             if unit2 == "Kilometers (km)":
#                 speed_input = st.number_input("Speed (km/h)", min_value=0.1, value=10.0, step=0.1, key="speed")
#                 time_hours = distance2_km / speed_input
#             else:
#                 speed_input = st.number_input("Speed (mi/h)", min_value=0.1, value=6.2, step=0.1, key="speed")
#                 distance2_mi = distance2_km / 1.60934
#                 time_hours = distance2_mi / speed_input
#             total_seconds2 = time_hours * 3600
#         else:
#             if unit2 == "Kilometers (km)":
#                 pace_min = st.number_input("Pace Minutes per km", min_value=0, value=5, step=1, key="pace_min")
#                 pace_sec = st.number_input("Pace Seconds per km", min_value=0, max_value=59, value=0, step=1, key="pace_sec")
#                 pace_seconds = pace_min * 60 + pace_sec
#                 total_seconds2 = pace_seconds * distance2_km
#             else:
#                 pace_min = st.number_input("Pace Minutes per mi", min_value=0, value=8, step=1, key="pace_min")
#                 pace_sec = st.number_input("Pace Seconds per mi", min_value=0, max_value=59, value=0, step=1, key="pace_sec")
#                 pace_seconds = pace_min * 60 + pace_sec
#                 distance2_mi = distance2_km / 1.60934
#                 total_seconds2 = pace_seconds * distance2_mi
#         if distance2_km > 0:
#             st.success(f"Predicted Time: {format_seconds_to_hhmmss(total_seconds2)}")
#         else:
#             st.warning("Please enter a valid distance.")

st.markdown("---")
st.markdown("My grandmother can run faster than you.")
