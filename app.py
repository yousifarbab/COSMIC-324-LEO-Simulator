import streamlit as st

st.set_page_config(page_title="COSMIC-324 Secure", page_icon="🔐")

def check_password():
    def password_entered():
        # التأكد من إدخال البيانات وتحويلها لحروف صغيرة لتجنب أخطاء الكتابة
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

if check_password():
    # هنا يوضع كود تطبيقك الأصلي كاملاً
    st.title("🚀 مرحباً بك يا مهندس في منصة COSMIC-324 المحمية")
    st.success("تم التحقق من هويتك بنجاح!")
