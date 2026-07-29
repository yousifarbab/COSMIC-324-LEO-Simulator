import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# 🌐 نظام اللغات الموسع
translations = {
    "English": {
        "portal_title": "🔐 Enterprise Portal",
        "welcome": "Welcome",
        "logout": "Log out",
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "billing": "Subscription & Billing",
        "select_plan": "Select Your Plan",
        "starter_desc": "Starter Tier ($20/month - Basic S/Ku-Band)",
        "enterprise_desc": "Enterprise 6G Tier ($150/month - V-Band & Logs)",
        "starter_warn": "⚠️ Starter tier limits V-Band features.",
        "upgrade_btn": "🚀 Upgrade to Enterprise 6G ($150/mo)",
        "upgrade_success": "Upgrade simulated successfully!",
        "active_prem": "🌟 Premium Enterprise 6G Active ($150/mo)!",
        "parameters": "📡 Parameters",
        "time_steps": "Simulation Time Steps",
        "main_title": "🛰️ COSMIC-324: Next-Gen NTN & 6G Spectrum Platform",
        "operating_normal": "Welcome back, Engineer. You are operating the advanced COSMIC-324 core, featuring cognitive multi-band allocation.",
        "spectrum_status": "Spectrum Status (S-Band (Direct-to-Cell)): Resource allocation stable.",
        "kpi_title": "📌 Advanced Enterprise KPIs & Telemetry",
        "avg_latency": "Average Latency",
        "throughput": "Est. Throughput",
        "handovers": "Executed Handovers",
        "efficiency": "Constellation Link Integrity & Efficiency",
        "latency_dynamics": "Latency Dynamics",
        "handover_top": "Handover Topology",
        "telemetry": "📊 Live Telemetry Report",
        "step": "Step",
        "status": "Status",
        "active_link": "Active Link"
    },
    "العربية": {
        "portal_title": "🔐 بوابة المؤسسة",
        "welcome": "أهلاً بك",
        "logout": "تسجيل خروج",
        "login": "تسجيل الدخول",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "billing": "الاشتراكات والفوترة",
        "select_plan": "اختر باقتك",
        "starter_desc": "الباقة الأساسية ($20/شهرياً - S/Ku-Band)",
        "enterprise_desc": "باقة المؤسسات 6G ($150/شهرياً - V-Band والسجلات)",
        "starter_warn": "⚠️ الباقة الأساسية تحصر ميزات V-Band.",
        "upgrade_btn": "🚀 الترقية إلى المؤسسات 6G ($150/شهرياً)",
        "upgrade_success": "تمت محاكاة الترقية بنجاح!",
        "active_prem": "🌟 باقة المؤسسات 6G المميزة مفعلة ($150/شهرياً)!",
        "parameters": "📡 المعلمات والخصائص",
        "time_steps": "خطوات محاكاة الوقت",
        "main_title": "🛰️ COSMIC-324: منصة طيف الجيل السادس والأقمار الصناعية",
        "operating_normal": "أهلاً بعودتك، مهندس. أنت تشغل نواة COSMIC-324 المتقدمة مع التخصيص المعرفي متعدد النطاقات.",
        "spectrum_status": "حالة الطيف (S-Band المباشر للخلايا): تخصيص الموارد مستقر.",
        "kpi_title": "📌 مؤشرات الأداء المتقدمة للمؤسسات والقياس عن بعد",
        "avg_latency": "متوسط التأخير",
        "throughput": "إنتاجية النطاق المقدرة",
        "handovers": "عمليات التسليم المنفذة",
        "efficiency": "سلامة وكفاءة رابط الكوكبة",
        "latency_dynamics": "ديناميكيات التأخير",
        "handover_top": "طوبولوجيا التسليم",
        "telemetry": "📊 تقرير القياس عن بعد المباشر",
        "step": "الخطوة",
        "status": "الحالة",
        "active_link": "رابط نشط"
    }
}

# 🌍 اختيار اللغة من الشريط الجانبي
selected_lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["English", "العربية"])
t = translations[selected_lang]

# الشريط الجانبي لتسجيل الدخول والحماية
st.sidebar.title(t["portal_title"])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.sidebar.text_input(t["username"], value="Engineer")
    pwd = st.sidebar.text_input(t["password"], type="password")
    if st.sidebar.button(t["login"]):
        if user and pwd:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.rerun()
        else:
            st.sidebar.error("Please enter credentials.")
    st.stop()

st.sidebar.success(f"{t['welcome']}, {st.session_state.username}!")
if st.sidebar.button(t["logout"]):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")

# 💳 الأسعار والباقات في الشريط الجانبي
st.sidebar.header(t["billing"])
user_tier = st.sidebar.selectbox(t["select_plan"], [
    t["starter_desc"], 
    t["enterprise_desc"]
])

if "Starter" in user_tier or "الباقة الأساسية" in user_tier:
    st.sidebar.warning(t["starter_warn"])
    if st.sidebar.button(t["upgrade_btn"]):
        st.sidebar.success(t["upgrade_success"])
else:
    st.sidebar.success(t["active_prem"])

st.sidebar.markdown("---")
st.sidebar.header(t["parameters"])
time_steps = st.sidebar.slider(t["time_steps"], 5, 20, 10)

# الواجهة الرئيسية للمنصة
st.title(t["main_title"])
st.write(t["operating_normal"])

# حالة الطيف
st.info(t["spectrum_status"])

# مؤشرات الأداء المتقدمة (KPIs)
st.subheader(t["kpi_title"])
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=t["avg_latency"], value="3.64 ms")
with col2:
    st.metric(label=t["throughput"], value="4.7 Mbps")
with col3:
    st.metric(label=t["handovers"], value="0 Events")

st.progress(88, text=t["efficiency"])

# قسم الرسوم والمخططات
col_a, col_b = st.columns(2)
with col_a:
    st.subheader(t["latency_dynamics"])
    chart_data = pd.DataFrame(np.random.randn(20, 1) / 5 + 3.6, columns=["Latency"])
    st.line_chart(chart_data)

with col_b:
    st.subheader(t["handover_top"])
    st.bar_chart(pd.DataFrame([10, 25, 15, 30], columns=["Value"]))

# جدول القياس عن بعد المباشر
steps = np.arange(1, time_steps + 1)
df = pd.DataFrame({
    t["step"]: steps,
    t["status"]: [t["active_link"]] * len(steps),
    "Latency (ms)": np.round(np.linspace(3.1, 4.2, len(steps)), 2)
})

st.subheader(t["telemetry"])
st.dataframe(df, use_container_width=True)
