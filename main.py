from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pydantic import BaseModel
from langdetect import detect, LangDetectException
from transformers import pipeline
from cohere import ClientV2
import uvicorn
import requests
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multilingual Chatbot API", version="1.0.0")

# Add CORS middleware to allow frontend requests
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates and static files
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="frontend")
# Mount static files at /static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_ui(request: Request):
    """Serve the chat UI page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/voice.html", response_class=HTMLResponse)
async def voice_ui(request: Request):
    """Serve the voice UI page."""
    return templates.TemplateResponse("voice.html", {"request": request})

# Load sentiment analysis pipeline (multilingual)
try:
    sentiment_analyzer = pipeline(
        "sentiment-analysis", 
        model="nlptown/bert-base-multilingual-uncased-sentiment"
    )
    logger.info("Sentiment analyzer loaded successfully")
except Exception as e:
    logger.error(f"Failed to load sentiment analyzer: {e}")
    sentiment_analyzer = None

# Initialize Cohere ClientV2
COHERE_API_KEY = ""  # Replace with your actual Cohere API key
try:
    client = ClientV2(api_key=COHERE_API_KEY)
    logger.info("Cohere client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Cohere client: {e}")
    client = None

# Simple in-memory conversation history store (for demonstration)
conversation_history: Dict[str, List[Dict[str, str]]] = {}

# New dictionary to store user language preferences
user_language_preference: Dict[str, str] = {}

class Message(BaseModel):
    user_id: str
    text: str

class ChatResponse(BaseModel):
    reply: str
    sentiment: Optional[str]
    language: str
    conversation_history: List[Dict[str, str]]

def detect_language(text: str) -> str:
    """Detect the language of the input text."""
    try:
        lang = detect(text)
        logger.info(f"Detected language: {lang}")
        return lang
    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e}")
        return "en"  # Default to English
    except Exception as e:
        logger.error(f"Unexpected error in language detection: {e}")
        return "en"

def translate_text(text: str, target_lang: str) -> str:
    """
    Translate text to target language using LibreTranslate API.
    """
    if not text or target_lang in ["unknown", "en"]:
        return text  # No translation needed

    try:
        url = "https://libretranslate.de/translate"
        payload = {
            "q": text,
            "source": "auto",
            "target": target_lang,
            "format": "text"
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("translatedText", text)
            logger.info(f"Translation successful: {text[:50]}... -> {translated_text[:50]}...")
            return translated_text
        else:
            logger.warning(f"Translation API returned status {response.status_code}")
            return text
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Translation request failed: {e}")
        return text
    except Exception as e:
        logger.error(f"Unexpected error in translation: {e}")
        return text

def analyze_sentiment(text: str) -> tuple[str, float]:
    """Analyze sentiment of the text - Enhanced to handle multilingual model output."""
    if not sentiment_analyzer:
        return "NEUTRAL", 0.5
    
    try:
        result = sentiment_analyzer(text)[0]
        sentiment_label = result['label']
        sentiment_score = result['score']
        
        # Better mapping for the nlptown multilingual model
        normalized_label = sentiment_label.upper()
        
        if any(neg in normalized_label for neg in ['1 STAR', '2 STAR', 'NEG']):
            mapped_sentiment = "NEGATIVE"
        elif any(pos in normalized_label for pos in ['4 STAR', '5 STAR', 'POS']):
            mapped_sentiment = "POSITIVE"
        else:
            mapped_sentiment = "NEUTRAL"
        
        logger.info(f"Sentiment analysis: {mapped_sentiment} ({sentiment_score:.2f}) - Original: {sentiment_label}")
        return mapped_sentiment, sentiment_score
        
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return "NEUTRAL", 0.5

import google.generativeai as genai
import random

def get_gemini_response(user_input: str, user_mood: str = "neutral") -> str:
    """Generate response using Gemini AI with feminine voice assistant personality."""
    try:
        genai.configure(api_key="AIzaSyAIb4W_ev8Ur2QZBeN73tdc5EOA4_YhDiQ")
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "max_output_tokens": 100,
        }
        
        gemini_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=generation_config
        )
        
        prompt = f"""You are Niva, a friendly female voice assistant. The user said: "{user_input}"

Rules:
- ALWAYS respond in ENGLISH ONLY (no Hindi words)
- Keep response very short (1-2 sentences max)
- Be caring and supportive like a female friend
- If user seems confused, offer help
- If user is sad, be comforting  
- If user is happy, be encouraging
- Ask follow-up questions when appropriate
- Be conversational and natural
- Sound warm and feminine in your responses

Current mood context: {user_mood}

Respond in clear English with a warm, feminine tone:"""
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            # Fallback responses
            fallback_responses = [
                "I'm here to listen, dear. Please tell me more.",
                "Don't worry, honey. I'm here to help.",
                "Take your time, sweetie. What would you like to talk about?"
            ]
            return random.choice(fallback_responses)
        
    except Exception as e:
        logger.error(f"Gemini AI error: {e}")
        fallback_responses = [
            "I'm here to listen, dear. Please tell me more.",
            "Don't worry, honey. I'm here to help.",
            "Take your time, sweetie. What would you like to talk about?"
        ]
        return random.choice(fallback_responses)

def generate_empathetic_response(sentiment_label: str, lang: str, user_text: str = "") -> str:
    """Generate empathetic prefix based on sentiment - Enhanced version."""
    
    # Expanded empathetic responses for more languages
    empathetic_responses = {
        "en": {
            "negative": "I'm sorry to hear that. ",
            "positive": "I'm glad to hear that! ",
            "neutral": ""
        },
        "es": {
            "negative": "Lamento escuchar eso. ",
            "positive": "¡Me alegra escuchar eso! ",
            "neutral": ""
        },
        "fr": {
            "negative": "Je suis désolé d'entendre cela. ",
            "positive": "Je suis content d'entendre ça! ",
            "neutral": ""
        },
        "de": {
            "negative": "Es tut mir leid, das zu hören. ",
            "positive": "Das freut mich zu hören! ",
            "neutral": ""
        },
        "it": {
            "negative": "Mi dispiace sentirlo. ",
            "positive": "Sono felice di sentirlo! ",
            "neutral": ""
        },
        "pt": {
            "negative": "Lamento ouvir isso. ",
            "positive": "Fico feliz em ouvir isso! ",
            "neutral": ""
        },
        "hi": {
            "negative": "मुझे यह सुनकर दुख हुआ। ",
            "positive": "मुझे यह सुनकर खुशी हुई! ",
            "neutral": ""
        },
        "zh": {
            "negative": "听到这个我很难过。",
            "positive": "听到这个我很高兴！",
            "neutral": ""
        },
        "ar": {
            "negative": "أنا آسف لسماع ذلك. ",
            "positive": "أنا سعيد لسماع ذلك! ",
            "neutral": ""
        },
        "ru": {
            "negative": "Мне жаль это слышать. ",
            "positive": "Рад это слышать! ",
            "neutral": ""
        }
    }
    
    # Determine sentiment category
    if any(neg in sentiment_label.upper() for neg in ["NEG", "1", "2"]):
        sentiment_key = "negative"
    elif any(pos in sentiment_label.upper() for pos in ["POS", "4", "5"]):
        sentiment_key = "positive"
    else:
        sentiment_key = "neutral"
    
    # Use predefined response if available
    if lang in empathetic_responses:
        responses = empathetic_responses[lang]
        return responses.get(sentiment_key, "")
    
    # For unsupported languages, use Cohere to generate empathetic response
    if client and sentiment_key != "neutral" and user_text:
        try:
            prompt = f"""Generate a very short empathetic response in {lang} language for someone who seems {sentiment_key}. 
            Keep it brief (under 10 words) and natural. Just the empathetic phrase with a space at the end.
            
            Examples:
            - English negative: "I'm sorry to hear that. "
            - English positive: "I'm glad to hear that! "
            
            Respond only with the empathetic phrase in {lang}:"""
            
            response = client.chat(
                model="command-r-plus",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=30
            )
            
            empathetic_response = str(response.message.content).strip()
            if empathetic_response and len(empathetic_response) < 50:  # Sanity check
                return empathetic_response + " " if not empathetic_response.endswith(" ") else empathetic_response
                
        except Exception as e:
            logger.error(f"Failed to generate empathetic response: {e}")
    
    return ""  # Return empty for neutral or if generation fails

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the chat UI."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "sentiment_analyzer": sentiment_analyzer is not None,
        "cohere_client": client is not None
    }

@app.post("/chat", response_model=ChatResponse)
def chat(message: Message):
    """Main chat endpoint - Enhanced for better multilingual support."""
    try:
        user_id = message.user_id
        text = message.text.strip()
        
        if not text:
            raise HTTPException(status_code=400, detail="Message text cannot be empty")
        
        logger.info(f"Processing message from user {user_id}: {text[:100]}...")
        
        # Detect language
        detected_lang = detect_language(text)
        
        # Use stored user language preference if exists, else store detected language
        lang = user_language_preference.get(user_id)
        if lang:
            # Do not update language preference to keep it consistent
            pass
        else:
            user_language_preference[user_id] = detected_lang
            lang = detected_lang
        
        # Analyze sentiment
        sentiment_label, sentiment_score = analyze_sentiment(text)
        
        # Initialize conversation history for user if not present
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Get last bot message for context
        last_bot_message = None
        for entry in reversed(conversation_history[user_id]):
            if entry["role"] == "bot":
                last_bot_message = entry["text"]
                break
        
        # Simple dialogue flow management
        if last_bot_message and "sorry to hear that" in last_bot_message.lower():
            if any(keyword in text.lower() for keyword in ["because", "due to", "reason"]):
                reply = "Thank you for sharing. Remember, it's okay to feel this way. Would you like some suggestions to help you feel better?"
            else:
                reply = "Would you like to tell me more about what's bothering you? I'm here to listen."
        else:
            # Prepare messages for Cohere chat
            messages = [{"role": entry["role"], "text": entry["text"]} 
                       for entry in conversation_history.get(user_id, [])]
            
            # Translate user input to English for model if needed
            input_for_model = text
            if lang != "en":
                input_for_model = translate_text(text, "en")
            
            # Replace last user message with translated input if applicable
            if messages and messages[-1]["role"] == "user":
                messages[-1]["text"] = input_for_model
            else:
                messages.append({"role": "user", "text": input_for_model})
            
            # Get response from Gemini AI (now with language parameter)
            reply_generated = get_gemini_response(text, user_mood="neutral")
            
            # Add empathetic prefix based on sentiment (now with user_text parameter)
            empathetic_prefix = generate_empathetic_response(sentiment_label, lang, text)
            
            # Combine empathetic prefix with generated response
            # Translate reply back to user's language if needed
            if lang != "en":
                reply_generated = translate_text(reply_generated, lang)
            reply = empathetic_prefix + reply_generated

        # Clean reply string from unwanted formatting like type='text' text=
        import re
        reply = re.sub(r'type=[\'"]text[\'"]\s*text=[\'"]([^\'"]*)[\'"]', r'\1', reply)
        
        # Update conversation history
        conversation_history[user_id].append({"role": "user", "text": text})
        conversation_history[user_id].append({"role": "bot", "text": reply})
        
        # Limit conversation history to last 20 messages to prevent memory issues
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
        # Format conversation history for response
        formatted_history = []
        for entry in conversation_history[user_id]:
            if entry["role"] == "user":
                formatted_history.append({"user": entry["text"]})
            else:
                formatted_history.append({"bot": entry["text"]})
        
        logger.info(f"Successfully processed message for user {user_id} in {lang}")
        
        return ChatResponse(
            reply=reply,
            sentiment=sentiment_label,
            language=lang,
            conversation_history=formatted_history
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/send_message")
async def api_send_message(request: Request):
    """
    API endpoint to receive voice input messages from frontend voice.html,
    process them similarly to /chat, and return a JSON response.
    """
    try:
        data = await request.json()
        message_text = data.get("message", "").strip()
        
        if not message_text:
            return {"error": "Message text cannot be empty"}
        
        # For voice input, we can use a fixed user_id or generate one
        user_id = "voice_user"
        
        # Detect language
        detected_lang = detect_language(message_text)
        
        # Use stored user language preference if exists, else store detected language
        lang = user_language_preference.get(user_id)
        if lang:
            pass
        else:
            user_language_preference[user_id] = detected_lang
            lang = detected_lang
        
        # Analyze sentiment
        sentiment_label, sentiment_score = analyze_sentiment(message_text)
        
        # Initialize conversation history for user if not present
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Get last bot message for context
        last_bot_message = None
        for entry in reversed(conversation_history[user_id]):
            if entry["role"] == "bot":
                last_bot_message = entry["text"]
                break
        
        # Simple dialogue flow management
        if last_bot_message and "sorry to hear that" in last_bot_message.lower():
            if any(keyword in message_text.lower() for keyword in ["because", "due to", "reason"]):
                reply = "Thank you for sharing. Remember, it's okay to feel this way. Would you like some suggestions to help you feel better?"
            else:
                reply = "Would you like to tell me more about what's bothering you? I'm here to listen."
        else:
            # Prepare messages for Cohere chat
            messages = [{"role": entry["role"], "text": entry["text"]} 
                       for entry in conversation_history.get(user_id, [])]
            
            # Translate user input to English for model if needed
            input_for_model = message_text
            if lang != "en":
                input_for_model = translate_text(message_text, "en")
            
            # Replace last user message with translated input if applicable
            if messages and messages[-1]["role"] == "user":
                messages[-1]["text"] = input_for_model
            else:
                messages.append({"role": "user", "text": input_for_model})
            
            # Get response from Cohere (now with language parameter)
            reply_generated = get_gemini_response(message_text, user_mood="neutral")
            
            # Add empathetic prefix based on sentiment (now with user_text parameter)
            empathetic_prefix = generate_empathetic_response(sentiment_label, lang, message_text)
            
            # Combine empathetic prefix with generated response
            # Translate reply back to user's language if needed
            if lang != "en":
                reply_generated = translate_text(reply_generated, lang)
            reply = empathetic_prefix + reply_generated

        # Clean reply string from unwanted formatting like type='text' text=
        import re
        reply = re.sub(r'type=[\'"]text[\'"]\s*text=[\'"]([^\'"]*)[\'"]', r'\1', reply)
        
        # Update conversation history
        conversation_history[user_id].append({"role": "user", "text": message_text})
        conversation_history[user_id].append({"role": "bot", "text": reply})
        
        # Limit conversation history to last 20 messages to prevent memory issues
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
        # Format conversation history for response
        formatted_history = []
        for entry in conversation_history[user_id]:
            if entry["role"] == "user":
                formatted_history.append({"user": entry["text"]})
            else:
                formatted_history.append({"bot": entry["text"]})
        
        logger.info(f"Successfully processed voice message in {lang}")
        
        return {"response": reply, "sentiment": sentiment_label, "language": lang, "conversation_history": formatted_history}
    
    except Exception as e:
        logger.error(f"Error processing voice message: {e}")
        return {"error": "Internal server error"}

@app.delete("/chat/{user_id}/history")
async def clear_history(user_id: str):
    """Clear conversation history for a specific user."""
    if user_id in conversation_history:
        del conversation_history[user_id]
        return {"message": f"Conversation history cleared for user {user_id}"}
    else:
        return {"message": f"No conversation history found for user {user_id}"}

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=True  # Remove in production
    )
