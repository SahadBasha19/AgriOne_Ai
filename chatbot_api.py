import os
import io
import tempfile
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
except ImportError:
    genai = None


LANGUAGE_SETTINGS = {
    "English": {"speech": "en-IN", "tts": "en"},
    "Telugu": {"speech": "te-IN", "tts": "te"},
    "Hindi": {"speech": "hi-IN", "tts": "hi"},
    "Tamil": {"speech": "ta-IN", "tts": "ta"},
}


def get_current_language():
    return st.session_state.get("language", "English")


def _settings(language=None):
    return LANGUAGE_SETTINGS.get(
        language or get_current_language(),
        LANGUAGE_SETTINGS["English"]
    )


@st.cache_resource
def get_gemini_client():
    if genai is None:
        return None

    api_key = ""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def language_instruction(language):
    instructions = {
        "English": "Answer in simple English.",
        "Telugu": "Answer completely in simple Telugu.",
        "Hindi": "Answer completely in simple Hindi.",
        "Tamil": "Answer completely in simple Tamil.",
    }
    return instructions.get(language, instructions["English"])


def chatbot_response(question, language=None, conversation_history=None):
    language = language or get_current_language()
    question = str(question or "").strip()

    if not question:
        return {"success": False, "response": "", "error": "Please ask a question."}

    client = get_gemini_client()
    if client is None:
        return {
            "success": False,
            "response": "",
            "error": "Gemini API key is not configured. Add GEMINI_API_KEY to Streamlit secrets or environment variables."
        }

    history_text = ""
    for item in (conversation_history or [])[-6:]:
        role = item.get("role", "user")
        text = item.get("text", item.get("content", ""))
        if text:
            history_text += f"{role}: {text}\n"

    prompt = f"""You are AgriOne AI, an intelligent agriculture assistant.

{language_instruction(language)}
Give practical, safe, and easy-to-understand answers for farmers.
Keep answers concise unless the user asks for details.

Conversation history:
{history_text}

User question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = (getattr(response, "text", "") or "").strip()

        if not answer:
            return {
                "success": False,
                "response": "",
                "error": "Gemini returned an empty response. Please try again."
            }

        return {"success": True, "response": answer, "error": None}

    except Exception as error:
        return {"success": False, "response": "", "error": f"Gemini error: {error}"}


def voice_to_text(audio_data, language=None):
    if audio_data is None:
        return {"success": False, "text": "", "error": "No voice recording found."}

    try:
        import speech_recognition as sr
    except ImportError:
        return {
            "success": False,
            "text": "",
            "error": "SpeechRecognition package is missing. Run: pip install -r requirements.txt"
        }

    temporary_path = None
    try:
        if hasattr(audio_data, "getvalue"):
            audio_bytes = audio_data.getvalue()
        elif isinstance(audio_data, bytes):
            audio_bytes = audio_data
        else:
            audio_bytes = audio_data.read()

        if not audio_bytes:
            return {"success": False, "text": "", "error": "Recorded audio is empty."}

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_bytes)
            temporary_path = temp_file.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(temporary_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language=_settings(language)["speech"]
        )

        return {"success": True, "text": text, "error": None}

    except sr.UnknownValueError:
        return {"success": False, "text": "", "error": "Could not understand the voice. Please record again."}
    except sr.RequestError as error:
        return {"success": False, "text": "", "error": f"Speech recognition service error: {error}"}
    except Exception as error:
        return {"success": False, "text": "", "error": f"Voice input error: {error}"}
    finally:
        if temporary_path and os.path.exists(temporary_path):
            try:
                os.remove(temporary_path)
            except OSError:
                pass


def voice_output(text, language=None):
    text = str(text or "").strip()
    if not text:
        return {"success": False, "audio": None, "error": "No text available for voice output."}

    try:
        from gtts import gTTS

        audio_buffer = io.BytesIO()
        tts = gTTS(
            text=text,
            lang=_settings(language)["tts"],
            slow=False
        )
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return {"success": True, "audio": audio_buffer.getvalue(), "error": None}

    except Exception as error:
        return {
            "success": False,
            "audio": None,
            "error": f"Voice output is unavailable: {error}"
        }


def voice_to_voice(audio_data, language=None, conversation_history=None):
    language = language or get_current_language()

    speech_result = voice_to_text(audio_data, language)
    if not speech_result["success"]:
        return {"success": False, "error": speech_result["error"]}

    question = speech_result["text"]

    ai_result = chatbot_response(
        question=question,
        language=language,
        conversation_history=conversation_history
    )
    if not ai_result["success"]:
        return {"success": False, "error": ai_result["error"]}

    tts_result = voice_output(ai_result["response"], language)

    return {
        "success": True,
        "question": question,
        "response": ai_result["response"],
        "audio": tts_result.get("audio"),
        "audio_error": tts_result.get("error"),
        "error": None
    }