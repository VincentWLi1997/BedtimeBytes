import streamlit as st
import requests
from openai import OpenAI
from PIL import Image
from pathlib import Path
import os
import StoryTimeApp.story_text_generation as story_text_generation
import StoryTimeApp.story_image_generation as story_image_generation
import StoryTimeApp.story_voice_generation as story_voice_generation


client = OpenAI(api_key="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")

# create our streamlit app
with st.form(key = "chat"):
    prompt = st.text_input("Tell us what kind of bedtime story you want and we'll handle the rest!") # TODO!
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        story=story_text_generation.get_completion(prompt)
        st.write(story)
        image_prompt="The following is a bedtime story for a young child. Generate a picture that goes with the story:\n" + story

        story_image_generation.get_image(prompt,image_prompt, "dall-e-3")
        image = Image.open(str(Path(__file__).parent)+'/images/'+prompt+'_1.png')
        st.image(image, caption='New Image')

        speech_file_path = Path(__file__).parent / "newfile.mp3"
        
        story_voice_generation.text_to_speech(story, speech_file_path)

        audio_file = open(speech_file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        
