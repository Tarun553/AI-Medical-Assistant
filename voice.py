import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

from langdetect import detect
from deep_translator import GoogleTranslator
# Try to import from your module first, fall back to environment variable
try:
    from brain_of_dr import GROQ_API_KEY
except ImportError:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables or brain_of_dr module")

# 🔥 Set ffmpeg and ffprobe paths manually (important for venv)
AudioSegment.converter = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl-shared\bin\ffprobe.exe"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from microphone and save as MP3.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Listening for speech...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording completed.")
            audio_data = audio.get_wav_data()
            audio_segment = AudioSegment.from_file(BytesIO(audio_data), format="wav")
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")
            return file_path
    except Exception as e:
        logging.error(f"Failed to record audio: {str(e)}")
        return None

def transcribe_audio(audio_filepath):
    """
    Transcribe audio using Groq's Whisper model.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        sst_model = "whisper-large-v3-turbo"
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=sst_model,
                file=audio_file,
                language="auto",
                
            )
            detected_language = detect(transcription.text)
            logging.info(f"Detected language: {detected_language}")
            if detected_language != 'hi':
                logging.info(f"Translating transcription from {detected_language} to Hindi...")
                translated_text = GoogleTranslator(source=detected_language, target='hi').translate(transcription.text)
                logging.info(f"Translated text: {translated_text}")
                return transcription.text, translated_text, detected_language
            else:
                logging.info("Transcription is already in Hindi.")
                return transcription.text, transcription.text, detected_language
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {str(e)}")
        return None
    
    
    
