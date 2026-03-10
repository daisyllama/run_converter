import streamlit as st


KM_IN_MILE = 1.60934


def to_hhmmss(total_seconds: float | int | None) -> str:
    if total_seconds is None:
        return "N/A"
    seconds_int = max(0, int(round(total_seconds)))
    hours = seconds_int // 3600
    minutes = (seconds_int % 3600) // 60
    seconds = seconds_int % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def to_mmss(total_seconds: float | int | None) -> str:
    if total_seconds is None:
        return "N/A"
    seconds_int = max(0, int(round(total_seconds)))
    minutes = seconds_int // 60
    seconds = seconds_int % 60
    return f"{minutes:02}:{seconds:02}"


def pace_to_speed(pace_seconds_per_unit: float) -> float:
    return 3600 / pace_seconds_per_unit


def speed_to_pace(speed_per_hour: float) -> float:
    return 3600 / speed_per_hour


st.set_page_config(page_title="Run Converter", page_icon="🏃", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --page-bg: #eef2f6;
        --panel-bg: #ffffff;
        --ink: #0f172a;
        --muted-ink: #334155;
        --border: #cbd5e1;
        --accent: #0b7285;
    }
    .stApp {
        background: var(--page-bg);
        color: var(--ink);
    }
    .main .block-container {
        background: var(--panel-bg);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem 1.1rem 2rem 1.1rem;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    }
    .stApp, .stApp * {
        color: var(--ink);
    }
    h1, h2, h3 {
        letter-spacing: 0.01em;
        color: var(--ink);
    }
    p, label, span, div {
        color: var(--muted-ink);
    }
    [data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.5rem;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: var(--ink) !important;
    }
    [data-testid="stSidebar"] {
        background: #d8e1ec;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * {
        color: #0b1324 !important;
    }
    [data-baseweb="input"] input,
    [data-baseweb="select"] input,
    .stNumberInput input,
    textarea {
        background: #ffffff !important;
        color: var(--ink) !important;
    }
    .stNumberInput button,
    [data-baseweb="input"] button {
        background: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
    }
    .stNumberInput button:hover,
    [data-baseweb="input"] button:hover {
        background: #1e293b !important;
        color: #ffffff !important;
    }
    .stButton button,
    .stDownloadButton button {
        background: var(--accent);
        color: #ffffff !important;
        border: none;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--ink) !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom-color: var(--accent) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Run Converter and Quick Calculator")
st.caption("Fast training math for pace, speed, finish time, splits, and quick arithmetic.")

with st.sidebar:
    st.subheader("Quick Preset")
    preset = st.selectbox(
        "Race distance",
        ["Custom", "2.4K", "5K", "10K", "Half Marathon", "Marathon"],
        index=0,
    )

    preset_distances = {
        "Custom": 5.0,
        "2.4K": 2.4,
        "5K": 5.0,
        "10K": 10.0,
        "Half Marathon": 21.097,
        "Marathon": 42.195,
    }
    default_distance = preset_distances[preset]

    st.divider()
    st.write("Tip: Use the same distance/time across tabs for rapid what-if checks.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Pace and Speed", "Finish Time", "Splits", "Quick Math"]
)

with tab1:
    st.subheader("Convert Run Result to Useful Metrics")
    unit = st.radio("Distance unit", ["km", "mi"], horizontal=True)
    if unit == "km":
        distance = st.number_input(
            "Distance (km)", min_value=0.01, value=float(default_distance), step=0.01
        )
        distance_km = distance
    else:
        default_mi = default_distance / KM_IN_MILE
        distance = st.number_input(
            "Distance (mi)", min_value=0.01, value=float(default_mi), step=0.01
        )
        distance_km = distance * KM_IN_MILE

    minutes = st.number_input("Minutes", min_value=0, value=26, step=1)
    seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1)
    total_seconds = minutes * 60 + seconds
    st.info("This panel calculates pace per km, pace per mile, 400m split, and speed.")

    if distance_km > 0 and total_seconds > 0:
        pace_km = total_seconds / distance_km
        pace_mi = total_seconds / (distance_km / KM_IN_MILE)
        speed_kmh = distance_km / (total_seconds / 3600)
        speed_mih = speed_kmh / KM_IN_MILE

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Pace / km", to_mmss(pace_km))
        m2.metric("Pace / mi", to_mmss(pace_mi))
        m3.metric("400m split", to_mmss(pace_km * 0.4))
        m4.metric("Speed", f"{speed_kmh:.2f} km/h | {speed_mih:.2f} mi/h")
    else:
        st.warning("Enter a valid positive distance and time.")

with tab2:
    st.subheader("Predict Finish Time")
    mode = st.radio("Input mode", ["Use pace", "Use speed"], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        predict_unit = st.radio("Distance unit", ["km", "mi"], horizontal=True, key="predict_unit")
        if predict_unit == "km":
            predict_distance = st.number_input(
                "Target distance (km)", min_value=0.01, value=float(default_distance), step=0.01
            )
            predict_distance_km = predict_distance
        else:
            default_predict_mi = default_distance / KM_IN_MILE
            predict_distance = st.number_input(
                "Target distance (mi)", min_value=0.01, value=float(default_predict_mi), step=0.01
            )
            predict_distance_km = predict_distance * KM_IN_MILE

    with c2:
        if mode == "Use pace":
            pace_unit = st.radio("Pace unit", ["per km", "per mi"], horizontal=True)
            pace_minutes = st.number_input("Pace minutes", min_value=0, value=5, step=1)
            pace_seconds = st.number_input("Pace seconds", min_value=0, max_value=59, value=0, step=1)
            base_pace_seconds = pace_minutes * 60 + pace_seconds

            if pace_unit == "per km":
                finish_seconds = base_pace_seconds * predict_distance_km
            else:
                finish_seconds = base_pace_seconds * (predict_distance_km / KM_IN_MILE)
        else:
            speed_unit = st.radio("Speed unit", ["km/h", "mi/h"], horizontal=True)
            speed_value = st.number_input("Speed", min_value=0.1, value=10.0, step=0.1)

            if speed_unit == "km/h":
                finish_seconds = (predict_distance_km / speed_value) * 3600
            else:
                finish_seconds = ((predict_distance_km / KM_IN_MILE) / speed_value) * 3600

    st.success(f"Estimated finish time: {to_hhmmss(finish_seconds)}")

with tab3:
    st.subheader("Generate Splits")
    split_unit = st.radio("Split unit", ["km", "mi"], horizontal=True)
    split_mode = st.radio("Split style", ["Standard", "Custom split length"], horizontal=True)
    total_time_min = st.number_input("Total time minutes", min_value=1, value=50, step=1)
    total_time_sec = st.number_input("Total time seconds", min_value=0, max_value=59, value=0, step=1)

    if split_unit == "km":
        split_distance = st.number_input("Total distance (km)", min_value=0.5, value=float(default_distance), step=0.5)
        split_size = 1.0
        if split_mode == "Custom split length":
            split_size = st.number_input(
                "Your split size (km)", min_value=0.1, max_value=float(split_distance), value=0.4, step=0.1
            )
        n_splits = int(split_distance / split_size)
        unit_distance_km = split_size
        label = "km"
        split_distance_km = split_distance
    else:
        split_distance = st.number_input(
            "Total distance (mi)", min_value=0.5, value=float(default_distance / KM_IN_MILE), step=0.5
        )
        split_size = 1.0
        if split_mode == "Custom split length":
            split_size = st.number_input(
                "Your split size (mi)", min_value=0.1, max_value=float(split_distance), value=0.25, step=0.05
            )
        n_splits = int(split_distance / split_size)
        unit_distance_km = split_size * KM_IN_MILE
        label = "mi"
        split_distance_km = split_distance * KM_IN_MILE

    total_split_seconds = total_time_min * 60 + total_time_sec
    avg_seconds_per_unit = total_split_seconds / max(split_distance, 0.001)
    full_split_seconds = avg_seconds_per_unit * split_size

    if n_splits >= 1:
        rows = []
        cumulative = 0.0
        for split_idx in range(1, n_splits + 1):
            cumulative += full_split_seconds
            rows.append(
                {
                    "Split": f"{split_idx} x {split_size:g} {label}",
                    "Target": to_mmss(full_split_seconds),
                    "Cumulative": to_hhmmss(cumulative),
                }
            )

        remaining_distance = split_distance - (n_splits * split_size)
        if remaining_distance > 0:
            last_leg_seconds = avg_seconds_per_unit * remaining_distance
            cumulative += last_leg_seconds
            rows.append(
                {
                    "Split": f"Last {remaining_distance:.2f} {label}",
                    "Target": to_mmss(last_leg_seconds),
                    "Cumulative": to_hhmmss(cumulative),
                }
            )

        st.dataframe(rows, use_container_width=True, hide_index=True)

        split_pace_km = total_split_seconds / max(split_distance_km, 0.001)
        st.caption(
            f"Average pace: {to_mmss(split_pace_km)} / km | {to_mmss(split_pace_km * KM_IN_MILE)} / mi"
        )
    else:
        st.warning("Set a distance of at least 1 full split unit to generate a split table.")

with tab4:
    st.subheader("Quick Math Pad")
    st.write("Use this for ad hoc calculations: fuelling, cadence totals, cost per race, and more.")

    q1, q2, q3 = st.columns(3)
    with q1:
        a = st.number_input("A", value=10.0, step=1.0)
    with q2:
        b = st.number_input("B", value=2.0, step=1.0)
    with q3:
        op = st.selectbox("Operation", ["A + B", "A - B", "A * B", "A / B", "A % B", "A^B"])

    result = None
    if op == "A + B":
        result = a + b
    elif op == "A - B":
        result = a - b
    elif op == "A * B":
        result = a * b
    elif op == "A / B":
        result = None if b == 0 else a / b
    elif op == "A % B":
        result = None if b == 0 else a % b
    elif op == "A^B":
        result = a**b

    if result is None:
        st.error("Invalid operation (for division/modulo, B cannot be 0).")
    else:
        st.metric("Result", f"{result:,.6g}")

st.markdown("---")
st.caption("Built for quick training decisions on desktop and mobile.")
