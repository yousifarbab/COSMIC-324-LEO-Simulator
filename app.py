import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import sqlite3
import datetime

# إعدادات صفحة الويب
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# إعداد قاعدة البيانات المحلية لحفظ السجلات
def init_db():
    conn = sqlite3.connect('cosmic_simulations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp TEXT,
            spectrum_band TEXT,
            space_weather TEXT,
            avg_latency REAL,
            link_health REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 🔐 نظام تسجيل الدخول المبسط في الشريط الجانبي
st.sidebar.title("🔐 Enterprise Portal")
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username_input = st.sidebar.text_input("Username", value="Engineer")
    password_input = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username_input and password_input:  # قبول أي بيانات تجريبية صحيحة
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.rerun()
        else:
            st.sidebar.error("Please enter credentials.")
    st.stop() # إيقاف التنفيذ حتى يتم تسجيل الدخول

# إذا تم تسجيل الدخول بنجاح
st.sidebar.success(f"Welcome, {st.session_state.username}!")
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")

# عنوان لوحة التحكم الرئيسية
st.title("🛰️ COSMIC-324: Secure Enterprise LEO & Spectrum Platform")
st.markdown(f"""
Welcome back, **{st.session_state.username}**. You are connected to the secure enterprise simulation core of **COSMIC-324**, 
featuring persistent database logging, cognitive spectrum allocation, and live space weather telemetry.
""")

# شريط جانبي للتحكم المتقدم
st.sidebar.header("📡 Cognitive Spectrum & Weather")
spectrum_band = st.sidebar.selectbox("Frequency Band", ["S-Band (Direct-to-Cell)", "Ku-Band (Standard Broadband)", "Ka-Band (High-Throughput HTS)"])
space_weather = st.sidebar.selectbox("Space Weather Condition", ["Clear Sky (Optimal)", "Solar Radiation Storm (Interference)"])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Orbital & Network Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", min_value=5, max_value=20, value=10, step=1)
base_latency = st.sidebar.slider("Base Latency (ms)", min_value=2.0, max_value=5.0, value=3.7, step=0.1)
growth_factor = st.sidebar.slider("Growth Rate Factor", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
elevation_threshold = st.sidebar.slider("Min Elevation Angle (°)", min_value=10, max_value=40, value=25, step=5)

# خصائص النطاق الترددي
if "S-Band" in spectrum_band:
    band_throughput = 5.0
    band_penalty = 0.5
elif "Ku-Band" in spectrum_band:
    band_throughput = 50.0
    band_penalty = 0.2
else: 
    band_throughput = 150.0
    band_penalty = 0.0

weather_penalty = 3.5 if "Storm" in space_weather else 0.0

# حساب البيانات
steps = np.arange(1, time_steps + 1)
latencies = base_latency + (steps ** 1.2) * growth_factor * 2 + weather_penalty + band_penalty
elevations = 45 - (steps * 1.5) if "Storm" in space_weather else 45 - (steps * 1.2)
connection_status = ["Connected (Active)" if (el >= elevation_threshold and weather_penalty == 0) else "Storm Interrupted / Handover" for el in elevations]
throughputs = [band_throughput * (1.0 - (i*0.02)) if weather_penalty == 0 else band_throughput * 0.3 for i in range(len(steps))]
active_ratio = (connection_status.count("Connected (Active)") / len(connection_status))

# بناء جدول البيانات
df_results = pd.DataFrame({
    "Time_Step": steps,
    "Frequency_Band": spectrum_band,
    "Latency_ms": np.round(latencies, 2),
    "Throughput_Mbps": np.round(throughputs, 2),
    "Elevation_Angle_deg": np.round(elevations, 1),
    "Link_Status": connection_status
})

# زر لحفظ الجلسة الحالية في قاعدة البيانات
if st.button("💾 Save Simulation Run to Database"):
    conn = sqlite3.connect('cosmic_simulations.db')
    c = conn.cursor()
    c.execute("INSERT INTO simulations (username, timestamp, spectrum_band, space_weather, avg_latency, link_health) VALUES (?, ?, ?, ?, ?, ?)",
              (st.session_state.username, str(datetime.datetime.now()), spectrum_band, space_weather, float(np.mean(latencies)), float(active_ratio * 100)))
    conn.commit()
    conn.close()
    st.success("Simulation session successfully saved to secure database!")

# 🚨 التنبيهات
if space_weather == "Clear Sky (Optimal)" and active_ratio == 1.0:
    st.success(f"🟢 **Spectrum Optimal ({spectrum_band}):** Secure cognitive channel active.")
elif "Storm" in space_weather:
    st.error("⚡ **Space Weather Alert:** Solar storm affecting high-frequency signals.")
else:
    st.warning("⚠️ **Network Notice:** Orbital degradation detected.")

# 📊 مؤشرات الأداء الرئيسية (KPIs)
st.markdown("### 📌 Enterprise System KPIs & Database Logs")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Average Latency", value=f"{np.mean(latencies):.2f} ms")
with kpi2:
    st.metric(label="Est. Throughput", value=f"{np.mean(throughputs):.1f} Mbps")
with kpi3:
    st.metric(label="Active LEO Satellites", value=min(max(int(time_steps / 2), 3), 6))
with kpi4:
    st.metric(label="Link Health Index", value=f"{active_ratio * 100:.0f}%")

st.progress(active_ratio, text="Enterprise Constellation Health Index")
st.markdown("---")

# عرض الرسوم البيانية
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Latency & Spectrum Performance")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(steps, latencies, marker='o', linestyle='-', color='#9467bd', linewidth=2, label='Latency (ms)')
    ax.set_title(f"COSMIC-324: {spectrum_band.split()[0]} Performance")
    ax.set_xlabel("Simulation Time Steps")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left')
    st.pyplot(fig)

with col2:
    st.subheader("🌐 Enterprise Network Topology")
    G = nx.Graph()
    terminal_name = "HTS Terminal / Mobile" if "Ka" in spectrum_band else "Mobile Device (NTN)"
    G.add_node(terminal_name, pos=(0, 0))
    
    num_sats = min(max(int(time_steps / 2), 3), 6)
    for i in range(1, num_sats + 1):
        sat_name = f"SAT-LEO-{i}"
        G.add_node(sat_name, pos=(np.cos(i * 2 * np.pi / num_sats), np.sin(i * 2 * np.pi / num_sats)))
        G.add_edge(terminal_name, sat_name, weight=round(latencies[i-1], 2))

    fig_net, ax_net = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    node_colors = ['#1f77b4' if terminal_name in node else '#2ca02c' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=8, font_color="white", font_weight="bold", ax=ax_net, edge_color='gray')
    ax_net.set_title("COSMIC-324: Enterprise Links")
    st.pyplot(fig_net)

# قسم عرض السجلات المحفوظة من قاعدة البيانات
st.markdown("---")
st.subheader("📂 Saved Simulation Logs from Database")
try:
    conn = sqlite3.connect('cosmic_simulations.db')
    df_db = pd.read_sql_query("SELECT * FROM simulations", conn)
    conn.close()
    if not df_db.empty:
        st.dataframe(df_db, use_container_width=True)
    else:
        st.info("No saved simulations in database yet. Adjust parameters and click 'Save Simulation Run to Database'.")
except Exception as e:
    st.write("Database table initializing...")

# جدول البيانات والتحميل
st.markdown("---")
st.subheader("📊 Current Simulation Report")
st.dataframe(df_results, use_container_width=True)

csv_data = df_results.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Simulation Report (CSV)",
    data=csv_data,
    file_name="COSMIC_324_Enterprise_Report.csv",
    mime="text/csv",
)
