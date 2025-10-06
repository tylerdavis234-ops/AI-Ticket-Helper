import streamlit as st
from openai import OpenAI
from streamlit_extras.let_it_rain import rain
from time import sleep

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(
    page_title="AI TicketMate",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# STYLING
# ========================
st.markdown("""
    <style>
    /* General Background */
    .main {
        background: linear-gradient(135deg, #0A0F24 0%, #141B3A 100%);
        color: #E0E6F8;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141B3A 0%, #0A0F24 100%);
        color: #FFFFFF;
    }

    /* Headers */
    h1, h2, h3 {
        color: #00FFC6;
        text-shadow: 0 0 15px #00FFC6;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #00FFC6;
        color: black;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #14A76C;
        color: white;
        transform: scale(1.05);
        box-shadow: 0 0 15px #00FFC6;
    }

    /* Inputs */
    div[data-baseweb="input"] > div {
        background-color: #1A1F38;
        color: white;
        border-radius: 6px;
    }

    textarea {
        background-color: #1A1F38 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
    }

    /* Footer */
    footer {visibility: hidden;}

    /* Neon title effect */
    .glow {
        color: #00FFC6;
        text-shadow: 0 0 15px #00FFC6, 0 0 30px #00FFC6;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ========================
# HEADER
# ========================
st.markdown("<h1 class='glow'>🤖 Welcome to AI TicketMate</h1>", unsafe_allow_html=True)
st.markdown("### Streamlined Tech Support — Powered by AI ⚡")

# Cool animation effect
rain(
    emoji="💾",
    font_size=30,
    falling_speed=5,
    animation_length="infinite"
)

# ========================
# SIDEBAR
# ========================
st.sidebar.header("⚙️ Settings")
dark_mode = st.sidebar.toggle("Enable Dark Mode", value=True)
show_debug = st.sidebar.toggle("Show Debug Logs", value=False)
st.sidebar.markdown("---")
st.sidebar.write("**Developed by Tyler Davis 🧠**")
st.sidebar.write("Version 1.2.0 | AI-Powered Support Tool")

# ========================
# OPENAI CLIENT
# ========================
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("⚠️ OpenAI API key not found in secrets.toml!")
    st.stop()

# ========================
# MAIN APP CONTENT
# ========================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### 💬 Describe the issue you're facing:")
    user_input = st.text_area(
        " ",
        placeholder="Example: Outlook not syncing or Teams mic not working..."
    )

    if st.button("🚀 Diagnose Issue"):
        if user_input.strip():
            with st.spinner("Analyzing your issue with AI..."):
                try:
                    sleep(1)

                    # Build prompt
                    prompt = f"""
                    You are TicketMate, a professional IT Helpdesk assistant.
                    Based on the issue description below, generate:
                    1. A short, clear 'Ticket Name'
                    2. A detailed summary paragraph of the issue in a professional tone.

                    Format:
                    Ticket Name: <name>
                    Details: <summary paragraph>

                    Issue: {user_input}
                    """

                    # OpenAI call
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are TicketMate, an expert IT Helpdesk AI that generates professional ticket summaries."
                            },
                            {"role": "user", "content": prompt}
                        ]
                    )

                    ticket_text = response.choices[0].message.content

                    # Parse output
                    lines = ticket_text.splitlines()
                    ticket_name, details = "", ""
                    for line in lines:
                        if line.lower().startswith("ticket name:"):
                            ticket_name = line.replace("Ticket Name:", "").strip()
                        elif line.lower().startswith("details:"):
                            details = line.replace("Details:", "").strip()

                    st.success("✅ Ticket Generated Successfully!")

                    # Display in styled boxes
                    st.markdown(f"""
                        <div style="background-color:#141B3A; padding:1em; border-radius:10px; margin-top:1em;">
                        <h4 style="color:#00FFC6;">🎟️ Ticket Name:</h4>
                        <p style="font-size:18px; color:white;">{ticket_name}</p>
                        <h4 style="color:#00FFC6;">📋 Details:</h4>
                        <p style="font-size:16px; color:white;">{details}</p>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error("❌ Error communicating with OpenAI API.")
                    if show_debug:
                        st.exception(e)
        else:
            st.warning("⚠️ Please describe an issue before submitting.")

with col2:
    st.markdown("#### 📂 Quick Actions")
    st.button("📘 Open Knowledge Base")
    st.button("✉️ Generate Email Template")
    st.button("🖥️ System Status Check")

# ========================
# FOOTER
# ========================
st.markdown("---")
st.caption("Built with ❤️ by Tyler Davis | AI TicketMate 2025")
