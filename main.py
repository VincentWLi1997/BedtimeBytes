import streamlit as st
import requests
from openai import OpenAI
from PIL import Image
from pathlib import Path
import os
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation

#API Key goes here
client = OpenAI(api_key="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")

# create our streamlit app
with st.form(key = "chat"):
    #Ask user for prompt and press submit button
    prompt = st.text_input("Tell us what kind of bedtime story you want and we'll handle the rest!") # TODO!
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        #Generate story, title, and prompt for image
        story=story_text_generation.get_completion(prompt)
        title_prompt = "The following is a bedtime story for a young child. Generate a title for the story that is 3 words or less. Write only the three word title and nothing else:\n" + story
        image_prompt="The following is a bedtime story for a young child. Generate a picture without any text inside that goes with the story:\n" + story
        title = story_text_generation.get_completion(title_prompt)
        
        #Write out title and story into app
        st.write(title)
        st.write(story)
        
        #Generate image, 
        story_image_generation.get_image(title,image_prompt, "dall-e-3")
        imagefilename = story_image_generation.filename_from_input(title)
        image = Image.open(str(Path(__file__).parent)+'/'+imagefilename+'_1.png')
        st.image(image, caption=title)

        speech_file_path = Path(__file__).parent / "newfile.mp3"
        
        story_voice_generation.text_to_speech(story, speech_file_path)

        audio_file = open(speech_file_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        
