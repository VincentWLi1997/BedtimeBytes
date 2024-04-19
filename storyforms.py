import streamlit as st
from PIL import Image
from pathlib import Path
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation
    

def openform():
    with st.form(key = "openprompt"):
        #Ask user for prompt and press submit button
        prompt = st.text_input("Tell us what you want a bedtime story about and we'll handle the rest!") # TODO!
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            #Generate story, and prompts for title and image based on the story
            story=story_text_generation.get_completion(prompt)
            title_prompt = "The following is a bedtime story for a young child. Generate a title in english for this story that is exactly 3 words long. Write only this three word title and nothing else. Do not add any punctuation:\n" + story
            image_prompt= "The following is a bedtime story for a young child. Generate a picture that depicts the story. Do not put any written language in the picture:\n" + story
            title = story_text_generation.get_completion(title_prompt)
            
            #Write out title and story into app
            st.write(title)
            st.write(story)
            
            #Generate image 
            story_image_generation.get_image(title,image_prompt, "dall-e-3")
            imagefilename = story_image_generation.filename_from_input(title)
            image = Image.open(str(Path(__file__).parent)+'/'+imagefilename+'_1.png')
            st.image(image, caption=title)

            #Generate Text to Speech
            speech_file_path = Path(__file__).parent / "newfile.mp3"
            story_voice_generation.text_to_speech(story, speech_file_path)

            audio_file = open(speech_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
       
class Character:
    name = ""
    role = ""
    ethnicity = ""
    def __init__(self, name, role, ethnicity):
        self.name = name
        self.role = role
        self.ethnicity = ethnicity
     
def assistedform():
    with st.form(key = "assistedprompt"):
        
        character_name = st.text_input("What is the character's name?")
        
        character_role = st.text_input("What is the character's role? (Keep it brief)")
        
        character_ethnicity = st.selectbox("What ethnicity would you like the character to be?", options=(
        "Chinese", "Bengali", "Hindi", "Arab", "Malay", "Russian", "Brazilian", "Punjabi", "Japanese", 
        "Javanese", "Vietnamese", "Telugu", "Marathi", "Turkish", "Korean", "Tamil", "Gujarati", 
        "Filipino", "Iranian", "Egyptian", "German", "Hausa", "Pashtun", "Yoruba", "Igbo", "Sindhi", 
        "Italian", "Thai", "Burmese", "Ethiopian", "Ukrainian", "Dutch", "Moroccan", "Algerian", 
        "Kurdish", "Sudanese", "Polish", "French", "Uzbek", "Cossack", "English", "Mexican", 
        "Peruvian", "Spaniard", "Argentine", "Colombian", "Portuguese", "Greek", "Swedish", "Austrian"))
        
        c = Character(character_name,character_role,character_ethnicity)
        
        story_language = st.selectbox("What language do you want the story to be in?", options=(
        "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", 
        "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", 
        "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", 
        "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", 
        "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", 
        "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", 
        "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", 
        "Vietnamese", "Welsh"
            
        ))
          
        prompt = ("Write a story in " + story_language + ". The main character's name is " 
                  + c.name + ". Their role in the story is " + c.role + "The character's ethnicity is "
                  + c.ethnicity)   
          
        st.write("If your story is ready, hit the submit button!")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            #Generate story, and prompts for title and image based on the story
            story=story_text_generation.get_completion(prompt)
            title_prompt = "The following is a bedtime story for a young child. Generate a title in english for this story that is exactly 3 words long. Write only this three word title and nothing else. Do not add any punctuation:\n" + story
            image_prompt= "The following is a bedtime story for a young child. Generate a picture that depicts the story. Do not put any written language in the picture:\n" + story
            title = story_text_generation.get_completion(title_prompt)
            
            #Write out title and story into app
            st.write(title)
            st.write(story)
            
            #Generate image 
            story_image_generation.get_image(title,image_prompt, "dall-e-3")
            imagefilename = story_image_generation.filename_from_input(title)
            image = Image.open(str(Path(__file__).parent)+'/'+imagefilename+'_1.png')
            st.image(image, caption=title)

            #Generate Text to Speech
            speech_file_path = Path(__file__).parent / "newfile.mp3"
            story_voice_generation.text_to_speech(story, speech_file_path)

            audio_file = open(speech_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')