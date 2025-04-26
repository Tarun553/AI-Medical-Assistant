# AI Medical Assistant

## Overview

The **AI Medical Assistant** is a state-of-the-art system that leverages AI technologies to help analyze medical conditions from both **speech input** (symptoms description) and **medical images** (X-rays, CT scans, etc.). It features the use of advanced models from **ElevenLabs**, **Groq**, **OpenAI's Whisper** for transcription, and **Gradio** for the user interface. 

The system can:
- Record user speech, transcribe it, and respond with a **doctor-like response**.
- Analyze medical images and provide **medical diagnoses**.
- Convert text responses to speech in multiple languages including **English** and **Hindi**.
- Work as an interactive **AI-powered medical assistant** using voice and vision.

---

## Features

- **Speech Recognition**: Converts spoken descriptions of symptoms into text using **Whisper**.
- **Medical Image Analysis**: Receives medical images (e.g., X-rays) and generates diagnoses using AI.
- **Text-to-Speech**: Converts doctor responses into speech using **ElevenLabs** or **Google TTS**.
- **Multilingual Support**: Supports **English** and **Hindi** for transcription and responses.
- **Gradio Interface**: Simple and interactive user interface to communicate with the system.

---

## Technologies Used

- **Speech Recognition**: **OpenAI Whisper** (via Groq) for transcription.
- **Medical Image Analysis**: AI model integration (to be replaced with a specific medical model).
- **Text-to-Speech**: **ElevenLabs API** for converting doctor responses into speech.
- **Multilingual Translations**: **Google Translator** for converting transcriptions into Hindi if required.
- **Gradio**: For building the UI and connecting various components together.

---

## Installation

### Prerequisites
Make sure you have Python 3.8 or later installed. You will also need access to an ElevenLabs API key and a Groq API key.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/AI-Medical-Assistant.git
   cd AI-Medical-Assistant
