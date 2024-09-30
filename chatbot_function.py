from openai import OpenAI
import datetime
import os
from langdetect import detect

# Load environment variables for OpenAI API key
client = OpenAI()

def get_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OpenAI API key not found in environment variables.")
    return api_key

# Function for speech-to-text conversion
def speech_to_text_conversion(file_path):
    """
    Converts audio format message to text using OpenAI's Whisper model.
    Infers the language from the transcribed text.
    """
    audio_file = open(file_path, "rb")  # Opening the audio file in binary read mode
    transcription = client.audio.transcriptions.create(
        model="whisper-1",  # Model to use for transcription
        file=audio_file     # Audio file to transcribe
    )
    
    # Transcription text
    transcribed_text = transcription.text

    # Detect language from the transcribed text using langdetect
    detected_language = detect(transcribed_text)
    
    return transcribed_text, detected_language


# Translate text from any language to English
def translate_to_english(text):
    """
    Translates text from any language to English using GPT model.
    """
    prompt = f"Translate the following text to English:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator. Do not provide explanations, only translation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def translate_back_to_original(text, original_language):
    """
    Translates text from English back to the original language using GPT model.
    """
    # Explicit translation task, no interpretation or explanations
    prompt = f"Translate the following text from English to {original_language}:\n\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate to {original_language} without providing explanations or context."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content



# Generate a response using OpenAI GPT
def text_chat(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# Convert text to speech
def text_to_speech_conversion(text):
    if text:
        speech_file_path = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_speech.webm"
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",  # Choose the voice you want
            input=text
        )
        response.stream_to_file(speech_file_path)
        with open(speech_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        os.remove(speech_file_path)
        return audio_data
