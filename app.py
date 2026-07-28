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
st.title("🛰️ COSMIC-324: Cognitive LEO & Spectrum-Aware Platform")
st.markdown("""
Welcome to the state-of-the-art cognitive simulation core of **COSMIC-324**. Featuring dynamic frequency spectrum allocation, 
throughput estimation, live space weather interference modeling, and autonomous NTN link tracking.
""")

# شريط جانبي (Sidebar) للتحكم المتقدم والابتكار الطيفي الجديد
st.sidebar.header("📡 Cognitive Spectrum & Weather")
spectrum_band = st.sidebar.selectbox("Frequency Band", ["S-Band (Direct-to-Cell)", "Ku-Band (Standard Broadband)", "Ka-Band (High-Throughput HTS)"])
space_weather = st.sidebar.selectbox("Space Weather Condition", ["Clear Sky (Optimal)", "Solar Radiation Storm (Interference)"])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Orbital & Network Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", min_value=5, max_value=20, value=10, step=1)
base_latency = st.sidebar.slider("Base Latency (ms)", min_value=2.0, max_value=5.0, value=3.7, step=0.1)
growth_factor = st.sidebar.slider("Growth Rate Factor", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
elevation_threshold = st.sidebar.slider("Min Elevation Angle (°)", min_value=10, max_value=40, value=25, step=5)

# خصائص النطاق الترددي المبتكرة
if "S-Band" in spectrum_band:
    band_throughput = 5.0   # Mbps (منخفض نسبياً للجوالات)
    band_penalty = 0.5
elif "Ku-Band" in spectrum_band:
    band_throughput = 50.0  # Mbps
    band_penalty = 0.2
else: # Ka-Band
    band_throughput = 150.0 # Mbps (عالي جداً)
    band_penalty = 0.0

weather_penalty = 3.5 if "Storm" in space_weather else 0.0

# حساب البيانات المتقدمة
steps = np.arange(1, time_steps + 1)
latencies = base_latency + (steps ** 1.2) * growth_factor * 2 + weather_penalty + band_penalty
elevations = 45 - (steps * 1.5) if "Storm" in space_weather else 45 - (steps * 1.2)
connection_status = ["Connected (Active)" if (el >= elevation_threshold and weather_penalty == 0) else "Storm Interrupted / Handover" for el in elevations]

# حساب سعة النقل الديناميكية لكل خطوة
throughputs = [band_throughput * (1.0 - (i*0.02)) if weather_penalty == 0 else band_throughput * 0.3 for i in range(len(steps))]

# حساب نسبة استقرار الشبكة
active_ratio = (connection_status.count("Connected (Active)") / len(connection_status))

# بناء جدول البيانات المطور لتصديره لاحقاً
df_results = pd.DataFrame({
    "Time_Step": steps,
    "Frequency_Band": spectrum_band,
    "Latency_ms": np.round(latencies, 2),
    "Throughput_Mbps": np.round(throughputs, 2),
    "Elevation_Angle_deg": np.round(elevations, 1),
    "Link_Status": connection_status
})

# 🚨 نظام التنبيه الذكي الطيفي
if space_weather == "Clear Sky (Optimal)" and active_ratio == 1.0:
    st.success(f"🟢 **Spectrum Optimal ({spectrum_band}):** Cognitive resource allocation active. High spectral efficiency achieved.")
elif "Storm" in space_weather:
    st.error("⚡ **Space Weather Alert:** Solar storm attenuating high-frequency signals. Throughput dynamically throttled!")
else:
    st.warning("⚠️ **Network Notice:** Orbital degradation detected. Handover protocol engaged.")

# 📊 مؤشرات الأداء الرئيسية المتقدمة (KPIs)
st.markdown("### 📌 Cognitive System KPIs & Spectrum Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Average Latency", value=f"{np.mean(latencies):.2f} ms", delta=f"{spectrum_band.split()[0]}")
with kpi2:
    st.metric(label="Est. Throughput", value=f"{np.mean(throughputs):.1f} Mbps", delta="High Capacity" if band_throughput > 40 else "Standard")
with kpi3:
    st.metric(label="Active LEO Satellites", value=min(max(int(time_steps / 2), 3), 6))
with kpi4:
    st.metric(label="Link Health Index", value=f"{active_ratio * 100:.0f}%", delta="Stable" if active_ratio >= 0.7 else "Degraded")

# شريط تقدم صحة الشبكة
st.progress(active_ratio, text="Cognitive Constellation Health Index")

st.markdown("---")

# تقسيم الشاشة إلى عمودين للرسوم البيانية المتقدمة
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
    st.subheader("🌐 Cognitive Network Topology")
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
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, 
            font_size=8, font_color="white", font_weight="bold", ax=ax_net, edge_color='gray')
    
    ax_net.set_title("COSMIC-324: Cognitive Links")
    st.pyplot(fig_net)

# قسم البيانات والتقارير المحدثة
st.markdown("---")
st.subheader("📊 Cognitive Simulation Report & Spectrum Log")
st.dataframe(df_results, use_container_width=True)

# زر التصدير المحدث
csv_data = df_results.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Cognitive Spectrum Report (CSV)",
    data=csv_data,
    file_name="COSMIC_324_Cognitive_Spectrum_Report.csv",
    mime="text/csv",
)

st.markdown("---")
st.success("🌟 **Cognitive Horizon Unlocked:** Dynamic frequency bands and real-time throughput calculations are fully deployed!")
