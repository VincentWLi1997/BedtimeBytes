import streamlit as st
from PIL import Image
from pathlib import Path
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation
import os    

def filename_from_input(title):
  alphanum = ""
  for character in title:
    if character.isalnum() or character == " ":
      alphanum += character
  alphanumSplit = alphanum.split()
  if len(alphanumSplit) > 4:
    alphanumSplit = alphanumSplit[:4]
  return "_".join(alphanumSplit)

def format_page():
    st.set_page_config(layout="wide")
    col1, col2 = st.columns([1,4])
    logo = Image.open("logo.png")
    with col1:
        st.image(logo)
    with col2:
        st.title("Bedtime Bytes")

def create_unique_filename(directory, title):
    base_path = directory / title
    counter = 0
    new_path = base_path.with_suffix('.txt')
    while new_path.exists():
        counter += 1
        new_path = directory / f"{title}({counter}).txt"
    return new_path

def generate_story(prompt):
    #Generate story, and prompts for title and image based on the story
    story=story_text_generation.get_completion(prompt)
    title_prompt = "The following is a bedtime story for a young child. Generate a title in english for this story that is 4 words or less. Write only this title and nothing else. Do not add any punctuation:\n" + story
    image_prompt= "The following is a bedtime story for a young child. Generate a picture that depicts the story. Do not put any written language in the picture:\n" + story
    title = story_text_generation.get_completion(title_prompt)
    filename = filename_from_input(title)
    
    #Generate image
    images_directory = Path(__file__).parent / "images"
    os.makedirs(images_directory, exist_ok=True) 
    story_image_generation.get_image(title,image_prompt, "dall-e-3")
    imagefilename = story_image_generation.filename_from_input(title) + ".png"
    image = Image.open(images_directory / imagefilename)


    #Generate Text to Speech
    voices_directory = Path(__file__).parent / "voices"
    os.makedirs(voices_directory, exist_ok=True) 
    audio_to_read = story_voice_generation.text_to_speech(title, story)

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
    def __init__(self, name, role):
        self.name = name
        self.role = role

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
        '''
        character_ethnicity = st.selectbox("What ethnicity would you like the character to be?", options=(
        "Chinese", "Bengali", "Hindi", "Arab", "Malay", "Russian", "Brazilian", "Punjabi", "Japanese", 
        "Javanese", "Vietnamese", "Telugu", "Marathi", "Turkish", "Korean", "Tamil", "Gujarati", 
        "Filipino", "Iranian", "Egyptian", "German", "Hausa", "Pashtun", "Yoruba", "Igbo", "Sindhi", 
        "Italian", "Thai", "Burmese", "Ethiopian", "Ukrainian", "Dutch", "Moroccan", "Algerian", 
        "Kurdish", "Sudanese", "Polish", "French", "Uzbek", "Cossack", "English", "Mexican", 
        "Peruvian", "Spaniard", "Argentine", "Colombian", "Portuguese", "Greek", "Swedish", "Austrian"))'''
        
        c = Character(character_name,character_role)
        
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