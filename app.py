import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

# إعدادات صفحة الويب
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# عنوان لوحة التحكم الرئيسية
st.title("🛰️ COSMIC-324: LEO Satellite Network & Latency Simulator")
st.markdown("""
Welcome to the advanced interactive dashboard of **COSMIC-324**. This upgraded simulation engine models 
Direct-to-Cell (NTN) satellite connectivity, dynamic latency evolution, and network topology interacting with mobile ground terminals.
""")

# شريط جانبي (Sidebar) للتحكم في معلمات المحاكاة المتقدمة
st.sidebar.header("🎛️ Simulation Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", min_value=5, max_value=20, value=10, step=1)
base_latency = st.sidebar.slider("Base Latency (ms)", min_value=2.0, max_value=5.0, value=3.7, step=0.1)
growth_factor = st.sidebar.slider("Growth Rate Factor", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
elevation_threshold = st.sidebar.slider("Min Elevation Angle (°)", min_value=10, max_value=40, value=25, step=5)

# حساب بيانات زمن التأخير وحالة الاتصال المباشر بالجوال (Direct-to-Cell)
steps = np.arange(1, time_steps + 1)
latencies = base_latency + (steps ** 1.2) * growth_factor * 2 

# محاكاة زوايا الارتفاع وحالة الاتصال المباشر للجوال
elevations = 45 - (steps * 1.5)  # زاوية الارتفاع تقل كلما تحرك القمر
connection_status = ["Connected (Active)" if el >= elevation_threshold else "Handover / Weak" for el in elevations]

# بناء جدول البيانات لتصديره لاحقاً
df_results = pd.DataFrame({
    "Time_Step": steps,
    "Latency_ms": np.round(latencies, 2),
    "Elevation_Angle_deg": np.round(elevations, 1),
    "Link_Status": connection_status
})

# تقسيم الشاشة إلى عمودين لعرض النتائج بصرياً
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Signal Latency Evolution over Time")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(steps, latencies, marker='o', linestyle='-', color='#1f77b4', linewidth=2, label='Signal Latency (ms)')
    ax.set_title("COSMIC-324: LEO Satellite Latency")
    ax.set_xlabel("Simulation Time Steps")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("🌐 Direct-to-Cell Network Topology")
    
    G = nx.Graph()
    mobile_device = "Mobile Device (No SIM)"
    G.add_node(mobile_device, pos=(0, 0))
    
    num_sats = min(max(int(time_steps / 2), 3), 6)
    for i in range(1, num_sats + 1):
        sat_name = f"SAT-LEO-{i}"
        G.add_node(sat_name, pos=(np.cos(i * 2 * np.pi / num_sats), np.sin(i * 2 * np.pi / num_sats)))
        G.add_edge(mobile_device, sat_name, weight=round(latencies[i-1], 2))

    fig_net, ax_net = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    
    node_colors = ['#2ca02c' if node == mobile_device else '#1f77b4' for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, 
            font_size=8, font_color="white", font_weight="bold", ax=ax_net, edge_color='gray')
    
    ax_net.set_title("COSMIC-324: NTN Direct-to-Cell Links")
    st.pyplot(fig_net)

# قسم عرض البيانات وتصديرها (CSV Export Section)
st.markdown("---")
st.subheader("📊 Simulation Data & Direct-to-Cell Metrics")
st.dataframe(df_results, use_container_width=True)

# زر تحميل البيانات بصيغة CSV
csv_data = df_results.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Simulation Report (CSV)",
    data=csv_data,
    file_name="COSMIC_324_Simulation_Report.csv",
    mime="text/csv",
)

st.markdown("---")
st.success("🚀 **System Upgraded Successfully:** Direct-to-Cell mobile parameters and CSV export features are now fully integrated!")
