import os
import streamlit as st
from openai import OpenAI
from pathlib import Path

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def text_to_speech(title, text, story_voice="nova"):
    voices_file_path = Path(__file__).parent / "voices/" / f"{title}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice=story_voice,
        input=text
    )
    voicefile = filename_from_input(title)
    with open(voicefile, 'wb') as file:
      file.write(response.content)
    return voicefile

def filename_from_input(title):
  alphanum = ""
  for character in title:
    if character.isalnum() or character == " ":
      alphanum += character
  alphanumSplit = alphanum.split()
  if len(alphanumSplit) > 4:
    alphanumSplit = alphanumSplit[:4]
  return "_".join(alphanumSplit)

if __name__ == "__main__":
    voices_file_path = Path(__file__).parent / "voices"
    
    story = "Hello World, my name is Vincent"
    print(f"Testing with: {story}")
    audio_to_read = text_to_speech(text = story, path = voices_file_path, title="HI THIS IS A NEW FILE")
    print(f"OpenAI Responded: ")
    with open(audio_to_read,'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
