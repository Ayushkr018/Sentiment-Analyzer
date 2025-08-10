<div align="center">
  
# 🎭 **NIVA** 🎙️
### *The Sentient Voice Assistant - Emotion Aware AI*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Sentiment Analysis](https://img.shields.io/badge/AI-Sentiment%20Analysis-purple.svg)](https://github.com)
[![Multilingual](https://img.shields.io/badge/Support-Multilingual-orange.svg)](https://github.com)

**🧠 Emotion Intelligence • 🌍 Multilingual • 👩‍💻 Feminine AI • 🎵 Mood Music**

[🚀 Quick Start](#-quick-start) • [🎯 Features](#-features) • [💡 Demo](#-live-demo) • [🛠️ Setup](#-installation)

</div>

---

## 🌟 **What Makes NIVA Special?**

**NIVA** (Neural Interactive Voice Assistant) isn't just another chatbot – it's your **emotion-aware digital companion** that truly understands how you feel. With advanced sentiment analysis, multilingual support, and a dynamic 3D web interface, NIVA creates conversations that feel genuinely human.

### ✨ **Core Highlights**
- 🎭 **Emotion Recognition** – Analyzes tone, pitch, and content to understand your feelings
- 💬 **Empathetic Responses** – Responds appropriately to your emotional state
- 🌍 **Multilingual Magic** – Understands and responds in multiple languages
- 👩‍💻 **Feminine Personality** – Warm, caring, and intuitive conversational style
- 🎵 **Mood-Based Music** – Plays music that matches your current emotional state
- ✨ **3D Web UI** – Beautiful animated interface with real-time visualizations

---

## 🎯 **Features**

### 🎤 **Advanced Voice Processing**
| Capability | Technology | What It Does |
|------------|------------|--------------|
| **Voice Recognition** | SpeechRecognition | Converts speech to text with high accuracy |
| **Natural Speech** | pyttsx3 | Generates human-like voice responses |
| **Emotion Detection** | Transformers + NLP | Analyzes emotional content from voice |
| **Pitch Analysis** | Audio processing | Detects emotional tone and stress patterns |

### 🧠 **AI-Powered Intelligence**
- **🤖 Gemini AI Integration**: Advanced conversational AI capabilities
- **📊 Cohere API**: Enhanced natural language understanding
- **💭 Sentiment Analysis**: Real-time emotion classification
- **🎯 Context Awareness**: Remembers conversation context and mood

### 🌍 **Multilingual Support**
- **🔍 Language Detection**: Automatically identifies spoken language
- **🌐 Translation**: LibreTranslate API for seamless communication
- **💬 Natural Responses**: Maintains personality across languages
- **🎵 Cultural Adaptation**: Music and responses adapted to cultural context

### 🎨 **Interactive Web Interface**
- **🔐 Login Screen**: Elegant entry point with glowing microphone animation
- **💬 Chat Interface**: Sentiment-aware text conversations
- **🎙️ Voice UI**: 3D visualizations that respond to your voice
- **📱 Responsive Design**: Works perfectly on all devices

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- Microphone for voice input
- Internet connection for AI APIs
- Modern web browser (Chrome, Firefox, Safari)

### **Installation**
Clone the repository
git clone https://github.com/yourusername/niva-assistant.git
cd niva-assistant

Create virtual environment (recommended)
python -m venv niva-env
source niva-env/bin/activate # On Windows: niva-env\Scripts\activate

Install dependencies
pip install -r requirements.txt

Set up API keys (see Configuration section below)
Edit main.py and voice.py with your API keys
Launch NIVA
uvicorn main:app --reload

text

### **First Experience**
1. **Open browser** → Navigate to `http://127.0.0.1:8000/`
2. **Login** → Use the beautiful animated login interface
3. **Choose Mode**:
   - **Chat Mode** → `http://127.0.0.1:8000/chat` for text conversations
   - **Voice Mode** → `http://127.0.0.1:8000/voice.html` for voice interactions
4. **Start Talking** → NIVA will detect your emotions and respond accordingly

---

## 💡 **Live Demo**

### **Emotion Detection in Action**
You: "I'm feeling really stressed about my exams"
NIVA: "I can hear the worry in your voice. Exams can be overwhelming, but you're
stronger than you think. Would you like me to play some calming music or
share some study tips to help you feel more confident?"

You: "I just got promoted at work!"
NIVA: "That's absolutely wonderful! I can feel your excitement and happiness!
Congratulations on your well-deserved promotion. This calls for celebration -
would you like me to play some upbeat music to match your joyful mood?"

text

### **Multilingual Conversation**
You: "Namaste, aaj main bahut khush hun"
NIVA: "Namaste! Main sun sakti hun ki aap bahut khush hain aaj. Kya baat hai?
Kuch special celebration karne ka man kar raha hai?"

You: "¿Cómo estás hoy?"
NIVA: "¡Hola! Estoy muy bien, gracias. Noto que hablas en español.
¿Cómo puedo ayudarte hoy?"

text

---

## 🛠️ **Technical Architecture**

### **Project Structure**
NIVA/
├── main.py # FastAPI backend server
├── voice.py # Python voice interface engine
├── frontend/
│ ├── login.html # Animated login screen
│ ├── index.html # Sentiment chat interface
│ ├── voice.html # 3D voice visualization UI
│ └── assets/
│ ├── css/ # Custom styling & animations
│ ├── js/ # Frontend JavaScript
│ └── audio/ # Sound effects & notifications
├── models/
│ ├── sentiment_model.py # Emotion classification
│ ├── voice_analysis.py # Audio processing
│ └── language_detector.py # Multilingual handling
├── requirements.txt # Python dependencies
├── config.py # Configuration settings
└── README.md # This documentation

text

### **Technology Stack**
<div align="center">

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend API** | 🚀 FastAPI + Uvicorn | High-performance async server |
| **Frontend** | 🎨 HTML5 + CSS3 + JavaScript | Interactive 3D web interface |
| **AI Models** | 🤖 Gemini AI + Cohere | Advanced conversational intelligence |
| **NLP Processing** | 🧠 Transformers + LangDetect | Sentiment analysis & language detection |
| **Voice Engine** | 🎤 SpeechRecognition + pyttsx3 | Voice input/output processing |
| **Translation** | 🌍 LibreTranslate API | Real-time language translation |

</div>

---

## ⚙️ **Configuration**

### **API Keys Setup**
Create a `.env` file or update the following files with your API keys:

**In `main.py`:**
Replace with your actual API keys
GEMINI_API_KEY = "your-gemini-api-key-here"
COHERE_API_KEY = "your-cohere-api-key-here"

text

**In `voice.py`:**
Add your Gemini API key
GEMINI_API_KEY = "your-gemini-api-key-here"

text

### **Getting API Keys**
- **🤖 Gemini AI**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **🔗 Cohere**: Sign up at [Cohere Dashboard](https://dashboard.cohere.ai/)
- **🌐 LibreTranslate**: Free tier available at [LibreTranslate](https://libretranslate.com/)

---

## 🎭 **Emotion Recognition Capabilities**

### **Supported Emotions**
| Emotion | Detection Method | NIVA's Response Style |
|---------|------------------|---------------------|
| **😊 Happiness** | Voice tone + keywords | Enthusiastic and celebratory |
| **😢 Sadness** | Audio pitch + content analysis | Comforting and supportive |
| **😠 Anger** | Voice intensity + word choice | Calming and understanding |
| **😰 Stress/Anxiety** | Speech patterns + keywords | Reassuring and helpful |
| **😐 Neutral** | Balanced tone indicators | Friendly and informative |
| **🤔 Confusion** | Question patterns + hesitation | Patient and explanatory |

### **Sentiment Analysis Process**
Voice Input → Speech Recognition → Text Analysis → Emotion Classification
↓ ↓ ↓ ↓
Audio Processing → Language Detection → Context Understanding → Response Generation
↓ ↓ ↓ ↓
Pitch Analysis → Translation (if needed) → Mood Assessment → Empathetic Reply

text

---

## 🌍 **Multilingual Support**

### **Supported Languages**
- 🇺🇸 **English** - Native support with full emotional understanding
- 🇮🇳 **Hindi** - Complete Hinglish and pure Hindi support
- 🇪🇸 **Spanish** - Cultural context-aware responses
- 🇫🇷 **French** - Elegant and sophisticated conversation style
- 🇩🇪 **German** - Precise and informative communication
- 🇨🇳 **Chinese** - Respectful and culturally appropriate responses

### **Language Features**
- **🔍 Auto-Detection**: Automatically identifies spoken language
- **💬 Code-Switching**: Handles mixed languages (like Hinglish)
- **🎭 Cultural Adaptation**: Adjusts personality to cultural norms
- **🎵 Localized Music**: Suggests music from appropriate cultural context

---

## 🎨 **User Interface Showcase**

### **🔐 Login Screen** (`/`)
- Animated glowing microphone with pulse effects
- Smooth gradient backgrounds with particle animations
- Elegant typography with modern design aesthetics
- Responsive layout that works on all screen sizes

### **💬 Chat Interface** (`/chat`)
- Real-time sentiment indicators during conversations
- Emotion-based color themes that change with your mood
- Message bubbles that reflect emotional context
- Live typing indicators with personality touches

### **🎙️ Voice Interface** (`/voice.html`)
- 3D visualizations that dance to your voice
- Real-time audio waveform displays
- Particle effects that respond to emotional intensity
- Voice activity indicators with smooth animations

---

## 🎵 **Mood-Based Music Integration**

NIVA doesn't just talk – it creates the perfect atmosphere for your conversations:

### **Music Selection Algorithm**
Detected Emotion → Music Genre Mapping → YouTube Integration → Playlist Creation
↓ ↓ ↓ ↓
Happiness → Upbeat Pop Sadness → Soft Ballads Anger → Calming Instrumental
Stress → Relaxing Ambient Neutral → Light Background Excited → Energetic Beats

text

### **Smart Playlist Features**
- **🎯 Context-Aware**: Considers time of day and conversation topic
- **⏰ Duration Control**: Plays music for appropriate lengths
- **🔄 Seamless Transitions**: Smooth changes between different moods
- **👤 Personal Preferences**: Learns your music taste over time

---

## 🚀 **Development & Customization**

### **Adding New Emotions**
1. **Update Sentiment Model**: Add new emotion categories
2. **Train Recognition**: Include sample data for new emotions
3. **Define Responses**: Create appropriate response templates
4. **Test & Validate**: Ensure accurate detection and appropriate responses

### **Extending Language Support**
1. **Language Models**: Add new language detection patterns
2. **Response Templates**: Create culturally appropriate response styles
3. **Translation Integration**: Configure translation API endpoints
4. **Cultural Context**: Define cultural norms and conversation styles

### **Custom UI Themes**
/* Example: Adding a new emotion theme */
.mood-excited {
background: linear-gradient(135deg, #ff6b6b, #feca57);
animation: pulse 1.5s infinite;
}

.mood-calm {
background: linear-gradient(135deg, #74b9ff, #0984e3);
animation: breathe 3s infinite;
}

text

---

## 📊 **Performance & Analytics**

### **System Requirements**
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 4GB | 8GB+ |
| **CPU** | Dual-core 2.0GHz | Quad-core 2.5GHz+ |
| **Storage** | 2GB free space | 5GB free space |
| **Internet** | 1 Mbps | 5 Mbps+ |
| **Microphone** | Any USB/built-in | High-quality condenser mic |

### **Response Times**
- **Voice Recognition**: < 2 seconds
- **Emotion Analysis**: < 1 second  
- **AI Response Generation**: < 3 seconds
- **Text-to-Speech**: < 1 second
- **Total Interaction Time**: < 5 seconds

---

## 🤝 **Contributing**

### **Ways to Contribute**
- 🐛 **Bug Reports**: Help us improve reliability
- 💡 **Feature Ideas**: Suggest new emotion recognition capabilities
- 🌍 **Language Support**: Add new languages and cultural contexts
- 🎨 **UI Improvements**: Enhance the visual experience
- 📚 **Documentation**: Improve guides and examples

### **Development Setup**
Fork the repository
git fork https://github.com/yourusername/niva-assistant.git

Create feature branch
git checkout -b feature/emotion-detection-improvement

Make your changes and test thoroughly
python -m pytest tests/

Submit pull request with detailed description
text

---

## 🔒 **Privacy & Ethics**

### **Data Protection**
- ✅ **Voice Data**: Processed locally, not stored permanently
- ✅ **Conversations**: Temporary processing only, no long-term storage
- ✅ **Emotions**: Analysis results are not saved or tracked
- ✅ **API Usage**: Only sent to trusted AI providers with encryption

### **Ethical AI Principles**
- 🤝 **Respectful**: Treats all users with dignity regardless of emotional state
- 🌍 **Inclusive**: Supports diverse languages and cultural contexts
- 🛡️ **Safe**: Designed to provide emotional support, not replace professional help
- 🔍 **Transparent**: Open about AI capabilities and limitations

---

## 📄 **License & Credits**

### **License**
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### **Credits & Acknowledgments**
- **🤖 AI Models**: Google Gemini AI, Cohere
- **🎤 Voice Processing**: SpeechRecognition, pyttsx3
- **🌐 Translation**: LibreTranslate
- **🎨 UI Inspiration**: Modern voice assistant interfaces
- **🧠 NLP**: Hugging Face Transformers

---

## 📞 **Support & Community**

### **Get Help**
- 📖 **Documentation**: Comprehensive guides in this README
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/niva/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/niva/discussions)
- 📧 **Email**: ayush.kumar@example.com

### **Stay Updated**
- ⭐ **Star** this repository to show support
- 👀 **Watch** for updates and new features
- 🍴 **Fork** to create your own version
- 📢 **Share** with friends who love AI technology

---

<div align="center">

### 🎭 **Created with ❤️ by Ayush Kumar** 🎙️

**B.Tech 2022–2026 | Python • C++ • AI Enthusiast**

*NIVA - Where Technology Meets Empathy*

**[⬆ Back to Top](#-niva-)**

---

**🌟 "In a world of artificial intelligence, NIVA brings artificial empathy" 🌟**

</div>
