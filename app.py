
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import io

st.set_page_config(
    page_title="TalkBridge",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 TalkBridge")
st.subheader("Speak naturally. Understand instantly.")
st.caption("A multilingual communication platform")

LANGUAGES = {
    "العربية": "ar",
    "English": "en",
    "Bahasa Indonesia": "id",
    "Français": "fr",
    "Español": "es",
    "Deutsch": "de",
    "中文": "zh-CN",
    "Türkçe": "tr"
}

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

source_lang = LANGUAGES[source_name]
target_lang = LANGUAGES[target_name]

if "source_text" not in st.session_state:
    st.session_state.source_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

st.markdown("### 🎙️ كلامك")

st.info(
    "يمكنك كتابة النص الآن. "
    "التسجيل الصوتي يحتاج إلى تشغيل الواجهة في بيئة "
    "تدعم الميكروفون."
)

st.session_state.source_text = st.text_area(
    "النص الأصلي",
    value=st.session_state.source_text,
    height=140,
    placeholder="اكتب ما تريد قوله هنا..."
)

if st.button("🌍 ترجمة النص", use_container_width=True):
    if not st.session_state.source_text.strip():
        st.warning("اكتب النص أولًا.")
    elif source_lang == target_lang:
        st.session_state.translated_text = (
            st.session_state.source_text
        )
    else:
        try:
            with st.spinner("جارٍ الترجمة..."):
                translator = GoogleTranslator(
                    source=source_lang,
                    target=target_lang
                )
                st.session_state.translated_text = (
                    translator.translate(
                        st.session_state.source_text
                    )
                )
        except Exception as error:
            st.error(
                "تعذرت الترجمة. تحقق من اتصال الإنترنت "
                "ثم حاول مرة أخرى."
            )

st.markdown("### 💬 الترجمة")

st.text_area(
    "النص المترجم",
    value=st.session_state.translated_text,
    height=140,
    disabled=True
)

if st.button("🔊 استمع إلى الترجمة", use_container_width=True):
    if not st.session_state.translated_text.strip():
        st.warning("ترجم النص أولًا.")
    else:
        try:
            with st.spinner("جارٍ تجهيز الصوت..."):
                audio_buffer = io.BytesIO()

                tts = gTTS(
                    text=st.session_state.translated_text,
                    lang=target_lang
                )
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

            st.audio(audio_buffer, format="audio/mp3")

        except Exception:
            st.error(
                "تعذر إنشاء الصوت لهذه اللغة حاليًا."
            )

st.divider()

st.caption(
    "TalkBridge Prototype | Meeting Room • Class Room • Tour Room"
)
st.caption(
    "ملاحظة: الترجمة والنطق يستخدمان خدمات خارجية عبر الإنترنت. "
    "لا تدخل معلومات سرية في هذه النسخة التجريبية."
)
