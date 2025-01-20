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

# Display chat history from session state (Messages appear sequentially)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "file" in message:  # If a file was uploaded, display its name
            st.write(f"📄 Uploaded File: {message['file']}")
        st.markdown(message["content"])

# File uploader stays above input box but is not fixed
uploaded_file = st.file_uploader("Upload an image or PDF (optional)", type=["jpg", "jpeg", "png", "pdf"])

# Custom CSS to fix input at the bottom
st.markdown(
    """
    <style>
        .stChatInputContainer {
            position: fixed !important;
            bottom: 0;
            left: 5%;
            width: 90%;
            background: white;
            padding: 10px;
            border-top: 1px solid #ddd;
            box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Fixed chat input box at the bottom
user_input = st.chat_input("Enter your query...")  # Pressing Enter sends message

# Handle user input when Enter is pressed
if user_input:
    # Store user message in session history
    user_message = {"role": "user", "content": user_input}
    if uploaded_file:
        user_message["file"] = uploaded_file.name  # Store file name

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

    # Prepare request payload, including full chat history
    history = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    files = {"file": uploaded_file} if uploaded_file else None
    data = {"query": user_input, "history": json.dumps(history)}  # ✅ Convert history to JSON string

    # Send request to FastAPI backend
    try:
        response = requests.post(f"{API_URL}/query/", data=data, files=files)  # ✅ Keep `data=` instead of `json=`

        print(f"📤 Sent request to backend: {data}, Files: {uploaded_file}")  # Debugging output

        if response.status_code == 200:
            bot_response = response.json().get("response", "No response received.")
        else:
            bot_response = f"Error processing request. Status Code: {response.status_code}, Response: {response.text}"

    except requests.exceptions.RequestException as e:
        bot_response = f"⚠️ Backend Error: {str(e)}"
        print(f"❌ Request Exception: {str(e)}")  # Debugging output

    message_placeholder.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
