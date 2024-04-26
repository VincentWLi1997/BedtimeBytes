import os
import streamlit as st
from openai import OpenAI
from pathlib import Path

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def text_to_speech(title, text):
    voices_file_path = Path(__file__).parent / "voices/" / f"{title}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    with open(voices_file_path, 'wb') as file:
      file.write(response.content)
    return voices_file_path


if __name__ == "__main__":
    voices_file_path = Path(__file__).parent / "voices"
    
    story = "Hello World, my name is Vincent"
    print(f"Testing with: {story}")
    audio_to_read = text_to_speech(text = story, path = voices_file_path, title="HI THIS IS A NEW FILE")
    print(f"OpenAI Responded: ")
    with open(audio_to_read,'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
