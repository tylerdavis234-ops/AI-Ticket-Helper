import streamlit as st
from openai import OpenAI
import pyperclip

# Initialize OpenAI client with Streamlit secret
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Ticket Helper", page_icon="🎫")
st.title("🎫 TeamDynamix Ticket Helper")
st.write("Enter basic info below — your AI assistant will format it for your ticket.")

# Initialize session state to store AI results
if "ticket_generated" not in st.session_state:
    st.session_state.ticket_generated = False
    st.session_state.ticket_name = ""
    st.session_state.details = ""

with st.form("ticket_form"):
    name = st.text_input("Name:")
    username = st.text_input("Username:")
    idnumber = st.text_input("JCCC ID Number:")
    roomnumber = st.text_input("Location:")
    issue = st.text_area("Describe the issue:")
    submitted = st.form_submit_button("Generate Ticket Summary")

if submitted:
    with st.spinner("Generating AI response..."):
        prompt = f"""
        You are TyBot, a professional IT helpdesk assistant.
        Using the information below, do the following:

        1. Generate a short, descriptive 'Ticket Name' for this issue (do NOT include the user's name).
        2. Generate a single paragraph summarizing the issue using only the information from the 'Describe the issue' field.

        Format your response exactly like this:
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

        # Parse Ticket Name and Details
        lines = ticket_text.splitlines()
        ticket_name = ""
        details = ""
        for line in lines:
            if line.lower().startswith("ticket name:"):
                ticket_name = line.replace("Ticket Name:", "").strip()
            elif line.lower().startswith("details:"):
                details = line.replace("Details:", "").strip()

        # Save to session state so page doesn't reset
        st.session_state.ticket_generated = True
        st.session_state.ticket_name = ticket_name
        st.session_state.details = details

# Only show formatted ticket if generated
if st.session_state.ticket_generated:
    # 1. Ticket Name
    col1, col2 = st.columns([4,1])
    col1.text_input("Ticket Name:", st.session_state.ticket_name, key="ticket_name")
    if col2.button("Copy Ticket Name"):
        pyperclip.copy(st.session_state.ticket_name)
        st.success("Ticket Name copied!")

    # 2. Name
    col1, col2 = st.columns([4,1])
    col1.text_input("Name:", name, key="name")
    if col2.button("Copy Name"):
        pyperclip.copy(name)
        st.success("Name copied!")

    # 3. Username
    col1, col2 = st.columns([4,1])
    col1.text_input("Username:", username, key="username")
    if col2.button("Copy Username"):
        pyperclip.copy(username)
        st.success("Username copied!")

    # 4. JCCC ID
    col1, col2 = st.columns([4,1])
    col1.text_input("JCCC ID:", idnumber, key="idnumber")
    if col2.button("Copy JCCC ID"):
        pyperclip.copy(idnumber)
        st.success("JCCC ID copied!")

    # 5. Location
    col1, col2 = st.columns([4,1])
    col1.text_input("Location:", roomnumber, key="location")
    if col2.button("Copy Location"):
        pyperclip.copy(roomnumber)
        st.success("Location copied!")

    # 6. Details
    col1, col2 = st.columns([4,1])
    col1.text_area("Details:", st.session_state.details, height=150, key="details")
    if col2.button("Copy Details"):
        pyperclip.copy(st.session_state.details)
        st.success("Details copied!")
