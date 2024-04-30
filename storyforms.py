import streamlit as st
from PIL import Image
from pathlib import Path
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation
import os
import pandas as pd
from io import StringIO

def filename_from_input(title):
  alphanum = ""
  for character in title:
    if character.isalnum() or character == " ":
      alphanum += character
  alphanumSplit = alphanum.split()
  if len(alphanumSplit) > 4:
    alphanumSplit = alphanumSplit[:4]
  return "_".join(alphanumSplit)

def format_cover():
    st.markdown("<style>.big-font {font-size:120px !important;}</style>", unsafe_allow_html=True)
    st.markdown('<p class="big-font">Welcome to Bedtime Bytes!</p>', unsafe_allow_html=True)
    logo = Image.open("logo.png")
    st.image(logo, width = 800)
    st.header("We create bedtime stories for children. You can either submit your own story, or we can help you create one.")

def format_page():
    st.set_page_config(layout="wide")
    st.markdown("<style>.big-font {font-size:100px !important;}</style>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,10])
    logo = Image.open("logo.png")
    with col1:
        st.image(logo)
    with col2:
        st.markdown('<p class="big-font">Bedtime Bytes</p>', unsafe_allow_html=True)

#This function doesn't make sense yet
def create_unique_filename(directory, title):
    alphanum = ""
    for character in title:
        if character.isalnum() or character == " ":
            alphanum += character
    alphanumSplit = alphanum.split()
    if len(alphanumSplit) > 4:
        alphanumSplit = alphanumSplit[:4]

    base_path = directory / title
    counter = 0
    new_path = base_path.with_suffix('.txt')
    while new_path.exists():
        counter += 1
        new_path = directory / f"{title}({counter}).txt"
    return "_".join(alphanumSplit)

def generate_story(prompt, image_prompt, story_voice):
    #Generate story, and prompts for title and image based on the story
    story=story_text_generation.get_completion(prompt)
    title_prompt = '''The following is a bedtime story for a young child. Generate a title in english for this story that is 4 words or less.
    Write only this title and nothing else. Do not use any punctuation: \n\n''' + story    
    image_prompt+= "\n\n" + story
    title = story_text_generation.get_completion(title_prompt) #Generate  a title from the prompt
    filename = story_text_generation.filename_from_input(title) #Generate a filename from the title
    
    #Create directory for text, and write story into the folder
    text_directory = Path(__file__).parent / "text"
    os.makedirs(text_directory, exist_ok=True)
    text_file_name = text_directory / f"{filename}.txt"
    with open(text_file_name, 'w', encoding='utf-8') as file:
        file.write(story)
    
    #Generate and store image
    images_directory = Path(__file__).parent / "images"
    os.makedirs(images_directory, exist_ok=True) 
    story_image_generation.get_image(title,image_prompt, "dall-e-3")
    imagefilename = story_image_generation.filename_from_input(title) + ".png"
    image = Image.open(images_directory / imagefilename)

    #Generate and store text to speech
    voices_directory = Path(__file__).parent / "voices"
    os.makedirs(voices_directory, exist_ok=True) 
    audio_to_read = story_voice_generation.text_to_speech(title, story, story_voice)

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
    with st.form(key = "open"):
        #Ask user for prompt and press submit button
        prompt = st.text_input("Tell us what you want a bedtime story about and we'll handle the rest!") # TODO!
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            generate_story(prompt)      
     
def assistedform():
    with st.form(key = "assisted"):
        
        story_prompt = ""
        image_prompt = ""
        
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
        
        if story_language:
            story_prompt += "Write a story in " + story_language +". "
        
        story_style = st.selectbox("What storytelling style would you like to emulate?", options=("", "Dr. Seuss", "Greek Mythology",
        "Norse Sagas", "Japanese Rakugo", "West African Griot", "Native American Oral Traditions", "Indian Epics", "Arabian Nights",
        "Chinese Pingshu", "Aboriginal Dreamtime", "Celtic Storytelling", "Russian Skaz", "Italian Commedia dell'Arte", "Jewish Midrash",
        "Caribbean Anansi Stories", "Mexican Corrido"))
        
        if story_style == "":
            story_prompt += "The story is a generic bedtime story. "
        elif story_style:
            story_prompt += "Tell the story in the style of " + story_style + ". "
            
        story_artstyle = st.selectbox("What art style would you like the picture to be in?", options=("", "Anime", "Cartoon", "Lifelike",
        "Renaissance", "Watercolor"))
        
        if story_artstyle == "":
            image_prompt += "Generate a picture depicting the story below. "
        elif story_artstyle:
            image_prompt += "Generate a picture in the art style of " + story_artstyle + " that depicts the story below. "
        
        character_name = st.text_input("What is the main character's name?")
        character_role = st.text_input("What is the main character's role?")
        c = Character(character_name,character_role)
        character_appearance = st.text_input("What does the main character look like?")
        
        if character_name and character_role and character_appearance:  
            image_prompt += ("The main character's name is " 
                + c.name + ". A description of their appearance is: " + character_appearance +
                ". Their role in the story is " + c.role)  
            story_prompt += ("The main character's name is " 
                + c.name + ". A description of their appearance is: " + character_appearance +
                ". Their role in the story is " + c.role)   
        
        story_voice = st.selectbox("Which voice would you like to use?", options =("alloy", "echo", "fable", "onyx", "nova", "shimmer"))
          
        st.write("If your story is ready, hit the submit button!")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            generate_story(story_prompt, image_prompt, story_voice)
            
def submittedstoryform():
    st.title("Submit your own story!")  
    uploaded_file = st.file_uploader("Submission")
    if uploaded_file is not None:
        
        with st.form(key = "ownstory"):
            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            story = stringio.read()
            title = st.text_input("What is the title of your story?")
            
            story_prompt = ""
            image_prompt = ""
            
            story_language = st.selectbox("Translate to another language?", options=("No", "English", 
            "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", 
            "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "Estonian", 
            "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", 
            "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", 
            "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", 
            "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", 
            "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", 
            "Vietnamese", "Welsh"
            ))
            
            story_artstyle = st.selectbox("What art style would you like the picture to be in?", options=("", "Anime", "Cartoon", "Lifelike Art",
            "Renaissance Paintings", "Watercolor"))
            
            if story_artstyle == "":
                image_prompt += "Generate a picture depicting the story below. "
            elif story_artstyle:
                image_prompt += "Generate a picture in the art style of " + story_artstyle + " that depicts the story below. "
                
            story_voice = st.selectbox("Which voice would you like to use?", options =("alloy", "echo", "fable", "onyx", "nova", "shimmer"))
            
            
            
            st.write("If your story is ready, hit the submit button!")
            submitted = st.form_submit_button("Submit")
            if submitted:    
                if story_language!="No":
                    story_prompt += "Translate the following story into " + story_language +": \n\n" + story
                    story = story_text_generation.get_completion(story_prompt)
            
                image_prompt += "\n\n" + story
                
                images_directory = Path(__file__).parent / "images"
                os.makedirs(images_directory, exist_ok=True) 
                story_image_generation.get_image(title,image_prompt, "dall-e-3")
                imagefilename = story_image_generation.filename_from_input(title) + ".png"
                image = Image.open(images_directory / imagefilename)

                #Generate and store text to speech
                voices_directory = Path(__file__).parent / "voices"
                os.makedirs(voices_directory, exist_ok=True) 
                audio_to_read = story_voice_generation.text_to_speech(title, story, story_voice)

                with open(audio_to_read,'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    format_story(title,story,image,audio_bytes)