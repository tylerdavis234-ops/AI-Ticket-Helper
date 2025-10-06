import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with Streamlit secret
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page config
st.set_page_config(page_title="AI Ticket Helper", page_icon="🎫")
st.title("🎫 TeamDynamix Ticket Helper")
st.write("Enter basic info below — your AI assistant will format it for your ticket.")

# Initialize session state
if "ticket_generated" not in st.session_state:
    st.session_state.ticket_generated = False
    st.session_state.ticket_name = ""
    st.session_state.details = ""

# Ticket form
with st.form("ticket_form"):
    name = st.text_input("Name:")
    username = st.text_input("Username:")
    idnumber = st.text_input("JCCC ID Number:")
    roomnumber = st.text_input("Location:")
    issue = st.text_area("Describe the issue:")
    submitted = st.form_submit_button("Generate Ticket Summary")

# Generate ticket
if submitted:
    with st.spinner("Generating AI response..."):
        prompt = f"""
        You are TyBot, a professional IT helpdesk assistant.
        Using the information below, do the following:

        1. Generate a short, descriptive 'Ticket Name' (no personal names).
        2. Write a short paragraph summarizing the issue based on the description.

        Format like this:
        Ticket Name: <Generated Ticket Name>
        Details: <Summary paragraph>

        Name: {name}
        Username: {username}
        JCCC ID Number: {idnumber}
        Location: {roomnumber}
        Issue: {issue}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are TyBot, a friendly and professional IT assistant helping to write TeamDynamix tickets."},
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

        # Store in session
        st.session_state.ticket_generated = True
        st.session_state.ticket_name = ticket_name
        st.session_state.details = details

# Function to display fields with "highlight on focus"
def highlight_field(label, value, height=None, key=None):
    """Displays a text input or textarea that highlights all text when focused."""
    key = key or label.lower().replace(" ", "_")
    if height:
        st.text_area(label, value, height=height, key=key)
    else:
        st.text_input(label, value, key=key)

    # JS to highlight text when field is focused
    st.markdown(f"""
        <script>
        const input = window.parent.document.querySelector('[data-testid="{key}"] input, [data-testid="{key}"] textarea');
        if(input) {{
            input.addEventListener('focus', () => {{
                input.select();
            }});
        }}
        </script>
    """, unsafe_allow_html=True)

# Display generated ticket
if st.session_state.ticket_generated:
    st.subheader("✅ Ticket Generated")

    highlight_field("Ticket Name", st.session_state.ticket_name)
    highlight_field("Name", name)
    highlight_field("Username", username)
    highlight_field("JCCC ID", idnumber)
    highlight_field("Location", roomnumber)
    highlight_field("Details", st.session_state.details, height=150)
