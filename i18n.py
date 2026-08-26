# ============================================================
# AgriOne AI - Global Translation System
# ============================================================

import streamlit as st

LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
}

TRANSLATIONS = {
    "English": {
        "home": "Home",
        "chatbot": "AI Chatbot",
        "disease": "Disease Detection",
        "weather": "Weather",
        "soil": "Soil Analysis",
        "crop": "Crop Recommendation",
        "fertilizer": "Fertilizer Recommendation",
        "schemes": "Government Schemes",
        "market": "Market Information",
        "dashboard": "Dashboard",
        "language": "Language",
        "analyze": "Analyze",
        "processing": "Processing...",
        "clear": "Clear",
        "ask_question": "Ask your agriculture question",
        "type_message": "Type your message...",
        "upload_image": "Upload Crop Image",
        "upload_pdf": "Upload PDF",
        "try_again": "Please try again.",
    },
    "Telugu": {
        "home": "హోమ్",
        "chatbot": "AI చాట్‌బాట్",
        "disease": "పంట వ్యాధి గుర్తింపు",
        "weather": "వాతావరణం",
        "soil": "నేల విశ్లేషణ",
        "crop": "పంట సిఫార్సు",
        "fertilizer": "ఎరువుల సిఫార్సు",
        "schemes": "ప్రభుత్వ పథకాలు",
        "market": "మార్కెట్ సమాచారం",
        "dashboard": "డ్యాష్‌బోర్డ్",
        "language": "భాష",
        "analyze": "విశ్లేషించండి",
        "processing": "ప్రాసెస్ చేస్తోంది...",
        "clear": "క్లియర్",
        "ask_question": "మీ వ్యవసాయ ప్రశ్న అడగండి",
        "type_message": "మీ సందేశాన్ని టైప్ చేయండి...",
        "upload_image": "పంట చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "upload_pdf": "PDF అప్‌లోడ్ చేయండి",
        "try_again": "దయచేసి మళ్లీ ప్రయత్నించండి.",
    },
    "Hindi": {
        "home": "होम",
        "chatbot": "AI चैटबॉट",
        "disease": "फसल रोग पहचान",
        "weather": "मौसम",
        "soil": "मिट्टी विश्लेषण",
        "crop": "फसल सुझाव",
        "fertilizer": "उर्वरक सुझाव",
        "schemes": "सरकारी योजनाएँ",
        "market": "बाज़ार जानकारी",
        "dashboard": "डैशबोर्ड",
        "language": "भाषा",
        "analyze": "विश्लेषण करें",
        "processing": "प्रोसेस हो रहा है...",
        "clear": "साफ़ करें",
        "ask_question": "अपना कृषि प्रश्न पूछें",
        "type_message": "अपना संदेश लिखें...",
        "upload_image": "फसल की तस्वीर अपलोड करें",
        "upload_pdf": "PDF अपलोड करें",
        "try_again": "कृपया फिर प्रयास करें।",
    },
    "Tamil": {
        "home": "முகப்பு",
        "chatbot": "AI சாட்பாட்",
        "disease": "பயிர் நோய் கண்டறிதல்",
        "weather": "வானிலை",
        "soil": "மண் பகுப்பாய்வு",
        "crop": "பயிர் பரிந்துரை",
        "fertilizer": "உர பரிந்துரை",
        "schemes": "அரசு திட்டங்கள்",
        "market": "சந்தை தகவல்",
        "dashboard": "டாஷ்போர்டு",
        "language": "மொழி",
        "analyze": "பகுப்பாய்வு",
        "processing": "செயலாக்கப்படுகிறது...",
        "clear": "அழி",
        "ask_question": "உங்கள் விவசாய கேள்வியை கேளுங்கள்",
        "type_message": "உங்கள் செய்தியை உள்ளிடுங்கள்...",
        "upload_image": "பயிர் படத்தை பதிவேற்றவும்",
        "upload_pdf": "PDF பதிவேற்றவும்",
        "try_again": "மீண்டும் முயற்சிக்கவும்.",
    },
}

def get_language():
    return st.session_state.get(
        "language",
        "English"
    )

def t(key, default=None, language=None):
    language = language or get_language()
    return TRANSLATIONS.get(
        language,
        TRANSLATIONS["English"]
    ).get(
        key,
        default if default is not None else key
    )
