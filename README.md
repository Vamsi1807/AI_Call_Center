# 🛎️ AI Call Center

Welcome to **AI Call Center** – an interactive, AI-powered platform to modernize and automate everyday call center operations!

---

## 🚀 What is AI Call Center?

AI Call Center is a Streamlit-based web application that leverages **Google Gemini** AI and real-time **speech recognition** to deliver a seamless, natural language-driven call center experience. The project offers both **Admin** and **User** dashboards, supports Excel data uploads, and provides voice-driven conversations between users and your data.

---

## 🧑‍💼 Key Features

- **🎙️ Real-Time Voice Calls:** Speak to the AI using your microphone! The app converts speech to text and responds using smart AI-generated answers.
- **📊 Admin Dashboard:** Upload, edit, and summarize Excel files. Instantly generate AI-powered summaries and context from your datasets.
- **🤖 Gemini AI Integration:** Uses Google’s Gemini model for intelligent, context-aware responses.
- **📦 Flexible Data Handling:** Easily manage fee structures, student lists, and admissions – just upload your Excel files!
- **🗣️ Interactive UI:** Modern, responsive interface with live speech components and feedback.

---

## 🛠️ Tech Stack

| Technology         | Purpose/Role                                  |
|--------------------|-----------------------------------------------|
| Python             | Main backend language                         |
| Streamlit          | Web app framework for dashboards              |
| Google Gemini API  | AI/NLP model for generating responses         |
| gTTS (Google TTS)  | Text-to-speech for AI voice output            |
| Pandas             | Excel data handling and manipulation          |
| openpyxl           | Reading/writing Excel files                   |
| python-dotenv      | Environment variable management               |
| HTML/CSS/JavaScript| Custom speech recognition UI components       |

---

## 🗂️ Project Structure

```
AI_Call_Center/
├── excel_data/
│   └── admissions.xlsx                # Example Excel file with admissions data
└── frontend/
    ├── admin_dashboard.py             # Admin dashboard Streamlit app
    ├── user_dashboard.py              # User dashboard Streamlit app
    ├── ai_full_context.txt            # Auto-generated context from Excel
    ├── ai_summary.txt                 # Auto-generated summary from Excel
    ├── speech_recognition.html        # HTML/JS component for speech input
    ├── components.html                # Shared HTML components
```

---

## 🧑‍💻 How to Use

### 1. **Clone this repo**
```bash
git clone https://github.com/Vamsi1807/AI_Call_Center.git
cd AI_Call_Center
```

### 2. **Install requirements**
- Make sure you have Python 3.8+.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  (If `requirements.txt` is missing, install: `streamlit`, `google-generativeai`, `gtts`, `python-dotenv`, `pandas`, `openpyxl`)

### 3. **Set up Environment Variables**
- Create a `.env` in the root or frontend folder:
  ```
  GEMINI_API_KEY=your_google_gemini_api_key
  ```

### 4. **Run the Dashboards**

**Admin Dashboard:**
```bash
streamlit run frontend/admin_dashboard.py
```
- Upload Excel files (e.g., fee structure, student lists)
- View or edit data, and generate summaries.

**User Dashboard:**
```bash
streamlit run frontend/user_dashboard.py
```
- Start a voice call.
- Speak your query – the AI will listen, process, and reply with synthesized speech!

---

## 🏗️ Example Data

- `excel_data/admissions.xlsx` – Sample admissions info for demo/testing.
- `frontend/ai_full_context.txt` and `ai_summary.txt` are auto-generated when you use the admin dashboard.

---

## 🙌 Contributing

Contributions, ideas, and issues are welcome!  
Just fork this repo, create a branch, and submit a pull request.

---

### 💡 Get Ready to Revolutionize Your Call Center Experience with AI!

```
Feel free to customize this README with your own screenshots, links, and further details!
```
