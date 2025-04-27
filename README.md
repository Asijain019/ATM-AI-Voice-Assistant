# ATM-AI-Voice-Assistant
A voice-enabled ATM interface system that supports both English and Hindi languages, providing an accessible banking experience through speech recognition and text-to-speech capabilities.

## Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Key Functions](#key-functions)
- [Supported Transactions](#supported-transactions)
- [Accessibility Features](#accessibility-features)
- [Security Considerations](#security-considerations)
- [Demo Credentials](#demo-credentials)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)

## Features

- **Multilingual Support**: Full support for both English and Hindi
- **Voice and Text Modes**: Use either voice commands or keyboard input based on preference
- **Secure PIN Entry**: Hidden PIN input for security
- **Comprehensive Banking Functionality**: Withdrawals, balance checks, fund transfers, and more
- **Speech Recognition**: Advanced speech processing with noise adjustment
- **Contextual Understanding**: Recognizes commands in both languages with fuzzy matching
- **Secure Display**: Shows sensitive information only on screen, not via voice
- **Help System**: Interactive voice guidance for ATM operations

## System Requirements

- Python 3.6+
- Internet connection (for Google Speech Recognition service)
- Microphone and speakers for voice interaction
- Required libraries:
  - speech_recognition
  - pyttsx3
  - gTTS (Google Text-to-Speech)
  - pygame (optional, for improved audio playback)
  - playsound (fallback audio playback)

## Installation

1. Clone or download the repository
2. Install the required dependencies:

```bash
pip install SpeechRecognition pyttsx3 gTTS pygame playsound
```

3. Ensure your system has the necessary audio drivers installed

## Usage

1. Run the application:

```bash
python atm_voice_assistant.py
```

2. Follow the voice prompts to:
   - Select language preference (English or Hindi)
   - Enable or disable voice assistance
   - Insert your card (simulated)
   - Enter your PIN (use keyboard for security)
   - Select from available banking operations

## Key Functions

- **Language Selection**: Choose between English and Hindi
- **Voice Agent Toggle**: Opt for voice commands or keyboard-only input
- **PIN Entry**: Always uses secure keyboard input (PIN is hidden)
- **Command Recognition**: Understands natural language in both English and Hindi
- **Receipt Option**: Choose whether to print a transaction receipt
- **Help Menu**: Get assistance with PIN entry or transaction operations

## Supported Transactions

- **Cash Withdrawal**: Withdraw funds from your account
- **Balance Inquiry**: Check your current account balance (displayed on screen only)
- **PIN Change**: Update your security PIN
- **Mini Statement**: View recent transaction history
- **Fund Transfer**: Send money to another account
- **Help**: Get assistance with ATM operations

## Accessibility Features

- **Multilingual Support**: Full functionality in both English and Hindi
- **Voice Commands**: Natural language processing for hands-free operation
- **Text Fallback**: Keyboard input available for all functions
- **Clear Voice Prompts**: Well-paced, clear instructions
- **Ambient Noise Adjustment**: Adapts to surrounding noise levels
- **Timeout Handling**: Appropriate responses when no input is detected

## Security Considerations

- **Secure PIN Entry**: Always entered via keyboard, with input masking
- **Limited Attempts**: Three PIN attempts before card lockout
- **Privacy-Focused Voice Responses**: Financial details are displayed on screen, not spoken aloud
- **Temporary File Cleanup**: Voice processing files are automatically removed
- **Secure Transaction Processing**: Simulated processing time for security verification

## Demo Credentials

For demonstration purposes:
- **PIN**: 2341
- **Demo Balance**: ₹25,000

## Troubleshooting

- **Speech Recognition Issues**:
  - Ensure you have an active internet connection
  - Speak clearly and at a moderate pace
  - Adjust microphone settings if needed
  - Fall back to keyboard input if persistent issues occur

- **Audio Playback Problems**:
  - Ensure your speakers/headphones are connected and volume is adequate
  - The system will try multiple audio playback methods if the primary method fails

- **Language Recognition**:
  - Use simple, clear commands
  - For Hindi, common Hinglish terms are also recognized

## Contributors

- Asi Jain | JK Lakshmipat University, Jaipur
  - LinkedIn: [www.linkedin.com/in/asi-jain019](https://www.linkedin.com/in/asi-jain019)
  - GitHub: [https://github.com/Asijain019](https://github.com/Asijain019)

---

For questions, feedback, or contributions, please contact Asi Jain via LinkedIn or GitHub.
