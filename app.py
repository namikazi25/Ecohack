import streamlit as st
import requests
from PIL import Image
import io

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🌿 EcoBot", layout="wide")
st.title("🌿 EcoBot: Your Ecological Assistant")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "file_type" not in st.session_state:
    st.session_state.file_type = None

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user" and "file" in message:
            st.write("Uploaded File:", message["file"])
        st.write(message["content"])

# Upload & Input Together
with st.form("input_form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Upload an image or PDF (optional)", type=["jpg", "jpeg", "png", "pdf"])
    user_query = st.text_input("Enter your query:")
    submit_button = st.form_submit_button("Submit")

# Handle User Input & Upload
if submit_button and user_query:
    file_content = uploaded_file.read() if uploaded_file else None
    file_type = uploaded_file.type if uploaded_file else None

    # Add user message to chat history
    user_message = {"role": "user", "content": user_query}
    if uploaded_file:
        user_message["file"] = uploaded_file.name

    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.write(user_query)

    if uploaded_file:
        st.write(f"Uploaded File: {uploaded_file.name}")

    # Placeholder for bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.write("Processing...")

    # Send request to FastAPI
    files = {"file": (uploaded_file.name, file_content, file_type)} if uploaded_file else None
    data = {"query": user_query}

    response = requests.post(f"{API_URL}/query/", files=files, data=data)

    if response.status_code == 200:
        bot_response = response.json().get("response", "No response received.")
    else:
        bot_response = "Error processing request."

    # Update assistant message
    message_placeholder.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

elif submit_button:
    st.warning("Please enter a query.")
