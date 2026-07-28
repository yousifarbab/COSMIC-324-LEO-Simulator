import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الصفحة
st.set_page_config(
    page_title="COSMIC-324 LEO Simulator",
    page_icon="🛰️",
    layout="wide"
)

# 🌐 نظام اللغات الموسع (يشمل 5 لغات عالمية)
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
        "operating_normal": "System operating normally with cognitive multi-band allocation.",
        "telemetry": "📊 Live Telemetry Report",
        "step": "Step",
        "status": "Status",
        "latency": "Latency (ms)",
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
        "operating_normal": "النظام يعمل بشكل طبيعي مع التخصيص المعرفي متعدد النطاقات.",
        "telemetry": "📊 تقرير القياس عن بعد المباشر",
        "step": "الخطوة",
        "status": "الحالة",
        "latency": "التأخير (مللي ثانية)",
        "active_link": "رابط نشط"
    },
    "Français": {
        "portal_title": "🔐 Portail d'Entreprise",
        "welcome": "Bienvenue",
        "logout": "Déconnexion",
        "login": "Connexion",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "billing": "Abonnement et Facturation",
        "select_plan": "Sélectionnez votre offre",
        "starter_desc": "Offre Starter (20$/mois - S/Ku-Band)",
        "enterprise_desc": "Offre Enterprise 6G (150$/mois - V-Band)",
        "starter_warn": "⚠️ L'offre Starter limite les fonctionnalités V-Band.",
        "upgrade_btn": "🚀 Passer à Enterprise 6G (150$/mois)",
        "upgrade_success": "Mise à niveau simulée avec succès !",
        "active_prem": "🌟 Enterprise 6G Actif (150$/mois) !",
        "parameters": "📡 Paramètres",
        "time_steps": "Étapes de simulation",
        "main_title": "🛰️ COSMIC-324: Plateforme NTN & Spectre 6G",
        "operating_normal": "Système opérationnel avec allocation multi-bandes.",
        "telemetry": "📊 Rapport de Télémétrie en Direct",
        "step": "Étape",
        "status": "Statut",
        "latency": "Latence (ms)",
        "active_link": "Lien Actif"
    },
    "Español": {
        "portal_title": "🔐 Portal Empresarial",
        "welcome": "Bienvenido",
        "logout": "Cerrar sesión",
        "login": "Iniciar sesión",
        "username": "Usuario",
        "password": "Contraseña",
        "billing": "Suscripción y Facturación",
        "select_plan": "Selecciona tu plan",
        "starter_desc": "Nivel Starter ($20/mes - S/Ku-Band)",
        "enterprise_desc": "Nivel Enterprise 6G ($150/mes - V-Band)",
        "starter_warn": "⚠️ El nivel Starter limita las funciones de V-Band.",
        "upgrade_btn": "🚀 Actualizar a Enterprise 6G ($150/mes)",
        "upgrade_success": "¡Actualización simulada con éxito!",
        "active_prem": "🌟 ¡Enterprise 6G Activo ($150/mes)!",
        "parameters": "📡 Parámetros",
        "time_steps": "Pasos de Simulación",
        "main_title": "🛰️ COSMIC-324: Plataforma NTN y Espectro 6G",
        "operating_normal": "Sistema operando normalmente con asignación multibanda.",
        "telemetry": "📊 Reporte de Telemetría en Vivo",
        "step": "Paso",
        "status": "Estado",
        "latency": "Latencia (ms)",
        "active_link": "Enlace Activo"
    },
    "Deutsch": {
        "portal_title": "🔐 Unternehmensportal",
        "welcome": "Willkommen",
        "logout": "Abmelden",
        "login": "Anmelden",
        "username": "Benutzername",
        "password": "Passwort",
        "billing": "Abonnement & Abrechnung",
        "select_plan": "Wählen Sie Ihren Plan",
        "starter_desc": "Starter-Tarif ($20/Monat - S/Ku-Band)",
        "enterprise_desc": "Enterprise 6G-Tarif ($150/Monat - V-Band)",
        "starter_warn": "⚠️ Der Starter-Tarif schränkt V-Band ein.",
        "upgrade_btn": "🚀 Auf Enterprise 6G upgraden ($150/Mo)",
        "upgrade_success": "Upgrade erfolgreich simuliert!",
        "active_prem": "🌟 Premium Enterprise 6G Aktiv ($150/Mo)!",
        "parameters": "📡 Parameter",
        "time_steps": "Simulationsschritte",
        "main_title": "🛰️ COSMIC-324: Next-Gen NTN & 6G Plattform",
        "operating_normal": "System arbeitet normal mit kognitiver Mehrbandzuweisung.",
        "telemetry": "📊 Live-Telemetriebericht",
        "step": "Schritt",
        "status": "Status",
        "latency": "Latenz (ms)",
        "active_link": "Aktive Verbindung"
    }
}

# 🌍 اختيار اللغة من القائمة المنسدلة
selected_lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["English", "العربية", "Français", "Español", "Deutsch"])
t = translations[selected_lang]

# الشريط الجانبي لتسجيل الدخول
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

# 💳 الأسعار والباقات مع دعم اللغات المتعددة
st.sidebar.header(t["billing"])
user_tier = st.sidebar.selectbox(t["select_plan"], [
    t["starter_desc"], 
    t["enterprise_desc"]
])

if "Starter" in user_tier or "Offre Starter" in user_tier or "Nivel Starter" in user_tier or "Starter-Tarif" in user_tier or "الباقة الأساسية" in user_tier:
    st.sidebar.warning(t["starter_warn"])
    if st.sidebar.button(t["upgrade_btn"]):
        st.sidebar.success(t["upgrade_success"])
else:
    st.sidebar.success(t["active_prem"])

st.sidebar.markdown("---")
st.sidebar.header(t["parameters"])
time_steps = st.sidebar.slider(t["time_steps"], 5, 20, 10)

# الواجهة الرئيسية
st.title(t["main_title"])
st.write(f"{t['welcome']} **{st.session_state.username}**. {t['operating_normal']}")

# جدول البيانات
steps = np.arange(1, time_steps + 1)
df = pd.DataFrame({
    t["step"]: steps,
    t["status"]: [t["active_link"]] * len(steps),
    t["latency"]: np.round(np.linspace(2.1, 4.3, len(steps)), 2)
})

st.subheader(t["telemetry"])
st.dataframe(df, use_container_width=True)
