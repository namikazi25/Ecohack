import streamlit as st
import requests
import json
import base64
from st_multimodal_chatinput import multimodal_chatinput

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🌿 EcoBot", layout="wide")
st.title("🌿 EcoBot: Your Ecological Assistant")

# Initialize session state for chat history and processed input
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = None
if "last_processed_text" not in st.session_state:
    st.session_state.last_processed_text = ""

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "file" in message:
            st.write(f"📄 Uploaded File: {message['file']}")
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.markdown(f"[🔗 {source}]({source})")

# Get input from the multimodal chat component
chat_input_data = multimodal_chatinput() or {}
st.write("DEBUG: chat_input_data =", chat_input_data)  # For debugging

# Extract text and file(s) from the component output.
text_input = chat_input_data.get("text", "")
# We'll assume that any uploaded file (image or PDF) will come under "images"
uploaded_files = chat_input_data.get("images", [])

# Process input only if new text is present
if text_input and st.session_state.last_processed_text != text_input:
    st.session_state.last_processed_text = text_input

    user_message = {"role": "user", "content": text_input}
    file_bytes = None
    file_type = None

    # Process the first uploaded file if present.
    # (This logic works for both images and PDFs, provided the data URI includes the correct MIME type.)
    if uploaded_files:
        file_data_uri = uploaded_files[0]  # e.g. "data:image/jpeg;base64,..."
        try:
            header, base64_data = file_data_uri.split(",", 1)
            # Extract the MIME type from the header (e.g. "data:image/jpeg;base64")
            file_type = header.split(";")[0].split(":")[1]
            # Use the MIME subtype as extension (e.g. jpeg or pdf)
            ext = file_type.split("/")[-1]
            filename = f"upload.{ext}"
            file_bytes = base64.b64decode(base64_data)
            user_message["file"] = filename
            st.session_state.last_uploaded_file = filename
        except Exception as e:
            st.error(f"Error processing file: {e}")

    st.session_state.messages.append(user_message)

    # Display the user's message
    with st.chat_message("user"):
        st.markdown(text_input)
        if uploaded_files:
            st.write(f"📄 Uploaded File: {user_message.get('file')}")

    # Assistant response area
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.write("Processing...")

        # Create history payload from session state
        history = json.dumps([{"role": msg["role"], "content": msg["content"]} 
                               for msg in st.session_state.messages])
        data = {
            "query": text_input if text_input else "Analyze the uploaded file.",
            "history": history,
            "pdf_context": st.session_state.pdf_context
        }
        
        files = None
        if file_bytes:
            files = {"file": (user_message.get("file"), file_bytes, file_type)}

        try:
            response = requests.post(f"{API_URL}/query/", data=data, files=files)
            st.write("DEBUG: Response status code =", response.status_code)
            st.write("DEBUG: Response text =", response.text)
            response_data = response.json()
            bot_response = response_data.get("response", "No response received.")
            sources = response_data.get("sources", [])
            
            if "pdf_context" in response_data:
                st.session_state.pdf_context = response_data["pdf_context"]
                
        except requests.exceptions.RequestException as e:
            bot_response = f"⚠️ Backend Error: {str(e)}"
            sources = []

        # Display the backend's response and sources
        message_placeholder.markdown(bot_response)
        if sources:
            with st.expander("📚 Sources"):
                for source in sources:
                    st.markdown(f"[🔗 {source}]({source})")

    # Save the assistant's message in session state
    assistant_message = {"role": "assistant", "content": bot_response}
    if sources:
        assistant_message["sources"] = sources
    st.session_state.messages.append(assistant_message)

    # Clear the uploaded file state after processing
    st.session_state.last_uploaded_file = None

    st.rerun()
