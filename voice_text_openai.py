from audio_recorder_streamlit import audio_recorder
import tempfile
import chatbot_function
import streamlit as st
import streamlit.components.v1 as components

st.title('🎙️🤖Voice ChatBot with Translation🤖🎙️')

# Record audio input
audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="3x",
)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

# Update how the transcription is handled since we no longer return detected language

# Step 1: Add a font size slider at the beginning of the Streamlit app
font_size = st.slider('Adjust font size for translated text (for hearing-impaired patients)', 20, 100, 30)

# Rest of your code...
if st.button('🎙️Get Response🎙️'):
    # Step 1: Patient speaks (non-English) -> Speech-to-text and language detection
    converted_text, detected_language = chatbot_function.speech_to_text_conversion(temp_audio_path)
    st.write("Patient Transcription:", converted_text)
    st.write("Detected Language:", detected_language)

    # Step 2: Translate patient's text to English
    translated_text_to_english = chatbot_function.translate_to_english(converted_text)
    st.write("Patient's message in English:", translated_text_to_english)

    # Step 3: Clinician speaks (English) -> Speech-to-text (No translation yet)
    clinician_audio_bytes = audio_recorder(
        text="Clinician: Click to record your response",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="3x",
    )
    
    if clinician_audio_bytes:
        # Transcribe clinician's voice
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as clinician_audio:
            clinician_audio.write(clinician_audio_bytes)
            clinician_audio_path = clinician_audio.name

        clinician_text = chatbot_function.speech_to_text_conversion(clinician_audio_path)
        st.write("Clinician's Response (English):", clinician_text)
        
        # Step 4: Translate clinician's English response back to patient's language
        translated_back_to_original = chatbot_function.translate_back_to_original(clinician_text, detected_language)
        
        # Step 5: Display translated text in larger font for hearing-impaired patients
        components.html(f"""
            <div style="font-size:{font_size}px; margin: 20px 0;">
                Translated back to {detected_language}: {translated_back_to_original}
            </div>
        """, height=200)
        
        # Step 6: Convert translated response to speech in the original language
        audio_data = chatbot_function.text_to_speech_conversion(translated_back_to_original)

        # Save and play the audio response for the patient
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile.write(audio_data)
            tmpfile_path = tmpfile.name
            st.audio(tmpfile_path)
