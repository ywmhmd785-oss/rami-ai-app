import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="Rami AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================
# قراءة مفتاح Gemini بأمان
# =========================
try:
    GOOGLE_API_KEY = st.secrets["AQ.Ab8RN6IoLDiulYEKO478aNNtemgEgIOYjZYcNwGdG9WYuY1KDQ"]
except Exception:
    st.error("لم يتم العثور على GEMINI_API_KEY في Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """
أنت مساعد ذكاء اصطناعي اسمك Rami AI.
تجيب باللغة العربية بطريقة واضحة وعصرية وطبيعية.
كن مفيدًا ومختصرًا عندما يكون السؤال بسيطًا، ومفصلًا عندما يحتاج السؤال إلى شرح.
إذا سألك المستخدم: من وين أنت، من أين أنت، أو ما أصلك،
أجب حرفيًا:
إلي الشرف من درعا ❤️
"""

# =========================
# CSS
# =========================
st.markdown(
    """
<style>
.stApp {
    background-color: #0b141a;
    color: #e9edef;
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    max-width: 700px;
    padding-top: 100px;
    padding-bottom: 130px;
}

.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: #111b21;
    z-index: 999;
    padding: 12px 0;
    text-align: center;
    border-bottom: 1px solid #222d34;
}

.title-text {
    color: #00a884;
    font-size: 24px;
    font-weight: bold;
}

.welcome-text {
    color: #8696a0;
    font-size: 13px;
    margin-top: 4px;
}

.user-bubble {
    background: #005c4b;
    color: white;
    padding: 10px 14px;
    border-radius: 12px 12px 0 12px;
    max-width: 80%;
    margin: 8px 0 8px auto;
    text-align: right;
    direction: rtl;
    word-wrap: break-word;
}

.bot-bubble {
    background: #202c33;
    color: #f0f6fc;
    padding: 10px 14px;
    border-radius: 12px 12px 12px 0;
    max-width: 80%;
    margin: 8px auto 8px 0;
    text-align: right;
    direction: rtl;
    word-wrap: break-word;
}

div[data-testid="stHorizontalBlock"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 700px !important;
    background: #111b21 !important;
    padding: 10px !important;
    border-top: 1px solid #222d34 !important;
    z-index: 1000 !important;
}

.stTextInput input {
    background: #2a3942 !important;
    color: white !important;
    border: none !important;
    border-radius: 22px !important;
}

.stButton button {
    background: #00a884 !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    min-width: 44px !important;
    height: 44px !important;
}

.stFileUploader {
    background: transparent !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# الهيدر
# =========================
st.markdown(
    """
<div class="fixed-header">
    <div class="title-text">تطبيق Rami AI الذكي 🤖</div>
    <div class="welcome-text">
        ✨ أهلاً وسهلاً بكم، لا تنسوا الصلاة على النبي محمد ﷺ
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# الذاكرة
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# عرض المحادثة
# =========================
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="user-bubble">{message["text"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="bot-bubble">{message["text"]}</div>',
            unsafe_allow_html=True,
        )

# =========================
# الأدوات
# =========================
col_img, col_cam, col_text, col_send = st.columns([1, 1, 5.5, 1])

with col_img:
    uploaded_file = st.file_uploader(
        "🖼️",
        type=["jpg", "jpeg", "png", "webp"],
        key="file_picker",
        label_visibility="collapsed",
    )

with col_cam:
    camera_file = st.camera_input(
        "📷",
        key="camera_picker",
        label_visibility="collapsed",
    )

with col_text:
    user_text = st.text_input(
        "المراسلة",
        placeholder="المراسلة...",
        key="chat_input",
        label_visibility="collapsed",
    )

with col_send:
    send = st.button("➤", use_container_width=True)

# =========================
# إرسال الرسالة
# =========================
if send:

    text = user_text.strip()

    image = None

    try:
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")

        elif camera_file is not None:
            image = Image.open(camera_file).convert("RGB")

    except Exception:
        st.error("تعذر قراءة الصورة.")
        st.stop()

    if not text and image is None:
        st.warning("اكتب رسالة أو اختر صورة أولًا.")
        st.stop()

    # رسالة المستخدم
    display_text = text

    if image is not None and not text:
        display_text = "📷 أرسلت صورة"

    elif image is not None:
        display_text = f"{text} 📷"

    st.session_state.messages.append(
        {
            "role": "user",
            "text": display_text,
        }
    )

    # =========================
    # الرد الخاص
    # =========================
    normalized = text.lower()

    origin_words = [
        "من وين أنت",
        "من وين انت",
        "من اين انت",
        "من أين أنت",
        "من وين اصلك",
        "من وين أصلك",
        "أصلك",
        "اصلك",
        "وين اصلك",
        "وين أصلك",
    ]

    if any(word.lower() in normalized for word in origin_words):

        answer = "إلي الشرف من درعا ❤️"

    else:

        try:

            contents = []

            if text:
                contents.append(text)

            if image is not None:
                contents.append(image)

            if image is not None and not text:
                contents.insert(
                    0,
                    "اشرح لي هذه الصورة بالتفصيل وباللغة العربية."
                )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                ),
            )

            answer = response.text

            if not answer:
                answer = "ما قدرت أحصل على رد من Gemini."

        except Exception as e:

            answer = (
                "حدث خطأ أثناء الاتصال بخدمة الذكاء الاصطناعي.\n\n"
                f"تفاصيل الخطأ: {str(e)}"
            )

    # إضافة الرد
    st.session_state.messages.append(
        {
            "role": "assistant",
            "text": answer,
        }
    )

    # إعادة تشغيل الصفحة
    st.rerun()