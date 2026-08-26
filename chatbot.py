import streamlit as st

try:
    from utils.i18n import t, get_language
except Exception:
    def get_language():
        return st.session_state.get("language", "English")

    def t(key, default=None):
        return default or key

from utils.chatbot_api import (
    chatbot_response,
    voice_to_text,
    voice_to_voice,
    voice_output,
)


def current_language():
    return get_language()


def build_history(messages):
    return [
        {
            "role": item.get("role", "user"),
            "text": item.get("content", "")
        }
        for item in messages[-8:]
    ]


def add_answer(question, result, language):
    if not result.get("success"):
        return False, result.get("error", "Please try again.")

    answer = result.get("response", "").strip()
    if not answer:
        return False, "AI returned an empty response."

    tts_result = voice_output(answer, language)

    st.session_state.chat_messages.append({
        "role": "user",
        "content": question,
    })
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": answer,
        "audio": tts_result.get("audio"),
        "audio_error": tts_result.get("error"),
    })

    return True, None


def app():
    language = current_language()

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "voice_question" not in st.session_state:
        st.session_state.voice_question = ""

    st.markdown("""
    <div class="badge-pill">🤖 AI AGRICULTURE ASSISTANT</div>
    <div class="hero-title">AI Chatbot</div>
    <div class="hero-subtitle">Ask your agriculture question</div>
    """, unsafe_allow_html=True)

    left, right = st.columns([3, 1])
    with left:
        st.markdown("### 💬 Ask your agriculture question")
    with right:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.voice_question = ""
            st.rerun()

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message.get("content", ""))
            if message.get("audio"):
                st.audio(message["audio"], format="audio/mp3")
            elif message.get("audio_error"):
                st.caption(f"🔇 {message['audio_error']}")

    # TEXT -> AI -> VOICE
    text_question = st.chat_input("Type your agriculture question...")

    if text_question and text_question.strip():
        question = text_question.strip()
        with st.spinner("🤖 AgriOne AI is thinking..."):
            result = chatbot_response(
                question=question,
                language=language,
                conversation_history=build_history(st.session_state.chat_messages),
            )

        ok, error = add_answer(question, result, language)
        if not ok:
            st.error(error)
        else:
            st.rerun()

    st.divider()
    st.markdown("## 🎙️ Voice Assistant")
    st.caption(f"🌐 Current language: {language}")

    voice_col1, voice_col2 = st.columns(2)

    # VOICE -> TEXT -> AI -> VOICE
    with voice_col1:
        st.markdown("#### 🎤 Voice Input")
        audio_recording = st.audio_input(
            "Record your farming question",
            key="agri_voice_input",
        )

        if audio_recording is not None:
            st.audio(audio_recording)

            if st.button("🎧 Convert Voice to Text", use_container_width=True):
                with st.spinner("Listening..."):
                    speech_result = voice_to_text(
                        audio_data=audio_recording,
                        language=language,
                    )

                if speech_result.get("success"):
                    st.session_state.voice_question = speech_result["text"]
                    st.success(f"🗣️ You said: {speech_result['text']}")
                else:
                    st.error(speech_result.get("error", "Voice input failed."))

        if st.session_state.voice_question:
            st.markdown(f"**🗣️ Question:** {st.session_state.voice_question}")

            if st.button("🤖 Ask AI", key="ask_from_voice", use_container_width=True):
                question = st.session_state.voice_question
                with st.spinner("Generating AI answer and voice..."):
                    result = chatbot_response(
                        question=question,
                        language=language,
                        conversation_history=build_history(st.session_state.chat_messages),
                    )

                ok, error = add_answer(question, result, language)
                if not ok:
                    st.error(error)
                else:
                    st.session_state.voice_question = ""
                    st.rerun()

    # ONE CLICK VOICE -> AI -> VOICE
    with voice_col2:
        st.markdown("#### 🔊 Voice → Voice")
        voice_audio = st.audio_input(
            "Record and get a spoken AI answer",
            key="voice_to_voice_input",
        )

        if voice_audio is not None:
            st.audio(voice_audio)

            if st.button("🚀 Ask AgriOne AI", key="voice_to_voice_button", use_container_width=True):
                with st.spinner("🎧 Listening, thinking, and creating voice..."):
                    result = voice_to_voice(
                        audio_data=voice_audio,
                        language=language,
                        conversation_history=build_history(st.session_state.chat_messages),
                    )

                if result.get("success"):
                    question = result.get("question", "")
                    answer = result.get("response", "")
                    audio = result.get("audio")

                    st.session_state.chat_messages.append({
                        "role": "user",
                        "content": question,
                    })
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": answer,
                        "audio": audio,
                        "audio_error": result.get("audio_error"),
                    })

                    if result.get("audio_error"):
                        st.warning(result["audio_error"])

                    st.rerun()
                else:
                    st.error(result.get("error", "Voice conversation failed."))


if __name__ == "__main__":
    app()