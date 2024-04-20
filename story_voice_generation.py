import openai
import os
import openai
import streamlit as st
import requests
from openai import OpenAI
from pathlib import Path
import API_KEY

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def text_to_speech(text,path, title):
    os.makedirs(path, exist_ok=True)
    speech_file_path = Path(__file__).parent / "voices/" / f"{title}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(str(speech_file_path))
    return speech_file_path

if __name__ == "__main__":
    voices_directory = Path(__file__).parent / "voices"
    
    story = "Hello World, my name is Vincent"
    print(f"Testing with: {story}")
    audio_to_read = text_to_speech(text = story, path = voices_directory, title="newfile")
    print(f"OpenAI Responded: ")
    with open(audio_to_read,'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')