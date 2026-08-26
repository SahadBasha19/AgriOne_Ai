import os
import importlib
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgriOne AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


# ============================================================
# LOAD CSS
# ============================================================

css_path = os.path.join(BASE_DIR, "style.css")

if os.path.exists(css_path):
    try:
        with open(css_path, "r", encoding="utf-8") as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )
    except Exception:
        pass


# ============================================================
# SESSION STATE
# ============================================================

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "🏠 Home"

if "language" not in st.session_state:
    st.session_state.language = "English"


# ============================================================
# LANGUAGES
# ============================================================

LANGUAGES = [
    "English",
    "Telugu",
    "Hindi",
    "Tamil"
]


# ============================================================
# PAGE ROUTES
# ============================================================

PAGE_ROUTES = {
    "🏠 Home": None,
    "🤖 AI Chatbot": "views.chatbot",
    "🌿 Disease Detection": "views.disease",
    "🌦️ Weather": "views.weather",
    "🌱 Soil Analysis": "views.soil",
    "🌾 Crop Recommendation": "views.crop",
    "🧪 Fertilizer Recommendation": "views.fertilizer",
    "🏛️ Government Schemes": "views.schemes",
    "📈 Market Information": "views.market",
    "📊 Dashboard": "views.dashboard"
}


# ============================================================
# NAVIGATION FUNCTION
# ============================================================

def go_to_page(page_name):
    st.session_state.selected_page = page_name
    st.rerun()


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    language = st.session_state.language

    content = {
        "English": {
            "title": "Smart Farming with AI",
            "description": (
                "Your intelligent agriculture assistant for crops, soil, "
                "weather, disease detection, fertilizer recommendations "
                "and market information."
            )
        },

        "Telugu": {
            "title": "AI తో స్మార్ట్ వ్యవసాయం",
            "description": (
                "పంటలు, నేల, వాతావరణం, వ్యాధులు మరియు మార్కెట్ సమాచారం కోసం "
                "మీ డిజిటల్ వ్యవసాయ సహాయకుడు."
            )
        },

        "Hindi": {
            "title": "AI के साथ स्मार्ट खेती",
            "description": (
                "फसल, मिट्टी, मौसम, रोग और बाजार की जानकारी के लिए "
                "आपका स्मार्ट कृषि सहायक।"
            )
        },

        "Tamil": {
            "title": "AI உடன் ஸ்மார்ட் விவசாயம்",
            "description": (
                "பயிர்கள், மண், வானிலை, நோய்கள் மற்றும் சந்தை தகவலுக்கான "
                "உங்கள் டிஜிட்டல் விவசாய உதவியாளர்."
            )
        }
    }

    current = content.get(
        language,
        content["English"]
    )


    # ========================================================
    # HERO
    # ========================================================

    st.title("🌱 AgriOne AI")

    st.subheader(current["title"])

    st.write(current["description"])

    st.info(
        "✨ AI-Powered Agriculture Platform   •   "
        "🤖 Smart Assistant   •   "
        "🎤 Voice Support   •   "
        "🌐 4 Languages"
    )


    # ========================================================
    # QUICK START
    # ========================================================

    st.subheader("🚀 Quick Start")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🤖 Ask AI", use_container_width=True):
            go_to_page("🤖 AI Chatbot")

    with col2:
        if st.button("🌿 Detect Disease", use_container_width=True):
            go_to_page("🌿 Disease Detection")

    with col3:
        if st.button("🌦️ Weather", use_container_width=True):
            go_to_page("🌦️ Weather")

    with col4:
        if st.button("📈 Market", use_container_width=True):
            go_to_page("📈 Market Information")


    st.divider()


    # ========================================================
    # FEATURES
    # ========================================================

    st.subheader("🌾 Smart Agriculture Features")

    features = [

        (
            "🤖",
            "AI Farmer Assistant",
            "Ask agriculture questions and get AI-powered answers.",
            "🤖 AI Chatbot"
        ),

        (
            "🌿",
            "Disease Detection",
            "Upload a crop image and analyze possible plant diseases.",
            "🌿 Disease Detection"
        ),

        (
            "🌦️",
            "Weather Intelligence",
            "Check weather information for better farm planning.",
            "🌦️ Weather"
        ),

        (
            "🌱",
            "Soil Analysis",
            "Analyze soil information and understand soil health.",
            "🌱 Soil Analysis"
        ),

        (
            "🌾",
            "Crop Recommendation",
            "Get crop recommendations based on agricultural data.",
            "🌾 Crop Recommendation"
        ),

        (
            "🧪",
            "Fertilizer Recommendation",
            "Get fertilizer recommendations for crop growth.",
            "🧪 Fertilizer Recommendation"
        ),

        (
            "🏛️",
            "Government Schemes",
            "Explore agriculture schemes and farmer support information.",
            "🏛️ Government Schemes"
        ),

        (
            "📈",
            "Market Information",
            "View crop market information and available prices.",
            "📈 Market Information"
        ),

        (
            "📊",
            "Smart Dashboard",
            "Explore agriculture data, charts and analytics.",
            "📊 Dashboard"
        )
    ]


    # ========================================================
    # FEATURE GRID
    # ========================================================

    for row in range(0, len(features), 3):

        cols = st.columns(3)

        for col, feature in zip(
            cols,
            features[row:row + 3]
        ):

            icon = feature[0]
            title = feature[1]
            description = feature[2]
            page = feature[3]

            with col:

                with st.container(border=True):

                    st.subheader(
                        f"{icon} {title}"
                    )

                    st.write(description)

                    if st.button(
                        "Open Feature",
                        key=f"feature_{page}",
                        use_container_width=True
                    ):
                        go_to_page(page)


    st.divider()


    # ========================================================
    # HIGHLIGHTS
    # ========================================================

    st.subheader("⚡ AgriOne AI Highlights")

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Languages",
            "4+"
        )

    with b:
        st.metric(
            "Smart Tools",
            "9"
        )

    with c:
        st.metric(
            "AI Support",
            "24/7"
        )

    with d:
        st.metric(
            "Voice Support",
            "Available"
        )


    st.divider()


    # ========================================================
    # HOW IT WORKS
    # ========================================================

    st.subheader("🔄 How It Works")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.success("1️⃣ Choose")
        st.caption("Select the farming tool you need.")

    with s2:
        st.success("2️⃣ Enter")
        st.caption("Provide your farming information.")

    with s3:
        st.success("3️⃣ Analyze")
        st.caption("AI or ML processes your information.")

    with s4:
        st.success("4️⃣ Get Results")
        st.caption("Receive insights and recommendations.")


    st.divider()


    # ========================================================
    # SMART FARMING TIPS
    # ========================================================

    st.subheader("💡 Smart Farming Tips")

    tip1, tip2, tip3 = st.columns(3)

    with tip1:
        with st.container(border=True):
            st.subheader("🌦️ Check Weather")
            st.caption(
                "Check weather before planning irrigation."
            )

    with tip2:
        with st.container(border=True):
            st.subheader("🌿 Monitor Crops")
            st.caption(
                "Inspect crops regularly for disease symptoms."
            )

    with tip3:
        with st.container(border=True):
            st.subheader("📈 Watch Markets")
            st.caption(
                "Check market information before selling crops."
            )


    st.divider()

    st.success(
        "🌱 AgriOne AI brings AI, machine learning "
        "and agriculture together in one platform."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌱 AgriOne AI")

    st.caption("Smart Agriculture Assistant")

    st.divider()

    st.subheader("🧭 Navigation")

    page_names = list(PAGE_ROUTES.keys())

    if st.session_state.selected_page not in page_names:
        st.session_state.selected_page = "🏠 Home"

    current_index = page_names.index(
        st.session_state.selected_page
    )

    selected_page = st.radio(
        "Navigation",
        page_names,
        index=current_index,
        label_visibility="collapsed"
    )

    if selected_page != st.session_state.selected_page:

        st.session_state.selected_page = selected_page

        st.rerun()


    st.divider()


    selected_language = st.selectbox(
        "🌐 Select Language",
        LANGUAGES,
        index=LANGUAGES.index(
            st.session_state.language
        )
    )

    if selected_language != st.session_state.language:

        st.session_state.language = selected_language

        st.session_state.current_language = selected_language

        st.rerun()


    st.divider()

    st.caption(
        f"🌐 Language: {st.session_state.language}"
    )

    st.caption(
        "🌱 Smart Agriculture Platform"
    )


# ============================================================
# PAGE ROUTER
# NORMAL PAGE LOADING - NO LAZY LOADER
# ============================================================

module_name = PAGE_ROUTES.get(
    st.session_state.selected_page
)


if module_name is None:

    home_page()


else:

    try:

        # Normal direct page loading
        module = importlib.import_module(
            module_name
        )

        page_function = getattr(
            module,
            "app",
            None
        )

        if callable(page_function):

            page_function()

        else:

            st.warning(
                "⚠️ This page does not contain an app() function."
            )


    except ModuleNotFoundError:

        st.warning(
            "⚠️ Required file or package is missing."
        )


    except ImportError:

        st.warning(
            "⚠️ Required dependency is missing."
        )


    except Exception:

        st.warning(
            "⚠️ Unable to open this feature right now."
        )

        if st.button(
            "🏠 Return to Home"
        ):
            go_to_page(
                "🏠 Home"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌱 AgriOne AI • Smart Agriculture Assistant • "
    "Powered by AI & Machine Learning"
)