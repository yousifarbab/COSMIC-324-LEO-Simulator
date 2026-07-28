import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# إعدادات صفحة الويب
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# عنوان لوحة التحكم الرئيسية
st.title("🛰️ COSMIC-324: LEO Satellite Network & Latency Simulator")
st.markdown("""
Welcome to the interactive dashboard of **COSMIC-324**. This simulation engine models 
the dynamic latency evolution and network topology of Low Earth Orbit (LEO) satellite constellations 
interacting with ground stations.
""")

# شريط جانبي (Sidebar) للتحكم في معلمات المحاكاة
st.sidebar.header("🎛️ Simulation Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", min_value=5, max_value=20, value=10, step=1)
base_latency = st.sidebar.slider("Base Latency (ms)", min_value=2.0, max_value=5.0, value=3.7, step=0.1)
growth_factor = st.sidebar.slider("Growth Rate Factor", min_value=0.01, max_value=0.1, value=0.05, step=0.01)

# تقسيم الشاشة إلى عمودين لعرض النتائج بصرياً
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Signal Latency Evolution over Time")
    
    # حساب بيانات زمن التأخير ديناميكياً بناءً على اختيار المستخدم
    steps = np.arange(1, time_steps + 1)
    # نموذج رياضي بسيط لتزايد التأخير بمرور الوقت
    latencies = base_latency + (steps ** 1.2) * growth_factor * 2 
    
    # رسم المنحنى البياني
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(steps, latencies, marker='o', linestyle='-', color='#1f77b4', linewidth=2, label='Signal Latency (ms)')
    ax.set_title("COSMIC-324: LEO Satellite Latency")
    ax.set_xlabel("Simulation Time Steps")
    ax.set_ylabel("Latency (ms)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("🌐 Dynamic Network Topology")
    
    # بناء شبكة توجيه افتراضية (Graph)
    G = nx.Graph()
    ground_station = "Ground Station"
    G.add_node(ground_station, pos=(0, 0))
    
    # إضافة عدد عشوائي أو منظم من الأقمار الصناعية بناءً على الخطوات
    num_sats = min(max(int(time_steps / 2), 3), 6)
    for i in range(1, num_sats + 1):
        sat_name = f"SAT-LEO-{i}"
        G.add_node(sat_name, pos=(np.cos(i * 2 * np.pi / num_sats), np.sin(i * 2 * np.pi / num_sats)))
        G.add_edge(ground_station, sat_name, weight=round(latencies[i-1], 2))

    # رسم الخريطة الشبكية
    fig_net, ax_net = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    
    # تلوين المحطة الأرضية بالأورانج والأقمار بالأزرق
    node_colors = ['#ff7f0e' if node == ground_station else '#1f77b4' for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, 
            font_size=9, font_color="white", font_weight="bold", ax=ax_net, edge_color='gray')
    
    ax_net.set_title("COSMIC-324: Constellation Topology")
    st.pyplot(fig_net)

# قسم معلومات إضافية وحالة النظام
st.markdown("---")
st.info("💡 **System Status:** Simulation running successfully. Adjust the parameters on the sidebar to observe real-time recalculations of network latency and topology links.")
