import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import google.generativeai as genai
import random
from datetime import datetime
import sys
import time

class ImprovedNivaVoiceAssistant:
    def __init__(self):
        # Initialize basic components
        self.recognizer = sr.Recognizer()
        self.conversation_active = True
        self.initial_mood_detected = False
        self.user_mood = 'neutral'
        
        # Custom songs for each mood - ADD YOUR LINKS HERE
        self.mood_songs = {
            'happy':[
                  "https://youtu.be/WxtJqyIyThU?si=tcmkGVgf7Cp3Fcha",
                   "https://youtu.be/6vKucgAeF_Q?si=I75PzT9On7yS6DYA",
                   "https://youtu.be/jCEdTq3j-0U?si=tJf3VaLb6As1U88c",
                   "https://youtu.be/ZbZSe6N_BXs?si=8WW06L4obM_piCL8",
                   "https://youtu.be/lrIKt5uDWZo?si=QIyCfNzHxF07o-5O"   # Replace with your happy song 5
            ],
            'sad': [
                "https://www.youtube.com/watch?v=SONG1_ID",  # Replace with your sad song 1
                "https://www.youtube.com/watch?v=SONG2_ID",  # Replace with your sad song 2
                "https://www.youtube.com/watch?v=SONG3_ID",  # Replace with your sad song 3
                "https://www.youtube.com/watch?v=SONG4_ID",  # Replace with your sad song 4
                "https://www.youtube.com/watch?v=SONG5_ID"   # Replace with your sad song 5
            ],
            'angry': [
                "https://www.youtube.com/watch?v=SONG1_ID",  # Replace with your angry song 1
                "https://www.youtube.com/watch?v=SONG2_ID",  # Replace with your angry song 2
                "https://www.youtube.com/watch?v=SONG3_ID",  # Replace with your angry song 3
                "https://www.youtube.com/watch?v=SONG4_ID",  # Replace with your angry song 4
                "https://www.youtube.com/watch?v=SONG5_ID"   # Replace with your angry song 5
            ],
            'worried': [
                "https://www.youtube.com/watch?v=SONG1_ID",  # Replace with your worried song 1
                "https://www.youtube.com/watch?v=SONG2_ID",  # Replace with your worried song 2
                "https://www.youtube.com/watch?v=SONG3_ID",  # Replace with your worried song 3
                "https://www.youtube.com/watch?v=SONG4_ID",  # Replace with your worried song 4
                "https://www.youtube.com/watch?v=SONG5_ID"   # Replace with your worried song 5
            ],
            'tired': [
                "https://www.youtube.com/watch?v=SONG1_ID",  # Replace with your tired song 1
                "https://www.youtube.com/watch?v=SONG2_ID",  # Replace with your tired song 2
                "https://www.youtube.com/watch?v=SONG3_ID",  # Replace with your tired song 3
                "https://www.youtube.com/watch?v=SONG4_ID",  # Replace with your tired song 4
                "https://www.youtube.com/watch?v=SONG5_ID"   # Replace with your tired song 5
            ],
            'confused': [
                "https://www.youtube.com/watch?v=SONG1_ID",  # Replace with your confused song 1
                "https://www.youtube.com/watch?v=SONG2_ID",  # Replace with your confused song 2
                "https://www.youtube.com/watch?v=SONG3_ID",  # Replace with your confused song 3
                "https://www.youtube.com/watch?v=SONG4_ID",  # Replace with your confused song 4
                "https://www.youtube.com/watch?v=SONG5_ID"   # Replace with your confused song 5
            ],
            'neutral': [
                "https://www.youtube.com/watch?v=SONG1_ID",  # Replace with your neutral song 1
                "https://www.youtube.com/watch?v=SONG2_ID",  # Replace with your neutral song 2
                "https://www.youtube.com/watch?v=SONG3_ID",  # Replace with your neutral song 3
                "https://www.youtube.com/watch?v=SONG4_ID",  # Replace with your neutral song 4
                "https://www.youtube.com/watch?v=SONG5_ID"   # Replace with your neutral song 5
            ]
        }
        
        # Initialize TTS with Windows Narrator style female voice
        self._setup_narrator_voice()
        
        # Initialize Gemini AI
        self._initialize_gemini_ai()
        
        print("🎤 Niva Voice Assistant Ready with Female Voice!")
        print("🎵 Custom songs loaded for each mood!")
        print("Say something to start...")
    
    def _setup_narrator_voice(self):
        """Setup Windows Narrator style female voice"""
        self.engine = None
        self.voice_working = False
        
        print("🔧 Setting up Windows Narrator style voice...")
        
        try:
            # Initialize Windows SAPI5 engine specifically
            self.engine = pyttsx3.init('sapi5')
            
            if self.engine:
                voices = self.engine.getProperty("voices")
                
                if voices:
                    print("🔍 Available voices:")
                    female_voice_found = False
                    
                    # Look for female voices (priority order)
                    female_voice_names = [
                        'zira',           # Microsoft Zira (Female)
                        'hazel',          # Microsoft Hazel (Female) 
                        'helen',          # Microsoft Helen (Female)
                        'susan',          # Microsoft Susan (Female)
                        'female',         # Any voice with 'female' in name
                        'woman',          # Any voice with 'woman' in name
                    ]
                    
                    # First try to find specific female voices
                    for voice in voices:
                        voice_name = voice.name.lower()
                        print(f"  - {voice.name} (ID: {voice.id})")
                        
                        # Check for female voice names
                        for female_name in female_voice_names:
                            if female_name in voice_name:
                                self.engine.setProperty('voice', voice.id)
                                print(f"✅ Selected female voice: {voice.name}")
                                female_voice_found = True
                                break
                        
                        if female_voice_found:
                            break
                    
                    # If no specific female voice found, try to use second voice (often female)
                    if not female_voice_found and len(voices) > 1:
                        self.engine.setProperty('voice', voices[1].id)
                        print(f"✅ Using alternate voice: {voices[1].name}")
                    elif not female_voice_found:
                        # Use default voice
                        print("⚠️ Using default voice (no female voice found)")
                    
                    # Configure voice settings for Windows Narrator style
                    self.engine.setProperty('rate', 180)      # Medium speed like Narrator
                    self.engine.setProperty('volume', 0.9)    # Clear volume
                    
                    # Test the voice
                    try:
                        print("🧪 Testing female voice...")
                        self.engine.say("Hello, I am Niva, your voice assistant with female voice")
                        self.engine.runAndWait()
                        time.sleep(0.3)
                        self.voice_working = True
                        print("✅ Female voice test successful!")
                        
                    except Exception as e:
                        print(f"❌ Voice test failed: {e}")
                        self.voice_working = False
                
            else:
                print("❌ Could not initialize SAPI5 engine")
                
        except Exception as e:
            print(f"❌ Windows Narrator voice setup failed: {e}")
            print("💡 Trying fallback voice setup...")
            
            # Fallback to any available TTS
            try:
                self.engine = pyttsx3.init()
                if self.engine:
                    voices = self.engine.getProperty("voices")
                    if voices and len(voices) > 1:
                        # Try second voice which is often female
                        self.engine.setProperty('voice', voices[1].id)
                        self.engine.setProperty('rate', 180)
                        self.engine.setProperty('volume', 0.9)
                        
                        self.engine.say("Fallback female voice activated")
                        self.engine.runAndWait()
                        self.voice_working = True
                        print("✅ Fallback voice working")
                    
            except Exception as fallback_error:
                print(f"❌ Fallback also failed: {fallback_error}")
                self.voice_working = False
        
        if not self.voice_working:
            print("⚠️ Voice engine setup failed. Using text-only mode.")
            print("💡 Make sure Windows Speech Platform is installed")
            print("💡 Try: Windows Settings > Time & Language > Speech")
    
    def _initialize_gemini_ai(self):
        """Initialize Gemini AI with better error handling"""
        try:
            genai.configure(api_key="your key")
            
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "max_output_tokens": 100,  # Shorter responses for voice
            }
            
            self.gemini_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                generation_config=generation_config
            )
            
            print("✅ Gemini AI ready")
            
        except Exception as e:
            print(f"⚠️ Gemini AI error: {e}")
            self.gemini_model = None
    
    def speak(self, text):
        """Enhanced speak function with Windows Narrator style"""
        print(f"🗣️ Niva (Female): {text}")
        
        if self.voice_working and self.engine:
            try:
                # Clean text for better speech (remove emojis and special chars)
                clean_text = text.replace('*', '').replace('_', '').replace('#', '')
                clean_text = clean_text.replace('🎵', '').replace('✨', '').replace('❤️', '')
                clean_text = clean_text.replace('🗣️', '').replace('🎤', '').replace('🤖', '')
                clean_text = clean_text.replace('🔧', '').replace('✅', '').replace('⚠️', '')
                
                # Stop any previous speech
                self.engine.stop()
                
                # Speak with Windows Narrator style timing
                self.engine.say(clean_text)
                self.engine.runAndWait()
                
                # Narrator style pause between sentences
                time.sleep(0.3)
                
            except Exception as e:
                print(f"❌ Speech error: {e}")
                print("⚠️ Continuing in text mode...")
                self.voice_working = False
                print("💡 Try restarting the program or check Windows Speech settings")
        else:
            print("📝 (Text mode - female voice not available)")
            # Ask user to press Enter to continue
            input("Press Enter to continue...")
    
    def listen(self):
        """Enhanced listen function with better Hindi-English recognition"""
        r = sr.Recognizer()
        
        # Improved microphone settings for Windows
        r.energy_threshold = 2500  # Adjusted for Windows
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.2     # Slightly longer pause
        r.phrase_threshold = 0.3
        r.non_speaking_duration = 0.8
        
        with sr.Microphone() as source:
            print("🎤 Listening... (Female voice ready)")
            
            try:
                # Adjust for ambient noise
                print("🔧 Adjusting for background noise...")
                r.adjust_for_ambient_noise(source, duration=1.0)
                
                # Listen with improved settings
                audio = r.listen(source, timeout=15, phrase_time_limit=10)
                print("🧠 Processing speech...")
                
                # Multi-language recognition attempts
                recognition_attempts = [
                    ('hi-IN', 'Hindi'),
                    ('en-IN', 'English (India)'),
                    ('en-US', 'English (US)'),
                    ('hi', 'Hindi Simple')
                ]
                
                for lang_code, lang_name in recognition_attempts:
                    try:
                        query = r.recognize_google(audio, language=lang_code)
                        if query:
                            print(f"👤 You ({lang_name}): {query}")
                            return query.lower().strip()
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        print(f"❌ Recognition service error: {e}")
                        continue
                
                print("❌ Could not understand audio")
                return None
                
            except sr.WaitTimeoutError:
                print("⏰ Listening timeout")
                return "timeout"
            except Exception as e:
                print(f"❌ Listen error: {e}")
                return None
    
    def detect_initial_mood(self, text):
        """Enhanced mood detection for Hindi and English"""
        if not text:
            return 'neutral'
            
        text_lower = text.lower()
        
        # Enhanced mood keywords (Hindi + English)
        mood_keywords = {
            'happy': ['happy', 'good', 'great', 'khush', 'acha', 'badhiya', 'excited', 
                     'amazing', 'fantastic', 'wonderful', 'awesome', 'achha', 'mazedaar', 'खुश', 'अच्छा'],
            'sad': ['sad', 'upset', 'down', 'dukhi', 'pareshan', 'hurt', 'crying', 
                   'depressed', 'low', 'udaas', 'gam', 'dard', 'दुखी', 'परेशान'],
            'angry': ['angry', 'mad', 'frustrated', 'gussa', 'naraz', 'irritated', 
                     'annoyed', 'gussey', 'pareshaan', 'गुस्सा', 'नाराज़'],
            'worried': ['worried', 'anxious', 'tension', 'stress', 'chinta', 'dar', 
                       'nervous', 'scared', 'bharti', 'pareshani', 'चिंता', 'टेंशन'],
            'tired': ['tired', 'thak', 'exhausted', 'bore', 'sleepy', 'lazy', 
                     'thaka', 'neend', 'aalas', 'थक', 'नींद'],
            'confused': ['confused', 'samajh', 'pata', 'nahin', 'kya', 'kuch', 
                        'understand', 'confuse', 'samjha', 'समझ', 'पता', 'नहीं']
        }
        
        for mood, keywords in mood_keywords.items():
            if any(word in text_lower for word in keywords):
                return mood
        
        return 'neutral'
    
    def is_goodbye(self, text):
        """Enhanced goodbye detection"""
        if not text:
            return False
        text_lower = text.lower()
        goodbye_words = ['goodbye', 'bye', 'exit', 'quit', 'stop', 'alvida', 
                        'band karo', 'bas karo', 'tata', 'see you', 'chalo bye',
                        'good bye', 'gude bye', 'bai', 'baai', 'बाई', 'अलविदा', 
                        'बंद करो', 'बस करो', 'गुड बाई']
        return any(word in text_lower for word in goodbye_words)
    
    def is_music_choice(self, text):
        """Enhanced music detection"""
        if not text:
            return False
        text_lower = text.lower()
        music_words = ['music', 'song', 'gaana', 'bajao', 'sunao', 'play', 
                      'youtube', 'sangeet', 'gana', 'gane', 'muzik', 'संगीत', 
                      'गाना', 'गाने', 'बजाओ', 'सुनाओ', 'music sunao', 'गाना सुनना']
        return any(word in text_lower for word in music_words)
    
    def is_talk_choice(self, text):
        """Enhanced talk detection"""
        if not text:
            return False
        text_lower = text.lower()
        talk_words = ['talk', 'chat', 'baat', 'conversation', 'discuss', 'share', 
                     'tell', 'speak', 'converse', 'baatcheet', 'charcha', 'kehna',
                     'बात', 'बात करना', 'बात करनी है', 'बातचीत', 'चर्चा', 'conversation',
                     'बात करते हैं', 'बात करना चाहते हैं', 'बात करना चाहिए', 'talk करना',
                     'हैव ए कन्वरसेशन', 'कन्वरसेशन', 'बात करनी', 'चैट']
        
        # Also check for phrases that indicate wanting to talk
        talk_phrases = ['बात करनी है', 'बात करना है', 'बात करते हैं', 'चर्चा करते हैं',
                       'बातचीत करते हैं', 'talk करना है', 'conversation करना है']
        
        # Check individual words
        if any(word in text_lower for word in talk_words):
            return True
            
        # Check phrases
        if any(phrase in text_lower for phrase in talk_phrases):
            return True
            
        return False
    
    def open_youtube_music(self):
        """Open YouTube with custom mood-based songs"""
        try:
            # Get songs for current mood
            mood_songs = self.mood_songs.get(self.user_mood, self.mood_songs['neutral'])
            
            # Check if songs are properly configured
            configured_songs = [song for song in mood_songs if 'SONG' not in song]
            
            if configured_songs:
                # Pick a random song from configured songs
                selected_song = random.choice(configured_songs)
                print(f"🎵 Playing custom {self.user_mood} song: {selected_song}")
                webbrowser.open(selected_song)
                self.speak(f"Playing a perfect song for your {self.user_mood} mood! Enjoy the music, honey!")
                return True
            else:
                # Fallback to search if no custom songs configured
                print(f"⚠️ No custom songs configured for {self.user_mood} mood, using search fallback")
                return self._fallback_music_search()
                
        except Exception as e:
            print(f"❌ Custom music error: {e}")
            return self._fallback_music_search()
    
    def _fallback_music_search(self):
        """Fallback music search when custom songs aren't configured"""
        music_for_mood = {
            'happy': 'happy bollywood songs 2024',
            'sad': 'sad hindi songs emotional',
            'angry': 'energetic rock hindi music',
            'worried': 'calming peaceful hindi music',
            'tired': 'relaxing bollywood lofi songs',
            'confused': 'motivational hindi songs',
            'neutral': 'latest hindi hits 2024'
        }
        
        search_query = music_for_mood.get(self.user_mood, 'popular hindi songs')
        youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        
        try:
            webbrowser.open(youtube_url)
            self.speak(f"Opening YouTube with {search_query} for you! Please configure your custom songs, dear!")
            return True
        except Exception as e:
            print(f"❌ Browser error: {e}")
            self.speak("Sorry, couldn't open music. Please check your browser, honey.")
            return False
    
    def generate_talk_response(self, user_input):
        """Generate English responses for Hindi/English input"""
        try:
            if not self.gemini_model:
                return self._get_fallback_response(user_input)
            
            # Enhanced prompt for better English responses
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

Current mood context: {self.user_mood}

Respond in clear English with a warm, feminine tone:"""

            response = self.gemini_model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return self._get_fallback_response(user_input)
                
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return self._get_fallback_response(user_input)
    
    def _get_fallback_response(self, user_input):
        """Smart fallback responses with feminine touch"""
        if not user_input:
            return "I'm here listening, sweetie. Please tell me what's on your mind."
        
        input_lower = user_input.lower()
        
        # Smart responses based on detected mood and keywords with feminine touch
        if self.user_mood == 'confused' or any(word in input_lower for word in ['samajh', 'pata', 'nahin', 'kya', 'confused']):
            responses = [
                "Don't worry honey, it's okay to feel confused sometimes. What's bothering you?",
                "Let's figure this out together, dear. What exactly is confusing you?",
                "Take your time, sweetie. What would you like to talk about?",
                "I'm here to help you through this. Can you tell me what's on your mind?"
            ]
        elif self.user_mood == 'sad':
            responses = [
                "I can hear you're feeling down, dear. Would you like to share what's troubling you?",
                "It's perfectly okay to feel sad sometimes, honey. I'm here to listen.",
                "You don't have to go through this alone, sweetie. Tell me more.",
                "I'm here for you. What's making you feel this way?"
            ]
        elif self.user_mood == 'happy':
            responses = [
                "That's wonderful, dear! Tell me more about what's making you so happy.",
                "I love hearing your positive energy! What's going on?",
                "That sounds amazing, honey! Can you share more details?",
                "Your happiness is contagious! What's the good news?"
            ]
        else:
            responses = [
                "That's interesting, dear. Can you tell me more?",
                "I'm listening carefully, honey. What else is on your mind?",
                "Thanks for sharing that with me, sweetie. How are you feeling about it?",
                "I hear you, dear. What would you like to discuss?",
                "Tell me more about what you're thinking, honey."
            ]
        
        return random.choice(responses)
    
    def run(self):
        """Main assistant loop with female voice personality"""
        print("\n🚀 Niva is ready to chat with her female voice...")
        print("🎵 Custom songs loaded for each mood!")
        print("💡 Don't forget to add your YouTube song links in the code!")
        
        # Step 1: Get initial input and detect mood
        while not self.initial_mood_detected:
            first_input = self.listen()
            
            if first_input == "timeout":
                self.speak("I'm still here, dear! Say something to get started.")
                continue
            elif not first_input:
                self.speak("I didn't catch that, honey. Could you please say something?")
                continue
            elif self.is_goodbye(first_input):
                self.speak("Goodbye, dear! Have a wonderful day!")
                return
            
            # Detect mood
            self.user_mood = self.detect_initial_mood(first_input)
            self.initial_mood_detected = True
            
            print(f"🎭 Detected mood: {self.user_mood}")
            
            # Ask for preference with feminine touch
            self.speak("Hi there! I'm Niva, your friendly voice assistant. Would you like to listen to some music or have a nice conversation with me? Music ya baat karna chahiye?")
            break
        
        # Step 2: Handle user choice with better logic
        choice_made = False
        attempts = 0
        max_attempts = 5
        
        while not choice_made and self.conversation_active and attempts < max_attempts:
            user_choice = self.listen()
            attempts += 1
            
            if user_choice == "timeout":
                self.speak("Would you like music or a conversation, dear? Music ya baat?")
                continue
            elif not user_choice:
                self.speak("I didn't hear you clearly, honey. Say music for songs or baat for talking.")
                continue
            elif self.is_goodbye(user_choice):
                self.speak("It was lovely meeting you! Take care, dear!")
                return
            elif self.is_music_choice(user_choice):
                # Music mode
                print("🎵 User chose music")
                if self.open_youtube_music():
                    self.speak("Enjoy your music, honey! Say goodbye when you want to stop.")
                    while True:
                        music_input = self.listen()
                        if music_input and self.is_goodbye(music_input):
                            self.speak("Thanks for spending time with me! Goodbye, dear!")
                            return
                        elif music_input == "timeout":
                            continue
                        else:
                            self.speak("I'm playing music for you, honey. Say goodbye when you're done!")
                choice_made = True
            elif self.is_talk_choice(user_choice):
                # Conversation mode
                print("💬 User chose conversation")
                self.speak("Wonderful! I'm here to chat with you, dear. What's on your mind?")
                
                while self.conversation_active:
                    talk_input = self.listen()
                    
                    if talk_input == "timeout":
                        self.speak("I'm still listening, sweetie. What would you like to talk about?")
                        continue
                    elif not talk_input:
                        self.speak("I didn't catch that, honey. Could you repeat?")
                        continue
                    elif self.is_goodbye(talk_input):
                        self.speak("It was wonderful talking with you, dear! Take care!")
                        return
                    else:
                        # Generate English response with feminine personality
                        response = self.generate_talk_response(talk_input)
                        self.speak(response)
                choice_made = True
            else:
                # Unclear choice - provide clearer options
                if attempts < 3:
                    self.speak("Please say music for songs or baat for conversation, dear. Clear words please.")
                else:
                    self.speak("Let me start conversation mode since I'm not sure what you want, honey.")
                    print("💬 Defaulting to conversation mode")
                    self.speak("I'm here to chat with you, sweetie. What's on your mind?")
                    
                    while self.conversation_active:
                        talk_input = self.listen()
                        
                        if talk_input == "timeout":
                            self.speak("I'm still listening, dear. What would you like to talk about?")
                            continue
                        elif not talk_input:
                            self.speak("I didn't catch that, honey. Could you repeat?")
                            continue
                        elif self.is_goodbye(talk_input):
                            self.speak("It was wonderful talking with you, dear! Take care!")
                            return
                        else:
                            response = self.generate_talk_response(talk_input)
                            self.speak(response)
                    choice_made = True
        
        if attempts >= max_attempts and not choice_made:
            self.speak("Starting conversation mode, dear. What would you like to talk about?")
        
        print("👋 Niva Assistant stopped!")

def main():
    """Start the improved assistant with Windows female voice"""
    try:
        print("🤖 Starting Niva Voice Assistant with Female Voice...")
        print("🎵 Custom songs feature enabled!")
        print("🔧 Checking system compatibility...")
        
        # Quick system check
        try:
            import speech_recognition as sr
            import pyttsx3
            print("✅ All required libraries found")
        except ImportError as e:
            print(f"❌ Missing library: {e}")
            print("Please install: pip install speechrecognition pyttsx3 google-generativeai")
            print("Also try: pip install pyaudio")
            return
        
        # Check microphone
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("✅ Microphone detected")
        except Exception as e:
            print(f"⚠️ Microphone issue: {e}")
            print("Please check your microphone connection")
        
        print("🎀 Initializing female voice assistant...")
        assistant = ImprovedNivaVoiceAssistant()
        assistant.run()
        
    except KeyboardInterrupt:
        print("\n👋 Assistant stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please check your microphone and internet connection")
        print("Try running as administrator if on Windows")
        print("💡 For female voice issues, check Windows Speech settings")

if __name__ == "__main__":
    main()
