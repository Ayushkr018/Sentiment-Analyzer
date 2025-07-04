# Sentiment-Analyzer
This project uses voice input to detect and classify human emotions using sentiment analysis techniques. By integrating speech recognition with natural language processing, the system analyzes the tone, pitch, and content of spoken language to determine emotional states like happiness, sadness, anger, or neutrality. 
# 🎙️ NIVA — The Sentient Voice Assistant

Niva is a multilingual, emotion-aware voice assistant designed with a dynamic 3D web UI and feminine conversational personality. It understands user emotions, responds empathetically, and supports both voice and text input, making conversations feel truly human-like.

![Niva Screenshot](https://via.placeholder.com/900x400.png?text=NIVA+Screenshot) <!-- Replace with your own image -->

## 💡 Features

- 🎤 **Voice Recognition & Text Commands** (SpeechRecognition, Pyttsx3)
- 🌍 **Multilingual Support** (LangDetect + LibreTranslate API)
- ❤️ **Mood Detection & Response** (Sentiment-aware replies)
- 🤖 **AI Chat via Gemini + Cohere API**
- 🎵 **Mood-Based Music Playback** (YouTube integrations)
- 💬 **Feminine Voice & Empathetic Responses**
- 💻 **FastAPI Backend + Jinja2 Templating**
- ✨ **Animated Web UIs** (`login.html`, `voice.html`, `index.html`)
- 🔒 **Login Interface (No auth backend yet)**

---

## 🧠 Tech Stack

| Component         | Technology                           |
|------------------|--------------------------------------|
| Backend API       | FastAPI                              |
| Frontend UI       | HTML, CSS (Custom + Animation)       |
| NLP & Sentiment   | `transformers`, `langdetect`, Cohere |
| Voice Handling    | `speech_recognition`, `pyttsx3`      |
| AI Assistant      | Gemini AI (`google.generativeai`)    |
| Deployment Ready  | Uvicorn server                       |

---

## 🚀 Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/niva-assistant.git
cd niva-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API keys
# - Update `main.py` and `voice.py` with your Gemini + Cohere API keys.

# 4. Run the app
uvicorn main:app --reload
📁 frontend/
 ├── login.html         # Login screen with glowing mic animation
 ├── index.html         # Sentiment chat interface
 ├── voice.html         # Voice-driven assistant with 3D visuals
📄 main.py               # FastAPI backend server
📄 voice.py              # Python voice interface (TTS + speech recognition)

🌐 Accessing Niva
Login Page → http://127.0.0.1:8000/

Chat UI → http://127.0.0.1:8000/chat

Voice UI → http://127.0.0.1:8000/voice.html

🔒 API Keys Required
Make sure to replace the placeholders with your Cohere and Gemini API keys in:

main.py (for Gemini + Cohere)

voice.py (for Gemini)

👩‍💻 Author
Ayush Kumar
B.Tech 2022–2026
Python • C++ • AI Enthusiast
Project: Niva – Your Emotional AI Companion

📃 License
This project is licensed under the MIT License.
Feel free to modify and share with attribution.

yaml
Copy
Edit

---

Let me know if you’d like help with a [project thumbnail](f), [GitHub repo description](f), or [depl
