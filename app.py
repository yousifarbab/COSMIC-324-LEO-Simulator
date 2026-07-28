import streamlit as st

# إعدادات الصفحة
st.set_page_title_config(page_title="COSMIC-324 Secure", page_icon="🔐")

# دالة التحقق من تسجيل الدخول
def check_password():
    """Returns True if the user had the correct password."""

    def password_entered():
        if (
            st.session_state["username"] == "engineer"
            and st.session_state["password"] == "12345"
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # عدم الاحتفاظ بكلمة المرور في الذاكرة
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # شاشة تسجيل الدخول الأولى
        st.subheader("🔐 يرجى تسجيل الدخول للوصول إلى المنصة")
        st.text_input("اسم المستخدم", key="username")
        st.text_input("كلمة المرور", type="password", key="password")
        st.button("دخول", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # إذا كانت كلمة المرور خطأ
        st.subheader("🔐 يرجى تسجيل الدخول للوصول إلى المنصة")
        st.text_input("اسم المستخدم", key="username")
        st.text_input("كلمة المرور", type="password", key="password")
        st.button("دخول", on_click=password_entered)
        st.error("😕 اسم المستخدم أو كلمة المرور غير صحيحة")
        return False
    else:
        # كلمة المرور صحيحة
        return True

# تطبيق الحماية
if check_password():
    # ---------------------------------------------------------
    # ضع كود مشروعك الأصلي (واجهة المحاكاة والجداول والخرائط هنا)
    # ---------------------------------------------------------
    st.title("🚀 مرحباً بك يا مهندس في منصة COSMIC-324 المحمية")
    st.success("تم التحقق من هويتك بنجاح. جميع الخوارزميات والبيانات مؤمنة.")
    
    # مثال على محتواك:
    st.write("هنا تظهر أدوات التحليل والخوارزميات الخاصة بك...")
