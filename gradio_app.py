import os
import gradio as gr
import logging

from brain_of_dr import encode_image_to_base64, analyize_image_with_query
from voice import transcribe_audio
from voice_ai import text_to_speech_with_gtts

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Define model and system prompt ---
model = "meta-llama/llama-4-scout-17b-16e-instruct"

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    # Transcribe audio if provided
    speech_to_text_output = ""
    if audio_filepath:
        speech_to_text_output = transcribe_audio(audio_filepath=audio_filepath, language="en")

    # Handle image input and doctor response
    doctor_response = "No input provided"
    if image_filepath:
        image_base64 = encode_image_to_base64(image_filepath)
        query = system_prompt
        if speech_to_text_output:
            query += " " + speech_to_text_output
        doctor_response = analyize_image_with_query(
            query=query,
            image_base64=image_base64,
            model=model
        )
    elif speech_to_text_output:
        doctor_response = "No image provided. I can only analyze medical conditions with an image."

    # Generate TTS
    tts_audio_path = "ai_doctor_response.mp3"
    text_to_speech_with_gtts(text=doctor_response, output_file=tts_audio_path, auto_play=False)

    return speech_to_text_output, doctor_response, tts_audio_path

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone", "upload"], type="filepath", label="🎙️ Speak or Upload Audio"),
        gr.Image(type="filepath", label="🩻 Upload Medical Image")
    ],
    outputs=[
        gr.Textbox(label="📝 Your Speech Transcription", lines=2),
        gr.Textbox(label="🩺 Doctor's Response", lines=3),
        gr.Audio(label="🔊 Voice Response", autoplay=True)
    ],
    title="AI Doctor with Real-Time Voice 🩺🎙️",
    description="Speak naturally or upload an audio file. Upload a relevant medical image too if you want.",
    theme="soft"
)

if __name__ == "__main__":
    iface.launch(share=True)