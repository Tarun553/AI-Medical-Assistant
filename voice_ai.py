# text_to_speech.py

import os
import logging
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from langdetect import detect
from deep_translator import GoogleTranslator
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get ElevenLabs API key from environment
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def play_audio(file_path):
    """
    Play an audio file using the appropriate method based on the OS.
    
    Args:
        file_path: Path to the audio file to play
    """
    logging.info(f"Playing audio file: {file_path}")
    
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["afplay", file_path])
        else:  # Linux and other OS
            subprocess.call(["xdg-open", file_path])
        logging.info("Audio playback started")
    except Exception as e:
        logging.error(f"Failed to play audio file: {str(e)}")

def text_to_speech_with_gtts(text, output_file, auto_play=True):
    """
    Convert text to speech using Google Text-to-Speech.
    
    Args:
        text: Text to convert to speech
        output_file: Path to save the output audio file
        auto_play: Whether to play the audio after saving
        
    Returns:
        output_file path if successful, None otherwise
    """
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_file)
        logging.info(f"Text-to-speech audio saved to {output_file} (gTTS)")
        
        if auto_play:
            play_audio(output_file)
        
        return output_file
    except Exception as e:
        logging.error(f"Failed to convert text to speech with gTTS: {str(e)}")
        return None

def text_to_speech_with_elevenlabs(text, output_filepath, auto_play=True, 
                                  voice_id="EXAVITQu4vr4xnSDxMaL"):
    """
    Convert text to speech using ElevenLabs.
    
    Args:
        text: Text to convert to speech
        output_filepath: Path to save the output audio file
        auto_play: Whether to play the audio after saving
        voice_id: ID of the voice to use
        
    Returns:
        output_filepath if successful, None otherwise
    """
    if not ELEVENLABS_API_KEY:
        logging.error("ElevenLabs API key not found")
        return None
    
    try:
        detect_language=detect(text)
        if detect_language == "hi":
            language = "hi"
            logging.info("Detected Hindi text for ElevenLabs TTS")
        else:
            language = "en"
            logging.info("Detected English text for ElevenLabs TTS")
            
            # translate english text to hindi before passing to elevenlabs
            translated_text = GoogleTranslator(source='en', target='hi').translate(text)
            logging.info(f"Translated English text to Hindi: {translated_text}")
            text=translated_text
        
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=text,
            language=language,
            voice=voice_id,
            output_format="mp3_22050_32",
            model="eleven_multilingual_v2"
        )
        elevenlabs.save(audio, output_filepath)
        logging.info(f"Text-to-speech audio saved to {output_filepath} (ElevenLabs)")
        
        if auto_play:
            play_audio(output_filepath)
        
        return output_filepath
    except Exception as e:
        logging.error(f"Failed to convert text to speech with ElevenLabs: {str(e)}")
        return None