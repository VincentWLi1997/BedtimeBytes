import openai
import os
import openai
import streamlit as st
import requests
from openai import OpenAI
from pathlib import Path

st.markdown("# Page 5 Text to Speech ❄️")
st.sidebar.markdown("# Page 5 Text to Speech ❄️")

speech_file_path = Path(__file__).parent / "newfile.mp3"

client = OpenAI(api_key="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")

def text_to_speech(text,path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(speech_file_path)

text = ''

# Create a button
if st.button('Submit'):
    text_to_speech(text, speech_file_path)

    audio_file = open(speech_file_path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')