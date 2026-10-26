
import io
import streamlit as st
from google import genai
from gtts import gTTS

st.set_page_config(
    page_title="TalkBridge",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 TalkBridge")
st.subheader("Speak naturally. Understand instantly.")
st.caption("A multilingual communication platform")

LANGUAGES = {
    "العربية": "Arabic",
    "English": "English",
    "Bahasa Indonesia": "Indonesian",
    "Français": "French",
    "Español": "Spanish",
    "Deutsch": "German",
    "中文": "Chinese (Simplified)",
    "Türkçe": "Turkish",
}

# Keep the API key in Streamlit Secrets, never in this file.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = None

st.divider()

col1, col2 = st.columns(2)

with col1:
    source_name = st.selectbox(
        "لغة المتحدث",
        list(LANGUAGES.keys()),
        index=0
    )

with col2:
    target_name = st.selectbox(
        "لغة الترجمة",
        list(LANGUAGES.keys()),
        index=1
    )

st.markdown("### 🎙️ كلامك")
st.info(
    "اكتب النص الذي تريد ترجمته. "
    "التسجيل الصوتي المباشر سيُضاف في مرحلة لاحقة."
)

source_text = st.text_area(
    "النص الأصلي",
    height=140,
    placeholder="اكتب ما تريد قوله هنا...",
    key="source_text"
)

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if st.button("🌍 ترجمة النص", use_container_width=True):
    text = source_text.strip()

    if not text:
        st.warning("اكتب النص أولًا.")

    elif source_name == target_name:
        st.session_state.translated_text = text
        st.success("تم نسخ النص؛ اللغتان متطابقتان.")

    elif not api_key:
        st.error(
            "مفتاح Gemini غير موجود. "
            "راجع إعدادات Secrets في Streamlit."
        )

    else:
        try:
            with st.spinner("Gemini يترجم النص..."):
                client = genai.Client(api_key=api_key)

                prompt = f"""
You are a professional translator.
Translate the text from {LANGUAGES[source_name]}
into {LANGUAGES[target_name]}.

Rules:
- Preserve the original meaning and tone.
- Use natural, fluent language.
- Return only the translated text.
- Do not add explanations or quotation marks.

Text to translate:
{text}
"""

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                result = (response.text or "").strip()

                if not result:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                st.session_state.translated_text = result
                st.success("تمت الترجمة بنجاح.")

        except Exception as error:
            st.error("تعذرت الترجمة باستخدام Gemini.")
            with st.expander("تفاصيل الخطأ"):
                st.code(
                    f"{type(error).__name__}: {error}"
                )

st.markdown("### 💬 الترجمة")

st.text_area(
    "النص المترجم",
    value=st.session_state.translated_text,
    height=140,
    disabled=True
)

if st.button(
    "🔊 استمع إلى الترجمة",
    use_container_width=True
):
    translated = st.session_state.translated_text.strip()

    if not translated:
        st.warning("ترجم النص أولًا.")

    else:
        try:
            with st.spinner("جارٍ تجهيز الصوت..."):
                audio_buffer = io.BytesIO()

                # gTTS uses language codes, unlike Gemini.
                tts_codes = {
                    "العربية": "ar",
                    "English": "en",
                    "Bahasa Indonesia": "id",
                    "Français": "fr",
                    "Español": "es",
                    "Deutsch": "de",
                    "中文": "zh-CN",
                    "Türkçe": "tr",
                }

                tts = gTTS(
                    text=translated,
                    lang=tts_codes[target_name]
                )

                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

            st.audio(audio_buffer, format="audio/mp3")

        except Exception as error:
            st.error("تعذر إنشاء الصوت.")
            with st.expander("تفاصيل خطأ الصوت"):
                st.code(
                    f"{type(error).__name__}: {error}"
                )

st.divider()

st.caption(
    "TalkBridge Prototype | Meeting Room • Class Room • Tour Room"
)
st.caption(
    "الترجمة تستخدم Gemini API، والصوت يستخدم gTTS. "
    "قد تتم معالجة النصوص بواسطة خدمات خارجية؛ "
    "تجنب إدخال المعلومات السرية."
)
