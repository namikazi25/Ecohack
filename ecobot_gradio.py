import gradio as gr
import requests
import mimetypes

# Point this to your running FastAPI backend:
API_URL = "http://localhost:8000/query/"

def call_backend(message: str, file_obj=None):
    """
    Sends 'message' (the user's query) and optional 'file_obj'
    to the FastAPI backend, and returns the JSON response.
    """
    data = {"query": message}
    files = {}

    if file_obj is not None:
        # 'file_obj' is a Gradio file-like object
        mime_type = mimetypes.guess_type(file_obj.name)[0] or "application/octet-stream"
        files["file"] = (file_obj.name, file_obj, mime_type)

    try:
        response = requests.post(API_URL, data=data, files=files)
        return response.json()
    except Exception as e:
        return {"response": f"Backend Error: {str(e)}", "sources": []}

def user_message(user_input, history):
    """
    Gradio handler for the user's text input.
    Returns the user input and the current chat history *unchanged*,
    so we can pass them along to the bot handler next.
    """
    return user_input, history

def bot_response(user_input, history, uploaded_file):
    """
    Gradio handler that actually calls the backend.
    It:
      1) Sends the user input + optional uploaded file to the backend
      2) Gets a response
      3) Updates the chat history with the new (user -> bot) messages
    """
    # Call the FastAPI backend
    backend_data = call_backend(user_input, uploaded_file)

    bot_text = backend_data.get("response", "No response received.")
    sources = backend_data.get("sources", [])

    # Optionally append the sources if they exist
    if sources:
        formatted_sources = "\n".join(f"- {src}" for src in sources)
        bot_text += f"\n\n**Sources**:\n{formatted_sources}"

    # Update chat history (a list of tuples: [(user_msg, bot_msg), ... ])
    history.append((user_input, bot_text))
    return history

with gr.Blocks() as demo:
    gr.Markdown("# EcoBot (Gradio Frontend)\nEnter a query and optionally upload a file.")

    # We'll store the conversation in a list of (user, bot) messages.
    # 'gr.State' allows us to keep data persistent within a user's session.
    chat_history = gr.State([])

    chatbot = gr.Chatbot(label="EcoBot Chat")
    file_upload = gr.File(
        label="Optional: Upload PDF/Image", 
        file_types=[".pdf", ".jpg", ".jpeg", ".png"]
    )
    user_input = gr.Textbox(
        placeholder="Type your question or request...",
        label="Your message"
    )
    submit_btn = gr.Button("Send")

    # 1) First, we take the user's text + existing history
    #    and just pass them straight through. We do NOT update
    #    the display in this step. We only keep track of what
    #    the user said so far.
    submit_btn.click(
        fn=user_message, 
        inputs=[user_input, chat_history],
        outputs=[user_input, chat_history],
        queue=False
    )

    # 2) Then, we call the bot_response function, which does:
    #    - calls the FastAPI backend
    #    - updates the chat history with the new (user -> bot) turn
    #    - returns the updated chat history so the chatbot component is updated
    submit_btn.click(
        fn=bot_response,
        inputs=[user_input, chat_history, file_upload],
        outputs=[chatbot]
    )

    # The user_input box will automatically clear after step 1 & 2 complete.

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
