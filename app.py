import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="COSMIC-324 Secure & LEO Simulator",
    page_icon="🔐",
    layout="wide"
)

# دالة التحقق من كلمة المرور (القفل المعتمد)
def check_password():
    def password_entered():
        u = st.session_state.get("username", "").strip().lower()
        p = st.session_state.get("password", "").strip()
        
        if u == "engineer" and p == "12345":
            st.session_state["password_correct"] = True
            if "password" in st.session_state: del st.session_state["password"]
            if "username" in st.session_state: del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.subheader("🔐 يرجى تسجيل الدخول للوصول إلى المنصة")
        st.text_input("اسم المستخدم", key="username")
        st.text_input("كلمة المرور", type="password", key="password")
        st.button("دخول", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.subheader("🔐 يرجى تسجيل الدخول للوصول إلى المنصة")
        st.text_input("اسم المستخدم", key="username")
        st.text_input("كلمة المرور", type="password", key="password")
        st.button("دخول", on_click=password_entered)
        st.error("😕 اسم المستخدم أو كلمة المرور غير صحيحة")
        return False
    else:
        return True

# تفعيل نظام الحماية أولاً
if check_password():

    # 🌐 نظام اللغات الموسع
    translations = {
        "English": {
            "welcome": "Welcome",
            "logout": "Log out",
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
            "charts": "📈 Signal & Latency Analysis Charts",
            "step": "Step",
            "status": "Status",
            "latency": "Latency (ms)",
            "active_link": "Active Link"
        },
        "العربية": {
            "welcome": "أهلاً بك",
            "logout": "تسجيل خروج",
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
            "charts": "📈 رسومات تحليل الإشارة والتأخير",
            "step": "الخطوة",
            "status": "الحالة",
            "latency": "التأخير (مللي ثانية)",
            "active_link": "رابط نشط"
        },
        "Français": {
            "welcome": "Bienvenue",
            "logout": "Déconnexion",
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
            "charts": "📈 Graphiques d'analyse du signal",
            "step": "Étape",
            "status": "Statut",
            "latency": "Latence (ms)",
            "active_link": "Lien Actif"
        },
        "Español": {
            "welcome": "Bienvenido",
            "logout": "Cerrar sesión",
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
            "charts": "📈 Gráficos de Análisis de Señal",
            "step": "Paso",
            "status": "Estado",
            "latency": "Latencia (ms)",
            "active_link": "Enlace Activo"
        },
        "Deutsch": {
            "welcome": "Willkommen",
            "logout": "Abmelden",
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
            "charts": "📈 Signal- und Latenzanalyse-Diagramme",
            "step": "Schritt",
            "status": "Status",
            "latency": "Latenz (ms)",
            "active_link": "Aktive Verbindung"
        }
    }

    # الشريط الجانبي واختيار اللغة
    selected_lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["English", "العربية", "Français", "Español", "Deutsch"])
    t = translations[selected_lang]

    st.sidebar.success(f"{t['welcome']}, Engineer!")
    
    if st.sidebar.button(t["logout"]):
        del st.session_state["password_correct"]
        st.rerun()

    st.sidebar.markdown("---")

    # الباقات والفوترة
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

    # الواجهة الرئيسية للمشروع
    st.title(t["main_title"])
    st.write(f"{t['welcome']} **Engineer**. {t['operating_normal']}")

    # توليد بيانات المحاكاة
    steps = np.arange(1, time_steps + 1)
    latency_values = np.round(np.linspace(2.1, 4.3, len(steps)), 2)

    df = pd.DataFrame({
        t["step"]: steps,
        t["status"]: [t["active_link"]] * len(steps),
        t["latency"]: latency_values
    })

    # عرض جدول القياس عن بعد
    st.subheader(t["telemetry"])
    st.dataframe(df, use_container_width=True)

    # إرجاع الرسوم البيانية وتحليل الجهاز
    st.subheader(t["charts"])
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(steps, latency_values, marker='o', color='#00d2ff', linewidth=2, label=t["latency"])
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()
    st.pyplot(fig)
