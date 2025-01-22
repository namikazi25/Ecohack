import streamlit as st
import requests
import json

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🌿 EcoBot", layout="wide")
st.title("🌿 EcoBot: Your Ecological Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None  # Store the last uploaded file name
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = None  # Store latest PDF content

# Display chat history (Messages appear sequentially)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "file" in message:  # If a file was uploaded, display its name
            st.write(f"📄 Uploaded File: {message['file']}")
        st.markdown(message["content"])

# File uploader (supports images & PDFs)
uploaded_file = st.file_uploader("Upload an image or PDF (optional)", type=["jpg", "jpeg", "png", "pdf"])

# Fixed chat input box at the bottom
user_input = st.chat_input("Enter your query...")

# Handle user input when Enter is pressed
if user_input:
    user_message = {"role": "user", "content": user_input}
    
    if uploaded_file:
        user_message["file"] = uploaded_file.name  # Store file name in chat memory
        st.session_state.last_uploaded_file = uploaded_file.name  # Store for clearing

    st.session_state.messages.append(user_message)

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.write(f"📄 Uploaded File: {uploaded_file.name}")

    # Placeholder for bot response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.write("Processing...")

    # Prepare request payload
    history = json.dumps([{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages])
    
     # data = {"query": user_input, "history": history}
    data = {
    "query": user_input if user_input else "Analyze the uploaded file.",
    "history": history,
    "pdf_context": st.session_state.pdf_context  # Send current PDF context
}
    
    files = None
    if uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

   

    # Send request to FastAPI backend
    try:
        response = requests.post(f"{API_URL}/query/", data=data, files=files)
        bot_response = response.json().get("response", "No response received.")
    except requests.exceptions.RequestException as e:
        bot_response = f"⚠️ Backend Error: {str(e)}"

    message_placeholder.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # **Auto-clear uploaded file after processing**
    st.session_state.last_uploaded_file = None
    st.rerun()  # Refresh the UI to clear the file uploader
