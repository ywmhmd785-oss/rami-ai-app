import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. تفعيل مفتاح الـ API الخاص بك مباشرة
GOOGLE_API_KEY = "AQ.Ab8RN6IoLDiulYEKO478aNNtemgEgIOYjZYcNwGdG9WYuY1KDQ"
genai.configure(api_key=GOOGLE_API_KEY)

# توجيهات النظام الصارمة لـ Rami AI
system_prompt = (
    "أنت مساعد ذكاء اصطناعي فائق السرعة اسمك 'Rami AI'. تستجيب لكل شيء بلمح البصر "
    "وبلغة عربية ممتازة وعصرية تشبه الواتساب. ملاحظة صارمة: إذا سألك المستخدم من أين أنت "
    "أو من وين أنت أو أصلك، يجب أن تجيب حرفياً وبفخر: 'إلي الشرف من درعا'."
)

# 2. تصميم واجهة الشات المتقدمة والثابتة كلياً كشاشة واتساب (CSS)
st.set_page_config(page_title="Rami AI - نظام واتساب", layout="centered")

st.markdown("""
<style>
/* تهيئة الخلفية العامة */
.stApp { 
    background-color: #0b141a; 
    color: #e9edef; 
    font-family: 'Segoe UI', sans-serif; 
}

/* تثبيت الهيدر العلوي بشكل دائم */
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #111b21;
    z-index: 999;
    padding: 12px 0;
    border-bottom: 1px solid #222d34;
    text-align: center;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
}
.title-text { color: #00a884; font-size: 24px; font-weight: bold; }
.welcome-text { color: #8696a0; font-size: 13px; margin-top: 4px; }

/* حاوية الشات مع هوامش علوية وسفلية دقيقة للتمرير */
.chat-container { 
    display: flex; 
    flex-direction: column; 
    gap: 10px; 
    margin-top: 100px; 
    margin-bottom: 160px; 
    padding: 10px;
}

/* تصميم فقاعات الواتساب للمحادثة */
.user-bubble { 
    background-color: #005c4b; 
    color: #ffffff; 
    padding: 10px 14px; 
    border-radius: 12px 12px 0px 12px; 
    max-width: 75%; 
    align-self: flex-end; 
    font-size: 15px; 
    margin-left: auto; 
    text-align: right; 
    box-shadow: 0 1px 1px rgba(0,0,0,0.15);
}
.bot-bubble { 
    background-color: #202c33; 
    color: #f0f6fc; 
    padding: 10px 14px; 
    border-radius: 12px 12px 12px 0px; 
    max-width: 75%; 
    align-self: flex-start; 
    font-size: 15px; 
    border: 1px solid #233138; 
    text-align: right; 
    margin-right: auto;
    box-shadow: 0 1px 1px rgba(0,0,0,0.15);
}

/* تثبيت شريط الأدوات بالأسفل على غرار تصميم الواتساب الأصلي */
div[data-testid="stHorizontalBlock"] { 
    position: fixed !important; 
    bottom: 0 !important; 
    left: 50% !important; 
    transform: translateX(-50%) !important; 
    width: 100% !important; 
    max-width: 650px !important; 
    background-color: #111b21 !important; 
    padding: 10px 15px !important; 
    border-radius: 15px 15px 0 0 !important; 
    border-top: 1px solid #222d34 !important; 
    z-index: 1000 !important; 
    box-shadow: 0px -4px 8px rgba(0,0,0,0.4) !important;
}

/* تنسيق العناصر داخل سطر واحد مدمج من الأسفل */
div[data-testid="stColumn"] { 
    display: flex !important; 
    align-items: center !important; 
    justify-content: center !important; 
}
.stFileUploader section { padding: 0px !important; min-height: auto !important; border: none !important; background: transparent !important; }
.stFileUploader label, .stCameraInput label { display: none !important; }
.stCameraInput button { padding: 6px !important; background-color: transparent !important; border: none !important; color: #8696a0 !important; }
.stTextInput input { background-color: #2a3942 !important; color: #ffffff !important; border-radius: 20px !important; border: none !important; padding: 10px 15px !important; }

/* إخفاء النصوص التلقائية داخل أزرار الرفع والكاميرا */
.stFileUploader section div, .stFileUploader section small,
.stCameraInput div, .stCameraInput span, .stCameraInput p, .stCameraInput small {
    display: none !important;
}

/* أزرار الإرسال الدائرية الخضراء */
.stButton button {
    background-color: #00a884 !important;
    color: #ffffff !important;
    border-radius: 50% !important;
    width: 44px !important;
    height: 44px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
}

.icon-container {
    font-size: 26px;
    cursor: pointer;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# عرض الترحيب الثابت أعلى الشاشة وتصحيح الأخطاء الإملائية
st.markdown("""
<div class="fixed-header">
    <div class="title-text">تطبيق Rami AI الذكي 🤖</div>
    <div class="welcome-text">✨ أهلاً وسهلاً بكم، لا تنسوا الصلاة على النبي محمد ﷺ</div>
</div>
""", unsafe_allow_html=True)

# تهيئة الذاكرة والسجل
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# دالة معالجة النصوص والملفات المرفقة مرئياً بشكل نظامي
def process_interaction():
    user_text = st.session_state.get("chat_input", "").strip()
    
    img = None
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
    elif camera_file is not None:
        img = Image.open(camera_file)

    if user_text or img:
        display_text = user_text if user_text else "📸 أرسل صورة"
        st.session_state["chat_history"].append({"role": "المستخدم", "text": display_text})
        
        query_clean = user_text.lower()
        if any(word in query_clean for word in ["من وين", "من اين", "أصلك", "اصلك", "وين اصلك"]):
            st.session_state["chat_history"].append({"role": "Rami AI", "text": "إلي الشرف من درعا ❤️"})
        else:
            try:
                # استخدام أحدث نموذج لعام 2026 لتجنب أخطاء الـ 404 كلياً
                model = genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=system_prompt)
                if img:
                    response = model.generate_content([user_text if user_text else "اشرح لي هذه الصورة بالتفصيل وبشكل ذكي", img])
                else:
                    response = model.generate_content(user_text)
                    
                st.session_state["chat_history"].append({"role": "Rami AI", "text": response.text})
            except Exception as e:
                st.session_state["chat_history"].append({"role": "Rami AI", "text": f"حدث خطأ في الاتصال: {e}"})
        
        st.session_state["chat_input"] = ""

# طباعة رسائل الشات المتتالية بمرونة
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state["chat_history"]:
    bubble_class = "user-bubble" if chat["role"] == "المستخدم" else "bot-bubble"
    st.markdown(f'<div class="{bubble_class}">{chat["text"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# توجيه الشاشة آلياً لآخر رسالة مضافة في الأسفل
st.components.v1.html(
    """
    <script>
        var window_parent = window.parent.document;
        var scroller = window_parent.querySelector('.main .block-container');
        if (scroller) { scroller.scrollTop = scroller.scrollHeight; }
    </script>
    """,
    height=0,
)

# 3. شريط أدوات الواتساب المرتب بدقة من الأسفل
col_img, col_cam, col_text, col_btn = st.columns([1, 1, 5.5, 1])

with col_img:
    st.markdown('<div class="icon-container">🖼️</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], key="file_picker", label_visibility="collapsed")
with col_cam:
    st.markdown('<div class="icon-container">📷</div>', unsafe_allow_html=True)
    camera_file = st.camera_input("", key="camera_picker", label_visibility="collapsed")
with col_text:
    st.text_input("", placeholder="المراسلة...", key="chat_input", label_visibility="collapsed")
with col_btn:
    st.button("◀️", on_click=process_interaction)