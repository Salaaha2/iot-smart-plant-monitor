import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PlantIQ – Smart Plant Monitor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Background */
    .stApp { background-color: #f4f7f4; }

    /* Hide default Streamlit header */
    header[data-testid="stHeader"] { display: none; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e8f0e8;
    }
    div[data-testid="metric-container"] label {
        font-size: 13px !important;
        color: #6b7c6b !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #1a2e1a !important;
    }

    /* Cards */
    .plant-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e8f0e8;
        margin-bottom: 16px;
    }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .badge-green  { background: #e6f4e6; color: #1e7e1e; }
    .badge-yellow { background: #fff8e1; color: #b8860b; }
    .badge-red    { background: #fdecea; color: #c62828; }
    .badge-blue   { background: #e3f2fd; color: #1565c0; }

    /* Section headers */
    .section-title {
        font-size: 15px;
        font-weight: 700;
        color: #2d4a2d;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 2px solid #e8f0e8;
    }

    /* History log rows */
    .log-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #f0f4f0;
        font-size: 14px;
        color: #3d4f3d;
    }
    .log-row:last-child { border-bottom: none; }
    .log-time { color: #8fa08f; font-size: 12px; }

    /* Gauge bar */
    .gauge-track {
        background: #e8f0e8;
        border-radius: 8px;
        height: 12px;
        width: 100%;
        margin: 8px 0;
        overflow: hidden;
    }
    .gauge-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }

    /* App title */
    .app-title {
        font-size: 28px;
        font-weight: 800;
        color: #1a2e1a;
        margin: 0;
        line-height: 1.2;
    }
    .app-subtitle {
        font-size: 14px;
        color: #6b7c6b;
        margin: 4px 0 0 0;
    }

    /* Online dot */
    .dot-online  { color: #22c55e; font-size: 10px; }
    .dot-offline { color: #ef4444; font-size: 10px; }

    /* Chart container */
    div[data-testid="stVegaLiteChart"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

SERVER = "http://localhost:5000"

# Keys

def get_status_info(soil):
    if soil < 30:
        return "Needs Water",  "⚠️ Your plant needs water now",        "badge-red",    "#ef4444"
    elif soil < 60:
        return "Getting Dry",  "🌿 Soil is getting dry — water soon",  "badge-yellow", "#f59e0b"
    elif soil <= 85:
        return "Healthy",      "✅ Your plant is happy and healthy",    "badge-green",  "#22c55e"
    else:
        return "Overwatered",  "💧 Too much water — let soil dry out", "badge-blue",   "#3b82f6"

def fetch(endpoint):
    try:
        r = requests.get(f"{SERVER}/{endpoint}", timeout=3)
        return r.json(), True
    except:
        return None, False

def gauge_color(val, low=30, high=60):
    if val < low:   return "#ef4444"
    if val < high:  return "#f59e0b"
    return "#22c55e"

# ── Session state ─────────────────────────────────────────────
if "last_soil" not in st.session_state:
    st.session_state.last_soil = None
if "last_temp" not in st.session_state:
    st.session_state.last_temp = None
if "last_hum"  not in st.session_state:
    st.session_state.last_hum  = None

# ── Main render loop ──────────────────────────────────────────
placeholder = st.empty()

while True:
    data,    ok1 = fetch("data")
    stats,   ok2 = fetch("stats")
    history, ok3 = fetch("history")
    connected    = ok1 and data and len(data) > 0

    with placeholder.container():

        # ── Header ───────────────────────────────────────────
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1:
            st.markdown('<p class="app-title">🌿 PlantIQ</p>', unsafe_allow_html=True)
            st.markdown('<p class="app-subtitle">Smart Plant Monitor</p>',
                        unsafe_allow_html=True)
        with h_col2:
            if connected:
                st.markdown(
                    '<div style="text-align:right;padding-top:12px">'
                    '<span class="dot-online">●</span>'
                    ' <span style="font-size:13px;color:#6b7c6b">Live</span>'
                    f'<br><span style="font-size:11px;color:#8fa08f">'
                    f'Updated {datetime.now().strftime("%H:%M:%S")}</span></div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="text-align:right;padding-top:12px">'
                    '<span class="dot-offline">●</span>'
                    ' <span style="font-size:13px;color:#6b7c6b">Offline</span></div>',
                    unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        if not connected:
            st.markdown("""
            <div class="plant-card" style="text-align:center;padding:40px">
                <div style="font-size:48px;margin-bottom:12px">📡</div>
                <div style="font-size:18px;font-weight:700;color:#1a2e1a;margin-bottom:8px">
                    Waiting for sensor data
                </div>
                <div style="font-size:14px;color:#6b7c6b">
                    Make sure your ESP32 is powered on and sending data to
                    <code>http://localhost:5000/data</code>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Latest reading
            latest  = data[0]
            soil    = latest[2]
            temp    = latest[3]
            hum     = latest[4]
            ts      = latest[1]

            # Delta vs previous
            d_soil = round(soil - st.session_state.last_soil, 1) if st.session_state.last_soil is not None else None
            d_temp = round(temp - st.session_state.last_temp, 1) if st.session_state.last_temp is not None else None
            d_hum  = round(hum  - st.session_state.last_hum,  1) if st.session_state.last_hum  is not None else None
            st.session_state.last_soil = soil
            st.session_state.last_temp = temp
            st.session_state.last_hum  = hum

            status, message, badge_class, status_color = get_status_info(soil)

            # Status banner
            st.markdown(f"""
            <div class="plant-card" style="
                border-left: 5px solid {status_color};
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 20px 24px;
            ">
                <div style="font-size:36px">
                    {"🌵" if soil < 30 else "🌿" if soil < 60 else "🌱" if soil <= 85 else "💧"}
                </div>
                <div>
                    <span class="badge {badge_class}">{status}</span>
                    <div style="font-size:16px;font-weight:600;color:#1a2e1a;margin-top:4px">
                        {message}
                    </div>
                    <div style="font-size:12px;color:#8fa08f;margin-top:4px">
                        Last reading: {ts}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Metric cards
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("🌱 Soil Moisture",
                          f"{soil}%",
                          delta=f"{d_soil:+.1f}%" if d_soil is not None else None)
            with m2:
                st.metric("🌡 Temperature",
                          f"{temp}°C",
                          delta=f"{d_temp:+.1f}°C" if d_temp is not None else None)
            with m3:
                st.metric("🌫️ Humidity",
                          f"{hum}%",
                          delta=f"{d_hum:+.1f}%" if d_hum is not None else None)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # Gauge bars
            st.markdown('<div class="plant-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">Sensor Levels</p>',
                        unsafe_allow_html=True)

            for label, val, unit, low, high in [
                ("Soil Moisture", soil, "%",  30, 60),
                ("Temperature",   min(temp/50*100, 100), "°C", 20, 60),
                ("Humidity",      hum,  "%",  30, 60),
            ]:
                fill_color = gauge_color(val, low, high)
                display_val = temp if label == "Temperature" else val
                st.markdown(f"""
                <div style="margin-bottom:14px">
                    <div style="display:flex;justify-content:space-between;
                                font-size:13px;color:#3d4f3d;font-weight:600;
                                margin-bottom:4px">
                        <span>{label}</span>
                        <span style="color:{fill_color}">{display_val}{unit}</span>
                    </div>
                    <div class="gauge-track">
                        <div class="gauge-fill"
                             style="width:{min(val,100)}%;background:{fill_color}">
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Charts + Stats side by side
            chart_col, stats_col = st.columns([2, 1])

            with chart_col:
                st.markdown('<div class="plant-card">', unsafe_allow_html=True)
                st.markdown('<p class="section-title">Sensor Trends</p>',
                            unsafe_allow_html=True)

                # Build dataframe from history (reversed so oldest first)
                rows = list(reversed(data[:20]))
                df = pd.DataFrame(rows, columns=["id","timestamp","Soil %",
                                                  "Temp °C","Humidity %"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], format='mixed')
                df = df.set_index("timestamp")

                tab1, tab2, tab3 = st.tabs(["🌱 Soil", "🌡 Temp", "🌫️ Humidity"])
                with tab1:
                    st.line_chart(df[["Soil %"]],
                                  color=["#22c55e"], height=160)
                with tab2:
                    st.line_chart(df[["Temp °C"]],
                                  color=["#f59e0b"], height=160)
                with tab3:
                    st.line_chart(df[["Humidity %"]],
                                  color=["#3b82f6"], height=160)
                st.markdown('</div>', unsafe_allow_html=True)

            with stats_col:
                st.markdown('<div class="plant-card">', unsafe_allow_html=True)
                st.markdown('<p class="section-title">Today\'s Stats</p>',
                            unsafe_allow_html=True)

                if stats:
                    for label, val, unit, color in [
                        ("Avg Soil",     stats["avg_soil"], "%",  "#22c55e"),
                        ("Low Soil",     stats["min_soil"], "%",  "#ef4444"),
                        ("Peak Soil",    stats["max_soil"], "%",  "#3b82f6"),
                        ("Avg Temp",     stats["avg_temp"], "°C", "#f59e0b"),
                        ("Avg Humidity", stats["avg_hum"],  "%",  "#6366f1"),
                        ("Readings",     stats["total_readings"], "", "#8fa08f"),
                    ]:
                        st.markdown(f"""
                        <div style="display:flex;justify-content:space-between;
                                    align-items:center;padding:8px 0;
                                    border-bottom:1px solid #f0f4f0">
                            <span style="font-size:13px;color:#6b7c6b">{label}</span>
                            <span style="font-size:15px;font-weight:700;
                                         color:{color}">{val}{unit}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<p style="color:#8fa08f;font-size:13px">'
                        'No stats yet today</p>',
                        unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Health log
            st.markdown('<div class="plant-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">Plant Health History</p>',
                        unsafe_allow_html=True)

            if history and len(history) > 0:
                badge_map = {
                    "Healthy":     ("badge-green",  "✅"),
                    "Getting Dry": ("badge-yellow", "🌿"),
                    "Needs Water": ("badge-red",    "⚠︎"),
                    "Overwatered": ("badge-blue",   "💧"),
                }
                for row in history[:10]:
                    _, ts_h, status_h, soil_h, msg_h = row
                    badge_cls, icon = badge_map.get(
                        status_h, ("badge-green", "🌱"))
                    st.markdown(f"""
                    <div class="log-row">
                        <div style="display:flex;align-items:center;gap:10px">
                            <span>{icon}</span>
                            <div>
                                <span class="badge {badge_cls}"
                                      style="margin:0;padding:3px 10px;
                                             font-size:11px">{status_h}</span>
                                <div style="font-size:12px;color:#6b7c6b;
                                            margin-top:2px">{msg_h}</div>
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:13px;font-weight:600;
                                        color:#3d4f3d">{soil_h}%</div>
                            <div class="log-time">{ts_h[5:16]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(
                    '<p style="color:#8fa08f;font-size:13px;padding:8px 0">'
                    'No status changes recorded yet. '
                    'History saves automatically as your plant\'s condition changes.'
                    '</p>',
                    unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Footer
            st.markdown("""
            <div style="text-align:center;padding:20px 0 8px;
                        color:#8fa08f;font-size:12px">
                PlantIQ — By: Alykaa Salaah &nbsp;•&nbsp;
                Data saved &nbsp;•&nbsp;
                Refreshes every 5 seconds
            </div>
            """, unsafe_allow_html=True)

    time.sleep(5)