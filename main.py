import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import time
import platform
import tempfile
import re
import uuid
import io
import getpass
from datetime import datetime

class ATMVoiceAssistant:
    def __init__(self):
        # Initialize speech recognition with improved settings
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300  # Lower energy threshold for better detection
        self.recognizer.dynamic_energy_threshold = True
        self.language = None  # Will be set during language selection
        self.use_voice_agent = None  # Will be set during initial prompt
        
        # Dictionary for multilingual support (English and Hindi)
        self.messages = {
            "en": {
                "welcome": "Welcome to our ATM service.",
                "agent_selection": "Would you like to use our voice assistant? Say yes to use voice assistance or no to continue without it.",
                "language_selection": "Please select your preferred language. Say 1 for English, 2 for Hindi.",
                "card_prompt": "Please insert your card.",
                "main_menu": "Main Menu: Say 1 for withdrawal, 2 for balance check, 3 for PIN change, 4 for mini-statement, 5 for fund transfer, 6 for help, or 7 to exit.",
                "card_inserted": "Card has been detected.",
                "pin_prompt": "For security purposes, please enter your 4-digit PIN using the keyboard.",
                "pin_error": "Incorrect PIN. Please try again.",
                "pin_accepted": "PIN accepted. You can now access the main menu.",
                "withdraw_prompt": "For security purposes, please enter the amount you wish to withdraw using the keyboard.",
                "processing": "Processing your transaction. Please wait.",
                "cash_dispensed": "Please collect your cash and your receipt is being printed.",
                "receipt": "Would you like to print a receipt? Say yes or no.",
                "receipt_printed": "Receipt has been printed. Thank you for using our ATM.",
                "balance_check": "Your balance information has been displayed on screen.",  # Modified to not announce amount
                "help_prompt": "For assistance, please say the number of your choice: 1 for PIN help, 2 for transaction help, 3 to return to the main menu.",
                "timeout": "I didn't hear anything. Please try again.",
                "cancel_confirmed": "Transaction cancelled. Thank you for using our ATM.",
                "goodbye": "Thank you for using our ATM. Have a nice day!",
                "transaction_menu": "Transaction Menu: Say 1 for cash withdrawal, 2 for balance check, 3 for PIN change, 4 for mini-statement, 5 for fund transfer, 6 for help, 7 to exit.",
                "pin_help": "PIN Help: Please enter your 4-digit PIN when prompted using the keypad for security.",
                "transaction_help": "Transaction Help: After entering your PIN, you can choose various options like withdraw cash, check balance, etc.",
                "pin_change_prompt": "Please enter your new 4-digit PIN using the keyboard.",
                "pin_changed": "Your PIN has been changed successfully.",
                "mini_statement": "Your mini statement is displayed on screen.",  # Modified to not read transactions
                "transfer_prompt": "Please enter the account number you wish to transfer to:",
                "transfer_amount_prompt": "Please enter the amount you wish to transfer:",
                "transfer_successful": "Cash is transferred.",  # Modified to not include details
                "transfer_failed": "Transfer failed. Please check account details and try again.",
                "custom": "{message}"
            },
            "hi": {
                "welcome": "हमारे एटीएम सेवा में आपका स्वागत है।",
                "agent_selection": "क्या आप हमारे वॉयस असिस्टेंट का उपयोग करना चाहेंगे? वॉयस सहायता का उपयोग करने के लिए हां कहें या बिना इसके जारी रखने के लिए नहीं कहें।",
                "language_selection": "कृपया अपनी पसंदीदा भाषा चुनें। अंग्रेजी के लिए 1 बोलें, हिंदी के लिए 2 बोलें।",
                "card_prompt": "कृपया अपना कार्ड डालें।",
                "main_menu": "मुख्य मेनू: पैसे निकालने के लिए 1, बैलेंस जांचने के लिए 2, पिन बदलने के लिए 3, मिनी-स्टेटमेंट के लिए 4, फंड ट्रांसफर के लिए 5, मदद के लिए 6, या बाहर निकलने के लिए 7 बोलें।",
                "card_inserted": "कार्ड मिल गया है।",
                "pin_prompt": "सुरक्षा कारणों से, कृपया कीबोर्ड का उपयोग करके अपना 4 अंकों का पिन दर्ज करें।",
                "pin_error": "पिन गलत है। कृपया दोबारा कोशिश करें।",
                "pin_accepted": "पिन सही है। अब आप मुख्य मेनू का उपयोग कर सकते हैं।",
                "withdraw_prompt": "सुरक्षा कारणों से, कृपया कीबोर्ड का उपयोग करके निकालने के लिए राशि दर्ज करें।",
                "processing": "आपका लेनदेन हो रहा है। कृपया प्रतीक्षा करें।",
                "cash_dispensed": "कृपया अपने पैसे लें और आपकी रसीद प्रिंट हो रही है।",
                "receipt": "क्या आप रसीद प्रिंट करना चाहेंगे? हां या नहीं कहें।",
                "receipt_printed": "रसीद प्रिंट हो गई है। हमारे एटीएम का उपयोग करने के लिए धन्यवाद।",
                "balance_check": "आपका बैलेंस जानकारी स्क्रीन पर दिखाई गई है।",  # Modified to not announce amount
                "help_prompt": "सहायता के लिए, अपनी पसंद का नंबर बोलें: पिन सहायता के लिए 1, लेनदेन सहायता के लिए 2, मुख्य मेनू पर लौटने के लिए 3।",
                "timeout": "मैंने कुछ नहीं सुना। कृपया फिर से प्रयास करें।",
                "cancel_confirmed": "लेनदेन रद्द कर दिया गया है। हमारे एटीएम का उपयोग करने के लिए धन्यवाद।",
                "goodbye": "हमारे एटीएम का उपयोग करने के लिए धन्यवाद। आपका दिन शुभ हो!",
                "transaction_menu": "लेनदेन मेनू: पैसे निकालने के लिए 1, बैलेंस जांचने के लिए 2, पिन बदलने के लिए 3, मिनी-स्टेटमेंट के लिए 4, फंड ट्रांसफर के लिए 5, मदद के लिए 6, बाहर निकलने के लिए 7 बोलें।",
                "pin_help": "पिन सहायता: सुरक्षा कारणों से, कृपया प्रॉम्प्ट किए जाने पर कीपैड का उपयोग करके अपना 4 अंकों का पिन दर्ज करें।",
                "transaction_help": "लेनदेन सहायता: पिन दर्ज करने के बाद, आप पैसे निकालने, बैलेंस देखने आदि विभिन्न विकल्पों का चयन कर सकते हैं।",
                "pin_change_prompt": "कृपया कीबोर्ड का उपयोग करके अपना नया 4 अंकों का पिन दर्ज करें।",
                "pin_changed": "आपका पिन सफलतापूर्वक बदल दिया गया है।",
                "mini_statement": "आपका मिनी स्टेटमेंट स्क्रीन पर दिखाया गया है।",  # Modified to not read transactions
                "transfer_prompt": "कृपया वह खाता संख्या दर्ज करें जिसे आप स्थानांतरित करना चाहते हैं:",
                "transfer_amount_prompt": "कृपया वह राशि दर्ज करें जिसे आप स्थानांतरित करना चाहते हैं:",
                "transfer_successful": "पैसा ट्रांसफर कर दिया गया है।",  # Modified to not include details
                "transfer_failed": "स्थानांतरण विफल। कृपया खाता विवरण जांचें और पुनः प्रयास करें।",
                "custom": "{message}"
            }
        }
        
        self.current_state = "welcome"
        self.card_detected = False
        self.pin_correct = False
        self.withdrawal_amount = 0
        self.account_balance = 25000
        self.attempts = 0
        
        # Demo transaction history
        self.transactions = [
            {"date": "2025-04-20", "type": "WITHDRAWAL", "amount": 5000},
            {"date": "2025-04-15", "type": "DEPOSIT", "amount": 10000},
            {"date": "2025-04-10", "type": "TRANSFER", "amount": 2500}
        ]
        
        # Create a user-specific directory for temp files
        self.temp_dir = os.path.join(tempfile.gettempdir(), f"atm_voice_{uuid.uuid4().hex}")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.system = platform.system()
        
        # Configure voices for better performance
        voices = self.tts_engine.getProperty('voices')
        # Find and set English voice
        for voice in voices:
            if "english" in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
    
    def speak_english(self, text):
        """Use pyttsx3 for English TTS"""
        try:
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            time.sleep(0.5)
        except Exception as e:
            print(f"English TTS Error: {e}")
            print(f"[SPOKEN-EN]: {text}")
    
    def speak_hindi(self, text):
        """Use gTTS for Hindi TTS with improved playback"""
        try:
            # Generate a unique filename for each speech file
            unique_filename = os.path.join(self.temp_dir, f"hindi_speech_{uuid.uuid4().hex}.mp3")
            
            # Generate TTS file
            tts = gTTS(text=text, lang='hi', slow=False)
            tts.save(unique_filename)
            
            print(f"Playing Hindi audio from: {unique_filename}")
            
            # Try to use pygame for playback
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(unique_filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except ImportError:
                # Fall back to playsound if pygame is not available
                try:
                    from playsound import playsound
                    playsound(unique_filename)
                except Exception as playback_error:
                    print(f"Playsound error: {playback_error}")
                    # Fall back to system commands if playsound fails
                    if self.system == "Windows":
                        os.system(f'start {unique_filename}')
                    elif self.system == "Darwin":  # macOS
                        os.system(f'afplay "{unique_filename}"')
                    else:  # Linux
                        os.system(f'mpg123 "{unique_filename}" || mpg321 "{unique_filename}" || play "{unique_filename}"')
            
            # Wait for audio to finish
            time.sleep(len(text) * 0.1)  # Slightly longer wait time
            
            # Clean up
            try:
                os.remove(unique_filename)
            except:
                pass
                
        except Exception as e:
            print(f"Hindi TTS Error: {e}")
            print(f"[SPOKEN-HI]: {text}")
            
            # Fallback: Try using pyttsx3 for Hindi
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
    
    def speak(self, message_key, **kwargs):
        """Text to speech output with language selection"""
        if not self.language and message_key in ["welcome", "agent_selection"]:
            # For welcome and agent selection, speak both languages
            eng_message = self.messages["en"][message_key].format(**kwargs)
            hindi_message = self.messages["hi"][message_key].format(**kwargs)
            
            print(f"ATM Assistant (English): {eng_message}")
            print(f"ATM Assistant (Hindi): {hindi_message}")
            
            # Speak English first, then Hindi
            self.speak_english(eng_message)
            time.sleep(0.3)  # Short pause between languages
            self.speak_hindi(hindi_message)
            
        elif self.language:
            # Speak in the selected language
            message = self.messages[self.language][message_key].format(**kwargs)
            print(f"ATM Assistant ({self.language}): {message}")
            
            if self.language == "en":
                self.speak_english(message)
            else:
                self.speak_hindi(message)
        else:
            # Default to Hindi if language not set (should not happen)
            message = self.messages["hi"][message_key].format(**kwargs)
            print(f"ATM Assistant (Default Hindi): {message}")
            self.speak_hindi(message)
    
    def listen(self):
        """Enhanced listening function with better recognition"""
        if not self.use_voice_agent:
            # If voice agent is disabled, get input via keyboard
            print("Please type your response: ")
            text = input().lower()
            print(f"User typed: {text}")
            return text
        
        # For specific operations, always use keyboard input
        if self.current_state in ["pin_entry", "withdraw_amount", "pin_change", "transfer_initiate"]:
            print("Please type your response: ")
            text = input().lower()
            print(f"User typed: {text}")
            return text
        
        print("Listening...")
        with sr.Microphone() as source:
            # Adjust for ambient noise with shorter duration for faster response
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Increase timeout and phrase time for better capture
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=10)
                
                # Implement parallel language recognition for better results
                text = None
                lang_options = ["en-IN", "hi-IN", "en-US", "en-GB"]
                
                # Try to recognize in multiple languages simultaneously
                for lang in lang_options:
                    try:
                        if not text:  # Only try if we haven't got a result yet
                            text = self.recognizer.recognize_google(audio, language=lang)
                            print(f"Recognized with {lang}: {text}")
                    except:
                        continue
                
                # If all language-specific attempts failed, try with default recognition
                if not text:
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print(f"Recognized with default: {text}")
                    except:
                        pass
                
                if text:
                    print(f"User said: {text}")
                    return text.lower()
                else:
                    print("Recognition failed")
                    self.speak("timeout")
                    return None
                    
            except sr.WaitTimeoutError:
                print("Timeout error - no speech detected")
                self.speak("timeout")
                return None
            except sr.UnknownValueError:
                print("Unknown value error - speech not understood")
                self.speak("timeout")
                return None
            except sr.RequestError as e:
                print(f"Request error: {e}")
                return None
    
    def get_pin_input(self):
        """Get PIN securely from keyboard input"""
        print("Enter your 4-digit PIN (input is hidden): ")
        pin = ""
        
        # For security, we'll try to use getpass if available
        try:
            pin = getpass.getpass(prompt="")
        except:
            # If getpass fails or is not available, fall back to regular input
            pin = input()
        
        return pin.strip()
    
    def get_amount_input(self):
        """Get withdrawal amount from keyboard input"""
        print("Enter the amount you wish to withdraw: ")
        try:
            amount = int(input().strip())
            return amount
        except ValueError:
            return None
    
    def get_account_input(self):
        """Get account number from keyboard input"""
        print("Enter the account number: ")
        try:
            account = input().strip()
            return account
        except:
            return None

    def extract_number_from_speech(self, text):
        """Enhanced number extraction from user speech"""
        if not text:
            return None
            
        # Extended dictionary with more variations for better recognition
        number_words = {
            "one": 1, "ek": 1, "एक": 1, "1": 1, "first": 1, "pehla": 1, "pahla": 1, "पहला": 1,
            "two": 2, "do": 2, "दो": 2, "2": 2, "second": 2, "doosra": 2, "दूसरा": 2,
            "three": 3, "teen": 3, "तीन": 3, "3": 3, "third": 3, "teesra": 3, "तीसरा": 3,
            "four": 4, "char": 4, "चार": 4, "4": 4, "fourth": 4, "chautha": 4, "चौथा": 4,
            "five": 5, "paanch": 5, "पांच": 5, "5": 5, "fifth": 5, "panchva": 5, "पांचवां": 5,
            "six": 6, "chhe": 6, "छे": 6, "6": 6, "sixth": 6, "chhatha": 6, "छठा": 6,
            "seven": 7, "saat": 7, "सात": 7, "7": 7, "seventh": 7, "satva": 7, "सातवां": 7
        }
        
        # Check for whole words that represent numbers
        words = text.lower().split()
        for word in words:
            if word in number_words:
                return number_words[word]
        
        # Check for numbers as parts of words
        for word, number in number_words.items():
            if word in text.lower():
                return number
                
        # Check for digits with improved regex
        digits = re.findall(r'\b\d+\b', text)
        if digits:
            try:
                return int(digits[0])
            except:
                pass
                
        return None

    def process_hinglish(self, text):
        """Enhanced command detection with broader keyword matching"""
        if not text:
            return text
        
        # Command mapping with primary and secondary keywords
        command_keywords = {
            "english": ["english", "angrezi", "inglis", "अंग्रेजी", "अंग्रेज़ी", "इंग्लिश", "first", "one", "1"],
            "hindi": ["hindi", "हिंदी", "हिन्दी", "second", "two", "2", "दो"],
            "withdraw": ["withdraw", "paise", "cash", "money", "amount", "withdraw money", "withdraw cash", 
                        "पैसे", "राशि", "निकालना", "कैश", "पैसा", "rupees", "rupay", "रुपये", "take", "get", 
                        "निकाल", "लेना", "raqam", "paisa"],
            "balance": ["balance", "baki", "check balance", "बैलेंस", "बाकी", "शेष", "कितना है", "how much", 
                        "kitna", "amount check", "inquiry", "चेक", "देखना", "जानना"],
            "yes": ["yes", "haan", "right", "correct", "ok", "okay", "sure", "हां", "हाँ", "ठीक है", 
                   "सही है", "हा", "ji", "जी", "yep", "yeah", "good"],
            "no": ["no", "nahi", "not", "wrong", "incorrect", "नहीं", "ना", "नही", "गलत", "नकारना", 
                  "cancel", "रद्द"],
            "help": ["help", "madad", "सहायता", "मदद", "हेल्प", "guide", "support", "assist", "सहायता करें"],
            "cancel": ["cancel", "rukjao", "stop", "back", "return", "कैंसिल", "रुकजाओ", "वापस", "रद्द", 
                      "रोकें", "नहीं", "no", "रुकना"],
            "card": ["card", "atm card", "कार्ड", "एटीएम कार्ड", "insert", "डालना", "डाल", "start", "शुरू", 
                    "begin", "card insert", "카드"],
            "exit": ["exit", "quit", "close", "बंद", "बाहर", "समाप्त", "end", "finish", "bye", "goodbye", 
                    "धन्यवाद", "thanks", "thank you"],
            "pin_change": ["pin change", "change pin", "new pin", "पिन बदलें", "नया पिन", "पिन बदलना"],
            "mini_statement": ["mini statement", "statement", "history", "transactions", "mini", "मिनी स्टेटमेंट", "लेनदेन", "इतिहास"],
            "transfer": ["transfer", "send money", "fund transfer", "ट्रांसफर", "भेजना", "पैसे भेजना", "स्थानांतरण"]
        }
        
        # Check for command matches with fuzzy matching
        for command, keywords in command_keywords.items():
            # Check for exact matches first
            for keyword in keywords:
                if keyword in text.lower().split():
                    return command
            
            # Then check for partial matches
            for keyword in keywords:
                if keyword in text.lower():
                    return command
                    
        return text
    
    def welcome_state(self):
        """Initial welcome message"""
        self.speak("welcome")
        self.current_state = "agent_selection"
        return True
    
    def agent_selection_state(self):
        """Ask user if they want to use voice assistant"""
        self.speak("agent_selection")
        
        # Try up to 3 times to get agent selection
        for attempt in range(3):
            # For initial prompt, always use voice recognition and typed input as fallback
            print("Please say 'yes' to use voice assistant or 'no' to continue without it.")
            print("Or type your response: ")
            
            # First try voice recognition
            with sr.Microphone() as source:
                try:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    user_input = self.recognizer.recognize_google(audio)
                    print(f"User said: {user_input}")
                except:
                    # If voice recognition fails, get keyboard input
                    user_input = input().lower()
                    print(f"User typed: {user_input}")
            
            if user_input:
                processed_input = self.process_hinglish(user_input)
                
                if processed_input == "yes" or "yes" in user_input.lower() or "yeah" in user_input.lower():
                    self.use_voice_agent = True
                    print("Voice assistant enabled")
                    break
                elif processed_input == "no" or "no" in user_input.lower() or "nahi" in user_input.lower():
                    self.use_voice_agent = False
                    print("Voice assistant disabled - using text input mode")
                    break
                else:
                    print(f"Selection unclear: '{user_input}'. Please say 'yes' or 'no'.")
                    if attempt < 2:
                        self.speak("agent_selection")
            else:
                print(f"No input received on attempt {attempt+1}")
                if attempt < 2:
                    self.speak("agent_selection")
        
        # Default to text input if no clear selection after attempts
        if self.use_voice_agent is None:
            self.use_voice_agent = False
            print("Defaulting to text input mode after multiple attempts")
        
        self.current_state = "language_selection"
        return True
    
    def language_selection_state(self):
        """Enhanced language selection with better detection"""
        self.speak("language_selection")
        
        # Try up to 3 times to get language selection
        for attempt in range(3):
            user_input = self.listen()
            
            if user_input:
                processed_input = self.process_hinglish(user_input)
                selection = self.extract_number_from_speech(user_input)
                
                # Check for explicit language mentions first
                if processed_input == "english" or selection == 1:
                    self.language = "en"
                    print("Language set to English")
                    break
                elif processed_input == "hindi" or selection == 2:
                    self.language = "hi"
                    print("Language set to Hindi")
                    break
                else:
                    print(f"Language selection unclear: '{user_input}'. Trying again...")
                    if attempt < 2:
                        self.speak("language_selection")
            else:
                print(f"No input received on attempt {attempt+1}")
                if attempt < 2:
                    self.speak("language_selection")
        
        # Default to English if no clear selection after attempts
        if not self.language:
            self.language = "en"
            print("Defaulting to English after multiple attempts")
        
        self.current_state = "card_prompt"
        return True
    
    def card_prompt_state(self):
        """Ask user to insert card"""
        self.speak("card_prompt")
        user_input = self.listen()
        
        if user_input:
            processed_input = self.process_hinglish(user_input)
            
            # Accept any input as card insertion
            self.card_detected = True
            self.current_state = "card_inserted"
        else:
            self.card_detected = True  # Auto-detect card for better user experience
            self.current_state = "card_inserted"
        
        return True
    
    def card_inserted_state(self):
        """Card inserted handling"""
        self.speak("card_inserted")
        self.current_state = "pin_entry"
        return True
    
    def pin_entry_state(self):
        """PIN entry with improved error handling - always uses keyboard"""
        self.speak("pin_prompt")
        
        # Get PIN from keyboard input (secure)
        pin = self.get_pin_input()
        
        if pin and len(pin) == 4 and pin.isdigit():
            print("PIN entered securely")
            if pin == "2341":  # Demo PIN
                self.pin_correct = True
                self.speak("pin_accepted")
                self.current_state = "main_menu"
            else:
                self.attempts += 1
                if self.attempts < 3:
                    self.speak("pin_error")
                else:
                    self.speak("custom", message="Too many attempts. Returning card." if self.language == "en" else "बहुत अधिक प्रयास। कार्ड वापस करना।")
                    self.card_detected = False
                    self.attempts = 0
                    self.current_state = "welcome"
        else:
            print("Invalid PIN format")
            self.speak("pin_error")
        
        return True
    
    def main_menu_state(self):
        """Enhanced main menu with improved command detection"""
        self.speak("main_menu")
        user_input = self.listen()
        
        if user_input:
            selection = self.extract_number_from_speech(user_input)
            processed_input = self.process_hinglish(user_input)
            
            # Extended keyword detection
            withdraw_keywords = ["withdraw", "cash", "money", "take", "get", "paise", "रुपए", "निकालना"]
            balance_keywords = ["balance", "check", "see", "how much", "kitna", "inquire", "बैलेंस", "जांच"]
            pin_change_keywords = ["pin change", "change pin", "new pin", "पिन बदलें", "नया पिन" , "change"]
            mini_statement_keywords = ["statement", "history", "mini", "transactions", "मिनी", "लेनदेन"]
            transfer_keywords = ["transfer", "send", "भेजना", "ट्रांसफर", "स्थानांतरण"]
            help_keywords = ["help", "support", "मदद", "सहायता"]
            exit_keywords = ["exit", "quit", "बाहर", "समाप्त", "निकलना" , "sath" , "bhar" , "nikalne "]
            
            if selection == 1 or processed_input == "withdraw" or any(keyword in user_input.lower() for keyword in withdraw_keywords):
                self.current_state = "withdraw_amount"
            elif selection == 2 or processed_input == "balance" or any(keyword in user_input.lower() for keyword in balance_keywords):
                self.current_state = "balance_check"
            elif selection == 3 or processed_input == "pin_change" or any(keyword in user_input.lower() for keyword in pin_change_keywords):
                self.current_state = "pin_change"
            elif selection == 4 or processed_input == "mini_statement" or any(keyword in user_input.lower() for keyword in mini_statement_keywords):
                self.current_state = "mini_statement"
            elif selection == 5 or processed_input == "transfer" or any(keyword in user_input.lower() for keyword in transfer_keywords):
                self.current_state = "transfer_initiate"
            elif selection == 6 or processed_input == "help" or any(keyword in user_input.lower() for keyword in help_keywords):
                self.current_state = "help_menu"
            elif selection == 7 or processed_input == "exit" or any(keyword in user_input.lower() for keyword in exit_keywords):
                self.current_state = "goodbye"
            else:
                self.speak("custom", message="Invalid selection. Please try again." if self.language == "en" else "अमान्य चयन। कृपया पुनः प्रयास करें।")
        else:
            self.speak("timeout")
        
        return True
    
    def withdraw_amount_state(self):
        """Withdraw money with enhanced security"""
        self.speak("withdraw_prompt")
        
        # Use keyboard for amount entry
        amount_input = self.get_amount_input()
        
        if amount_input and isinstance(amount_input, int):
            if amount_input > 0 and amount_input <= self.account_balance:
                self.withdrawal_amount = amount_input
                self.speak("processing")
                time.sleep(1)  # Simulate processing time
                
                # Update account balance
                self.account_balance -= self.withdrawal_amount
                
                # Add transaction to history
                self.transactions.insert(0, {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "type": "WITHDRAWAL",
                    "amount": self.withdrawal_amount
                })
                
                self.speak("cash_dispensed")
                time.sleep(1)
                
                # Ask for receipt
                self.speak("receipt")
                receipt_response = self.listen()
                
                if receipt_response and self.process_hinglish(receipt_response) == "yes":
                    self.speak("receipt_printed")
                
                self.current_state = "main_menu"
            else:
                self.speak("custom", message="Invalid amount or insufficient funds. Please try again." if self.language == "en" else "अमान्य राशि या अपर्याप्त धन। कृपया पुनः प्रयास करें।")
        else:
            self.speak("custom", message="Invalid amount. Please enter a valid number." if self.language == "en" else "अमान्य राशि। कृपया एक वैध संख्या दर्ज करें।")
        
        return True
    
    def balance_check_state(self):
        """Show account balance securely"""
        # For security, we don't speak the actual amount
        self.speak("balance_check")
        
        # Display balance on screen (simulated)
        print(f"\n{'=' * 40}")
        print(f"{'ACCOUNT BALANCE':^40}")
        print(f"{'=' * 40}")
        print(f"Current Balance: ₹{self.account_balance}")
        print(f"{'=' * 40}\n")
        
        time.sleep(1)  # Give user time to read
        self.current_state = "main_menu"
        return True
    
    def pin_change_state(self):
        """Change PIN securely"""
        self.speak("pin_change_prompt")
        
        # Get new PIN securely via keyboard
        new_pin = self.get_pin_input()
        
        if new_pin and len(new_pin) == 4 and new_pin.isdigit():
            self.speak("processing")
            time.sleep(1)  # Simulate processing
            
            # In a real app, this would update the PIN in a secure database
            self.speak("pin_changed")
            self.current_state = "main_menu"
        else:
            self.speak("custom", message="Invalid PIN format. Please try again." if self.language == "en" else "अमान्य पिन प्रारूप। कृपया पुनः प्रयास करें।")
        
        return True
    
    def mini_statement_state(self):
        """Show mini statement securely"""
        self.speak("mini_statement")
        
        # Display statement on screen (simulated)
        print(f"\n{'=' * 60}")
        print(f"{'MINI STATEMENT':^60}")
        print(f"{'=' * 60}")
        print(f"{'Date':<12}{'Type':<15}{'Amount':>15}")
        print(f"{'-' * 60}")
        
        # Show last 5 transactions
        for transaction in self.transactions[:5]:
            print(f"{transaction['date']:<12}{transaction['type']:<15}₹{transaction['amount']:>14}")
            
        print(f"{'=' * 60}")
        print(f"Current Balance: ₹{self.account_balance:>14}")
        print(f"{'=' * 60}\n")
        
        time.sleep(5)  # Give user time to read
        self.current_state = "main_menu"
        return True
    
    def transfer_initiate_state(self):
        """Initialize fund transfer process"""
        self.speak("transfer_prompt")
        
        # Get account number via keyboard
        account_number = self.get_account_input()
        
        if account_number and len(account_number) > 5:
            # Get transfer amount
            self.speak("transfer_amount_prompt")
            amount_input = self.get_amount_input()
            
            if amount_input and isinstance(amount_input, int):
                if amount_input > 0 and amount_input <= self.account_balance:
                    self.speak("processing")
                    time.sleep(1)  # Simulate processing
                    
                    # Update balance and record transaction
                    self.account_balance -= amount_input
                    self.transactions.insert(0, {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "TRANSFER",
                        "amount": amount_input
                    })
                    
                    self.speak("transfer_successful")
                    self.current_state = "main_menu"
                else:
                    self.speak("transfer_failed")
            else:
                self.speak("custom", message="Invalid amount. Please enter a valid number." if self.language == "en" else "अमान्य राशि। कृपया एक वैध संख्या दर्ज करें।")
        else:
            self.speak("transfer_failed")
        
        return True
    
    def help_menu_state(self):
        """Enhanced help menu"""
        self.speak("help_prompt")
        user_input = self.listen()
        
        if user_input:
            selection = self.extract_number_from_speech(user_input)
            
            if selection == 1:
                self.speak("pin_help")
                time.sleep(1)
                self.current_state = "main_menu"
            elif selection == 2:
                self.speak("transaction_help")
                time.sleep(1)
                self.current_state = "main_menu"
            elif selection == 3:
                self.current_state = "main_menu"
            else:
                self.speak("custom", message="Invalid selection. Returning to main menu." if self.language == "en" else "अमान्य चयन। मुख्य मेनू पर लौटना।")
                self.current_state = "main_menu"
        else:
            self.current_state = "main_menu"
        
        return True
    
    def goodbye_state(self):
        """End the session"""
        self.speak("goodbye")
        self.card_detected = False
        self.pin_correct = False
        self.attempts = 0
        self.current_state = "welcome"
        return False
    
    def clean_temp_files(self):
        """Clean up temporary files"""
        try:
            # Remove temp directory and all its contents
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            print(f"Cleaned up temporary files in {self.temp_dir}")
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")
    
    def run(self):
        """Main application loop with improved state management"""
        running = True
        
        # State machine implementation
        state_handlers = {
            "welcome": self.welcome_state,
            "agent_selection": self.agent_selection_state,
            "language_selection": self.language_selection_state,
            "card_prompt": self.card_prompt_state,
            "card_inserted": self.card_inserted_state,
            "pin_entry": self.pin_entry_state,
            "main_menu": self.main_menu_state,
            "withdraw_amount": self.withdraw_amount_state,
            "balance_check": self.balance_check_state,
            "pin_change": self.pin_change_state, 
            "mini_statement": self.mini_statement_state,
            "transfer_initiate": self.transfer_initiate_state,
            "help_menu": self.help_menu_state,
            "goodbye": self.goodbye_state
        }
        
        try:
            # Main loop
            while running:
                print(f"\nCurrent state: {self.current_state}")
                
                # Get the correct handler for current state
                handler = state_handlers.get(self.current_state)
                
                if handler:
                    # Run handler and get result
                    continue_running = handler()
                    if not continue_running:
                        running = False
                else:
                    print(f"Error: No handler for state '{self.current_state}'")
                    self.current_state = "welcome"
                      
        except KeyboardInterrupt:
            print("\nATM session terminated by user.")
        except Exception as e:
            print(f"Error in ATM system: {e}")
        finally:
            # Clean up resources
            self.clean_temp_files()
            print("ATM session ended. Thank you for using our service.")


# Run the application
if __name__ == "__main__":
    atm = ATMVoiceAssistant()
    atm.run()
