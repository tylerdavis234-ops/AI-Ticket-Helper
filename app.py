import streamlit as st
from openai import OpenAI
import re
import json

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ticketchimp",
    page_icon="🐵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS FOR DARK TECH UI & ANIMATIONS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700&display=swap');

body {
    background-color: #0E1117;
    color: #E4E6EB;
    font-family: 'Segoe UI', sans-serif;
    text-align: center;
}

/* Centered main container */
.main-box {
    max-width: 650px;
    margin: 40px auto 60px auto;
    background-color: #1A1D23;
    padding: 30px;
    border-radius: 15px;
    border: 1px solid #3A3F47;
    text-align: center;
}

/* Wacky Ticketchimp font */
.header-text {
    font-family: 'Baloo 2', cursive;
    font-size: 60px;
    vertical-align: middle;
}

/* Single animated monkey */
@keyframes jiggle {
    0% { transform: rotate(0deg) translateY(0); }
    25% { transform: rotate(10deg) translateY(-5px); }
    50% { transform: rotate(-10deg) translateY(5px); }
    75% { transform: rotate(10deg) translateY(-5px); }
    100% { transform: rotate(0deg) translateY(0); }
}
.monkey {
    font-size: 80px;
    display: inline-block;
    animation: jiggle 1s infinite;
    vertical-align: middle;
    margin-right: 15px;
}

/* Input field styling */
.stTextArea textarea, .stTextInput input {
    background-color: #0E1117 !important;
    color: #E4E6EB !important;
    border: 1px solid #3A3F47 !important;
    border-radius: 8px !important;
    width: 100%;
}

/* Banana button */
.stButton>button {
    display: block;
    margin: 25px auto;
    background: linear-gradient(90deg, #FFB200, #FFD700);
    color: #1A1D23;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease-in-out;
    font-size: 18px;
    padding: 10px 25px;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #FFD700, #FFB200);
    transform: scale(1.1);
}

/* Ticket output styling - stacked */
.ticket-box {
    background-color: #1A1D23;
    border: 1px solid #3A3F47;
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
    animation: fadein 0.6s;
    text-align: center;
}
.ticket-field {
    margin-bottom: 15px;
}
.ticket-field b {
    color: #00C6FF;
}

/* Fade-in */
@keyframes fadein {
    0% { opacity: 0; transform: translateY(10px);}
    100% { opacity: 1; transform: translateY(0);}
}

/* Subheader */
.sub {
    color: #B0B3B8;
    font-size: 18px;
    margin-top: -10px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div><span class='monkey'>🙉</span><span class='header-text'>Ticketchimp</span></div>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Your reliable ticket companion for IT requests</p>", unsafe_allow_html=True)

# --- OPENAI CLIENT ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ Please set your OpenAI API key in .streamlit/secrets.toml (local) or App Secrets (Streamlit Cloud).")
    st.stop()

client = OpenAI(api_key=api_key)

# --- CENTERED TICKET FORM ---
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    # Ticket description at top
    ticket_description = st.text_area(
        "📝 Ticket Description",
        height=150,
        placeholder="Type the issue here as you would on the phone..."
    )

    if st.button("🍌 Generate"):
        if not ticket_description.strip():
            st.warning("Please enter a ticket description first.")
        else:
            with st.spinner("Generating ticket..."):
                try:
                    prompt = f"""
                    You are an IT ticket assistant named Ticketchimp.
                    Based on the following description, generate:

                    1. Ticket Name (short, descriptive, no personal info)
                    2. Username (from description if mentioned)
                    3. Location (detect RC257 or CLB165, otherwise leave blank)
                    4. A concise AI-generated summary of the issue

                    Ticket Description: {ticket_description}

                    Format as JSON like this:
                    {{
                        "ticket_name": "<Ticket Name>",
                        "username": "<Username>",
                        "location": "<Location>",
                        "description": "<Summary>"
                    }}
                    """

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are Ticketchimp, a friendly and efficient IT ticket assistant."},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    content = response.choices[0].message.content.strip()

                    # Parse JSON
                    try:
                        ticket_data = json.loads(content)
                    except:
                        ticket_data = {}
                        ticket_data["ticket_name"] = re.search(r'"ticket_name":\s*"(.+?)"', content).group(1) if "ticket_name" in content else ""
                        ticket_data["username"] = re.search(r'"username":\s*"(.+?)"', content).group(1) if "username" in content else ""
                        ticket_data["location"] = re.search(r'"location":\s*"(.+?)"', content).group(1) if "location" in content else ""
                        ticket_data["description"] = re.search(r'"description":\s*"(.+?)"', content).group(1) if "description" in content else content

                    # --- DISPLAY TICKET STACKED ---
                    st.markdown("### 🗂️ Generated Ticket")
                    st.markdown(f"""
                    <div class='ticket-box'>
                        <div class='ticket-field'><b>Ticket Name:</b><br>{ticket_data.get('ticket_name', '')}</div>
                        <div class='ticket-field'><b>Username:</b><br>{ticket_data.get('username', '')}</div>
                        <div class='ticket-field'><b>Location:</b><br>{ticket_data.get('location', '')}</div>
                        <div class='ticket-field'><b>Description:</b><br>{ticket_data.get('description', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"⚠️ Error generating ticket: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<hr style="border: 1px solid #333;">
<p style="text-align: center; color: #555;">
🚀 Powered by OpenAI | Designed by Tyler Davis
</p>
""", unsafe_allow_html=True)
