import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import time

# إعدادات صفحة الويب
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# عنوان لوحة التحكم الرئيسية
st.title("🛰️ COSMIC-324: Autonomous LEO & Space-Weather Simulator")
st.markdown("""
Welcome to the cutting-edge autonomous simulation core of **COSMIC-324**. Featuring live playback engine, 
Space Weather interference modeling, dynamic NTN link tracking, and smart system alerts.
""")

# شريط جانبي (Sidebar) للتحكم المتقدم والأفق الجديد
st.sidebar.header("🎛️ Simulation Engine & Weather")
sim_mode = st.sidebar.radio("Simulation Mode", ["Static Analysis", "Live Space Playback"])
space_weather = st.sidebar.selectbox("Space Weather Condition", ["Clear Sky (Optimal)", "Solar Radiation Storm (Interference)"])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Orbital Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", min_value=5, max_value=20, value=10, step=1)
base_latency = st.sidebar.slider("Base Latency (ms)", min_value=2.0, max_value=5.0, value=3.7, step=0.1)
growth_factor = st.sidebar.slider("Growth Rate Factor", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
elevation_threshold = st.sidebar.slider("Min Elevation Angle (°)", min_value=10, max_value=40, value=25, step=5)

# تأثير الطقس الفضائي على التأخير وزاوية الارتفاع
weather_penalty = 3.5 if "Storm" in space_weather else 0.0

# حساب بيانات زمن التأخير وحالة الاتصال المباشر بالجوال (Direct-to-Cell)
steps = np.arange(1, time_steps + 1)
latencies = base_latency + (steps ** 1.2) * growth_factor * 2 + weather_penalty
elevations = 45 - (steps * 1.5) if "Storm" in space_weather else 45 - (steps * 1.2)
connection_status = ["Connected (Active)" if (el >= elevation_threshold and weather_penalty == 0) else "Storm Interrupted / Handover" for el in elevations]

# حساب نسبة استقرار الشبكة
active_ratio = (connection_status.count("Connected (Active)") / len(connection_status))

# بناء جدول البيانات لتصديره لاحقاً
df_results = pd.DataFrame({
    "Time_Step": steps,
    "Latency_ms": np.round(latencies, 2),
    "Elevation_Angle_deg": np.round(elevations, 1),
    "Link_Status": connection_status
})

# 🚨 نظام التنبيه الذكي التلقائي (Smart System Alerts)
if space_weather == "Clear Sky (Optimal)" and active_ratio == 1.0:
    st.success("🟢 **Network Status Optimal:** All LEO satellites maintain strong Direct-to-Cell (NTN) line-of-sight links.")
elif "Storm" in space_weather:
    st.error("⚡ **Space Weather Alert:** Solar Radiation Storm detected! Atmospheric drag and signal attenuation causing link degradation.")
else:
    st.warning("⚠️ **Network Notice:** Moderate orbital degradation detected. Handover recommended.")

# 📊 قسم مؤشرات الأداء الرئيسية (KPI Metrics Cards)
st.markdown("### 📌 Real-Time System KPIs & Weather Impact")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Average Latency", value=f"{np.mean(latencies):.2f} ms", delta=f"+{weather_penalty} ms weather" if weather_penalty>0 else "Nominal")
with kpi2:
    st.metric(label="Active LEO Satellites", value=min(max(int(time_steps / 2), 3), 6))
with kpi3:
    st.metric(label="Min Elevation Angle", value=f"{np.min(elevations):.1f}°")
with kpi4:
    st.metric(label="Link Health Index", value=f"{active_ratio * 100:.0f}%", delta="Degraded" if weather_penalty>0 else "Stable")

# شريط تقدم صحة الشبكة المرئي
st.progress(active_ratio, text="Network Constellation Stability Index")

# محاكاة التشغيل الحي (Live Playback Mode) إذا اختارها المستخدم
if sim_mode == "Live Space Playback":
    st.markdown("---")
    st.info("▶️ **Live Playback Engine Active:** Simulating real-time satellite pass over ground mobile terminal...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    status_text.success("✅ Orbital pass telemetry successfully updated in real-time!")

st.markdown("---")

# تقسيم الشاشة إلى عمودين لعرض النتائج بصرياً
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Signal Latency & Space Weather Impact")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(steps, latencies, marker='o', linestyle='-', color='#d62728' if weather_penalty>0 else '#1f77b4', linewidth=2, label='Latency (ms)')
    ax.set_title("COSMIC-324: Latency with Weather Effects")
    ax.set_xlabel("Simulation Time Steps")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left')
    st.pyplot(fig)

with col2:
    st.subheader("🌐 Direct-to-Cell Network Topology")
    
    G = nx.Graph()
    mobile_device = "Mobile Device (NTN)"
    G.add_node(mobile_device, pos=(0, 0))
    
    num_sats = min(max(int(time_steps / 2), 3), 6)
    for i in range(1, num_sats + 1):
        sat_name = f"SAT-LEO-{i}"
        G.add_node(sat_name, pos=(np.cos(i * 2 * np.pi / num_sats), np.sin(i * 2 * np.pi / num_sats)))
        G.add_edge(mobile_device, sat_name, weight=round(latencies[i-1], 2))

    fig_net, ax_net = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    
    node_colors = ['#d62728' if weather_penalty>0 else '#2ca02c' for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, 
            font_size=8, font_color="white", font_weight="bold", ax=ax_net, edge_color='gray')
    
    ax_net.set_title("COSMIC-324: NTN Direct Links")
    st.pyplot(fig_net)

# قسم عرض البيانات وتصديرها (CSV Export Section)
st.markdown("---")
st.subheader("📊 Comprehensive Simulation Report & Data")
st.dataframe(df_results, use_container_width=True)

# زر تحميل البيانات بصيغة CSV
csv_data = df_results.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Full Simulation Report (CSV)",
    data=csv_data,
    file_name="COSMIC_324_Autonomous_Report.csv",
    mime="text/csv",
)

st.markdown("---")
st.success("🚀 **New Horizon Unlocked:** Live Space Weather simulation and Autonomous Playback Engine are fully active!")
