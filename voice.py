import speech_recognition as sr
from gtts import gTTS
import tempfile

LANGUAGE_CODES = {
    "English": ("en-IN", "en"),
    "Telugu": ("te-IN", "te"),
    "Hindi": ("hi-IN", "hi"),
    "Tamil": ("ta-IN", "ta")
}


def voice_to_text(language):

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source, timeout=5)

            text = recognizer.recognize_google(
                audio,
                language=LANGUAGE_CODES[language][0]
            )

            return text

    except Exception:

        return ""


def text_to_voice(text, language):

    try:

        tts = gTTS(
            text=text,
            lang=LANGUAGE_CODES[language][1]
        )

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp.name)

        return temp.name

    except Exception:

        return None