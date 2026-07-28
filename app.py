import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import datetime

# إعدادات صفحة الويب
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# 🔐 نظام تسجيل الدخول في الشريط الجانبي
st.sidebar.title("🔐 Enterprise Portal")
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username_input = st.sidebar.text_input("Username", value="Engineer")
    password_input = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username_input and password_input:
            st.session_state.logged_in = True
            st.session_state.username = username_input
            st.rerun()
        else:
            st.sidebar.error("Please enter credentials.")
    st.stop()

st.sidebar.success(f"Welcome, {st.session_state.username}!")
if st.sidebar.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")

# 💳 قسم باقات الاشتراك والأسعار في أعلى الشريط الجانبي
st.sidebar.header("💳 Subscription & Billing")
user_tier = st.sidebar.selectbox("Select Your Plan", [
    "Starter Tier ($20/month - Basic S/Ku-Band)", 
    "Enterprise 6G Tier ($150/month - V-Band & Logs)"
])

if "Starter" in user_tier:
    st.sidebar.warning("⚠️ Starter tier restricts V-Band features.")
    if st.sidebar.button("🚀 Upgrade to Enterprise 6G ($150/mo)"):
        st.sidebar.success("Upgrade simulated successfully! [Demo]")
else:
    st.sidebar.success("🌟 Premium Enterprise 6G Active ($150/mo)!")

st.sidebar.markdown("---")

# عنوان لوحة التحكم الرئيسية
st.title("🛰️ COSMIC-324: Next-Gen NTN & 6G Spectrum Platform")
st.markdown(f"""
Welcome back, **{st.session_state.username}**. You are operating the advanced **COSMIC-324** core, 
featuring cognitive multi-band allocation and automated LEO handover protocols.
""")

# شريط جانبي للتحكم بالترددات
st.sidebar.header("📡 Cognitive Spectrum & Weather")

if "Starter" in user_tier:
    spectrum_band = st.sidebar.selectbox("Frequency Band", [
        "S-Band (Direct-to-Cell)", 
        "Ku-Band (Standard Broadband)"
    ])
    st.sidebar.info("💡 Upgrade to Enterprise 6G to unlock V-Band & Ka-Band.")
else:
    spectrum_band = st.sidebar.selectbox("Frequency Band", [
        "S-Band (Direct-to-Cell)", 
        "Ku-Band (Standard Broadband)", 
        "Ka-Band (High-Throughput HTS)",
        "V-Band (6G Optical / Ultra-High Density)"
    ])

space_weather = st.sidebar.selectbox("Space Weather Condition", ["Clear Sky (Optimal)", "Solar Radiation Storm (Interference)"])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Orbital & Network Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", min_value=5, max_value=20, value=10, step=1)
base_latency = st.sidebar.slider("Base Latency (ms)", min_value=1.5, max_value=5.0, value=2.5, step=0.1)
growth_factor = st.sidebar.slider("Growth Rate Factor", min_value=0.01, max_value=0.1, value=0.04, step=0.01)
elevation_threshold = st.sidebar.slider("Min Elevation Angle (°)", min_value=10, max_value=40, value=25, step=5)

# خصائص النطاق الترددي
if "S-Band" in spectrum_band:
    band_throughput = 5.0
    band_penalty = 0.5
elif "Ku-Band" in spectrum_band:
    band_throughput = 50.0
    band_penalty = 0.2
elif "Ka-Band" in spectrum_band: 
    band_throughput = 150.0
    band_penalty = 0.0
else: 
    band_throughput = 500.0
    band_penalty = -0.3

weather_penalty = 4.0 if "Storm" in space_weather else 0.0

# حساب البيانات
steps = np.arange(1, time_steps + 1)
latencies = base_latency + (steps ** 1.2) * growth_factor * 2 + weather_penalty + band_penalty
elevations = 48 - (steps * 1.8) if "Storm" in space_weather else 48 - (steps * 1.1)

connection_status = []
handovers_triggered = 0
for el in elevations:
    if el >= elevation_threshold and weather_penalty == 0:
        connection_status.append("Connected (Active)")
    else:
        connection_status.append("⚠️ Handover Executed")
        handovers_triggered += 1

throughputs = [band_throughput * (1.0 - (i*0.015)) if weather_penalty == 0 else band_throughput * 0.25 for i in range(len(steps))]
active_ratio = (connection_status.count("Connected (Active)") / len(connection_status))

df_results = pd.DataFrame({
    "Time_Step": steps,
    "Frequency_Band": spectrum_band,
    "Latency_ms": np.round(latencies, 2),
    "Throughput_Mbps": np.round(throughputs, 2),
    "Elevation_Angle_deg": np.round(elevations, 1),
    "Link_State_Protocol": connection_status
})

# التنبيهات الذكية
if "V-Band" in spectrum_band and space_weather == "Clear Sky (Optimal)":
    st.success(f"🚀 **6G V-Band Active:** Ultra-high capacity optical link established.")
elif "Storm" in space_weather:
    st.error("⚡ **Space Weather Alert:** Solar radiation causing atmospheric attenuation.")
else:
    st.info(f"ℹ️ **Spectrum Status ({spectrum_band}):** Resource allocation stable.")

# مؤشرات الأداء الرئيسية (KPIs)
st.markdown("### 📌 Advanced Enterprise KPIs & Telemetry")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Average Latency", value=f"{np.mean(latencies):.2f} ms")
with kpi2:
    st.metric(label="Est. Throughput", value=f"{np.mean(throughputs):.1f} Mbps")
with kpi3:
    st.metric(label="Executed Handovers", value=f"{handovers_triggered} Events")
with kpi4:
    st.metric(label="Link Health Index", value=f"{active_ratio * 100:.0f}%")

st.progress(active_ratio, text="Constellation Link Integrity & Efficiency")
st.markdown("---")

# الرسوم البيانية
col1, col2 = st.columns(2)
with col1:
    st.subheader("📈 Latency Dynamics")
    fig, ax = plt.subplots(figsize=(6, 4))
    color_scheme = '#d62728' if "V-Band" in spectrum_band else '#1f77b4'
    ax.plot(steps, latencies, marker='s', linestyle='-', color=color_scheme, linewidth=2, label=f'Latency')
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

with col2:
    st.subheader("🌐 Handover Topology")
    G = nx.Graph()
    terminal_name = "6G Terminal" if "V-Band" in spectrum_band else "NTN Device"
    G.add_node(terminal_name, pos=(0, 0))
    
    num_sats = min(max(int(time_steps / 2), 3), 7)
    for i in range(1, num_sats + 1):
        sat_name = f"SAT-{i}"
        G.add_node(sat_name, pos=(np.cos(i * 2 * np.pi / num_sats), np.sin(i * 2 * np.pi / num_sats)))
        G.add_edge(terminal_name, sat_name)

    fig_net, ax_net = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    node_colors = ['#ff7f0e' if terminal_name in node else '#2ca02c' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=750, font_size=8, font_color="white", font_weight="bold", ax=ax_net, edge_color='orange')
    st.pyplot(fig_net)

# جدول البيانات والتحميل
st.markdown("---")
st.subheader("📊 Detailed Simulation Telemetry Report")
st.dataframe(df_results, use_container_width=True)

csv_data = df_results.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Telemetry Report (CSV)",
    data=csv_data,
    file_name="COSMIC_324_Telemetry.csv",
    mime="text/csv",
)
