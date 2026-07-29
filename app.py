import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

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

# 💳 الأسعار والباقات في الشريط الجانبي
st.sidebar.header("💳 Subscription & Billing")
user_tier = st.sidebar.selectbox("Select Your Plan", [
    "Starter Tier ($20/month - Basic S/Ku-Band)", 
    "Enterprise 6G Tier ($150/month - V-Band & Logs)"
])

if "Starter" in user_tier:
    st.sidebar.warning("⚠️ Starter tier limits V-Band features.")
    if st.sidebar.button("🚀 Upgrade to Enterprise 6G ($150/mo)"):
        st.sidebar.success("Upgrade simulated successfully!")
else:
    st.sidebar.success("🌟 Premium Enterprise 6G Active ($150/mo)!")

st.sidebar.markdown("---")
st.sidebar.header("📡 Parameters")
time_steps = st.sidebar.slider("Simulation Time Steps", 5, 20, 10)

st.title("🛰️ COSMIC-324: Next-Gen NTN & 6G Spectrum Platform")
st.write(f"Welcome back, **{st.session_state.username}**. Core stability is optimal.")

steps = np.arange(1, time_steps + 1)
df = pd.DataFrame({
    "Step": steps,
    "Status": ["Active Link"] * len(steps),
    "Latency (ms)": np.round(np.linspace(2.1, 4.3, len(steps)), 2)
})

st.subheader("📊 Live Telemetry Report")
st.dataframe(df, use_container_width=True)
