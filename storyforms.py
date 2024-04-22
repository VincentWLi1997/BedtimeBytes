import streamlit as st
from PIL import Image
from pathlib import Path
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation
import os    

def format_page():
    col1, col2 = st.columns([1,4])
    logo = Image.open("logo.webp")
    with col1:
        st.image(logo)
    with col2:
        st.title("Tuck in Tales")

def generate_story(prompt):
    #Generate story, and prompts for title and image based on the story
    story=story_text_generation.get_completion(prompt)
    title_prompt = "The following is a bedtime story for a young child. Generate a title in english for this story that is 4 words or less. Write only this title and nothing else. Do not add any punctuation:\n" + story
    image_prompt= "The following is a bedtime story for a young child. Generate a picture that depicts the story. Do not put any written language in the picture:\n" + story
    title = story_text_generation.get_completion(title_prompt)
    
    text_directory = Path(__file__).parent / "text"
    os.makedirs(text_directory, exist_ok=True)
    text_file_name = text_directory / f"{title}.txt"
    with open(text_file_name, 'w', encoding='utf-8') as file:
        file.write(story)
    
    #Generate image 
    story_image_generation.get_image(title,image_prompt, "dall-e-3")
    imagefilename = story_image_generation.filename_from_input(title)
    image = Image.open(str(Path(__file__).parent)+'/'+imagefilename+'_1.png')

    #Generate Text to Speech
    voices_directory = Path(__file__).parent / "voices"
    audio_to_read = story_voice_generation.text_to_speech(story, voices_directory, title)

    with open(audio_to_read,'rb') as audio_file:
        audio_bytes = audio_file.read()
    
    format_story(title,story,image,audio_bytes)
        
    #Write out everything into streamlit
def format_story(title,story,image,audio_bytes):
    st.title(title)
    st.image(image, caption=title)
    st.write(story)
    st.audio(audio_bytes, format='audio/mp3')

class Character:
    def __init__(self, name, role, ethnicity):
        self.name = name
        self.role = role
        self.ethnicity = ethnicity

def openform():
    with st.form(key = "openprompt"):
        #Ask user for prompt and press submit button
        prompt = st.text_input("Tell us what you want a bedtime story about and we'll handle the rest!") # TODO!
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            generate_story(prompt)      
     
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
        
        story_language = st.selectbox("What language do you want the story to be in?", options=("English", 
        "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", 
        "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "Estonian", 
        "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", 
        "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", 
        "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", 
        "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", 
        "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", 
        "Vietnamese", "Welsh"
        ))
          
        prompt = ("Write a story in " + story_language + ". The main character's name is " 
                  + c.name + ". Their role in the story is " + c.role)   
          
        st.write("If your story is ready, hit the submit button!")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            generate_story(prompt)