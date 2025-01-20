```markdown
# 🌿 EcoBot: AI-Powered Ecological Assistant

EcoBot is an AI-powered chatbot that helps users identify species from images, analyze biodiversity, and answer ecological questions. It supports **chat history persistence** and **image/PDF processing** using GPT-4o Mini.

---

## 🚀 Features
✅ **Chatbot interface** with **Streamlit**  
✅ **Supports file uploads** (images & PDFs) for analysis  
✅ **Uses GPT-4o Mini** for intelligent ecological responses  
✅ **Maintains chat history** for contextual conversations  
✅ **FastAPI backend** to handle queries  

---

## 📂 **Project Structure**

EcoBot/
│── backend/
│   ├── main.py               # FastAPI backend
│   ├── gpt_handler.py         # GPT-4o Mini processing
│── frontend/
│   ├── app.py                # Streamlit frontend
│── tests/                     # Test scripts
│── .env                       # API key configuration
│── requirements.txt           # Dependencies
│── README.md                  # Documentation


---

## 🛠️ **Setup Instructions**

### **1️⃣ Clone the Repository**

git clone https://github.com/your-repo/ecobot.git
cd ecobot


### **2️⃣ Create a Virtual Environment**

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


### **3️⃣ Install Dependencies**

pip install -r requirements.txt


### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the root folder and add:

OPENAI_API_KEY=your-openai-api-key


---

## ▶️ **How to Run the App**
### **1️⃣ Start the FastAPI Backend**
cd backend
uvicorn main:app --reload


### **2️⃣ Start the Streamlit Frontend**
Open a new terminal and run:
streamlit run app.py


---

## 📌 **How It Works**
1️⃣ **User uploads an image or PDF (optional) and types a query**  
2️⃣ **Streamlit frontend sends request to FastAPI backend**  
3️⃣ **FastAPI processes the request and passes it to GPT-4o Mini**  
4️⃣ **GPT-4o Mini analyzes the query, chat history, and uploaded file**  
5️⃣ **Response is sent back and displayed in the chat UI**  

---

## 🛠️ **Troubleshooting**
❌ **Getting a "Field required" error?**  
✅ Make sure `history` is being sent as `json.dumps(history)`.  

❌ **Chatbot doesn't remember previous messages?**  
✅ Ensure `st.session_state.messages` is correctly maintained.  

❌ **File uploads not working?**  
✅ Make sure you're sending files using `files=files` in `requests.post()`.  

---

## 📜 **License**
This project is **open-source**. Feel free to modify and contribute!

---

## 🙌 **Contributing**
🚀 Want to improve EcoBot? Fork the repo, submit a PR, and let's build together! 🌱
