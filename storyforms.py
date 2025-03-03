import streamlit as st
from PIL import Image
from pathlib import Path
import OPEN_AI_TEXT as OPEN_AI_TEXT
import OPEN_AI_IMAGE as OPEN_AI_IMAGE
import ELEVEN_LABS_VOICE as ELEVEN_LABS_VOICE
import os
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

def format_prompts(story_prompt, title_prompt="", image_prompt="", voice_name=""):
    st.subheader("Prompts Being Used:")
    st.write("Story Prompt:")
    st.write(story_prompt)
    
    if title_prompt:
        st.write("Title Prompt:")
        st.write(title_prompt)
    
    st.write("Image Prompt:")
    st.write(image_prompt)
    
    st.write("Voice Selected:")
    st.write(voice_name)
    
    st.divider()  # Add a visual separator

def generate_story(prompt, art_style="Cartoon", story_voice="Vincent"):
    # Display prompts first
    # Then generate everything
    story = OPEN_AI_TEXT.get_completion(prompt)

    title_prompt = '''The following is a bedtime story for a young child. Generate a title in english for this story that is 4 words or less.
    Write only this title and nothing else. Do not use any punctuation: \n\n''' + story

    title = OPEN_AI_TEXT.get_completion(title_prompt)
    
    # Create image prompt with art style
    image_prompt = f"Create a child-friendly illustration in {art_style} style that captures this story:\n\n" + story
    
    format_prompts(prompt, title_prompt, image_prompt, story_voice)
    
    filename = OPEN_AI_TEXT.filename_from_input(title)
    
    #Create directory for text, and write story into the folder
    text_directory = Path(__file__).parent / "text"
    os.makedirs(text_directory, exist_ok=True)
    text_file_name = text_directory / f"{filename}.txt"
    with open(text_file_name, 'w', encoding='utf-8') as file:
        file.write(story)
    
    #Generate and store image
    images_directory = Path(__file__).parent / "images"
    os.makedirs(images_directory, exist_ok=True) 
    OPEN_AI_IMAGE.get_image(title, image_prompt, "dall-e-3")
    imagefilename = OPEN_AI_IMAGE.filename_from_input(title) + ".png"
    image = Image.open(images_directory / imagefilename)

    #Generate and store text to speech using ElevenLabs
    voices_directory = Path(__file__).parent / "voices"
    os.makedirs(voices_directory, exist_ok=True) 
    audio_to_read = ELEVEN_LABS_VOICE.text_to_speech(filename, story, story_voice)

    with open(audio_to_read,'rb') as audio_file:
        audio_bytes = audio_file.read()
    
    

    format_story(title, story, image, audio_bytes)
    
    
        
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

def quickform():
    with st.form(key = "open"):
        prompt = "Please write a bedtime story about the following prompt:\n"
        prompt += st.text_input("Tell us what you want a bedtime story about and we'll handle the rest!")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            generate_story(prompt)

def menuform():
    with st.form(key = "assisted"):
        story_prompt = "Write a bedtime story with the following details: "
        
        story_language = st.selectbox("Language", options=("English", 
        "Chinese", "Spanish", "French", "German", "Japanese", "Portuguese", "Arabic", 
        "Russian", "Italian", "Korean"
        ))
        
        if story_language != "English":
            story_prompt = f"Write the following story in {story_language}. "
            
        character_description = st.text_input("Describe the main character of the story.")
        
        if character_description:  
            story_prompt += (f"This is a description of the story's main character: {character_description}.")
        
        art_style = st.selectbox("Art Style", options=(
            "Cartoon",
            "Anime",
            "Renaissance Painting"
        ))
        
        story_voice = st.selectbox("Which voice would you like to use?", 
            options=("Vincent", "Rachel", "Domi", "Bella", "Antoni", "Elli", "Josh", "Arnold", "Adam", "Sam"))
          
        st.write("If your story is ready, hit the submit button!")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Pass the story prompt, art style and voice
            generate_story(story_prompt, art_style, story_voice)

def submittedstoryform():
    st.title("Submit your own story!")  
    uploaded_file = st.file_uploader("Submission")
    if uploaded_file is not None:
        
        with st.form(key = "ownstory"):
            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            story = stringio.read()
            title = st.text_input("What is the title of your story?")
            
            story_language = st.selectbox("Translate to another language?", options=("English", 
            "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", 
            "Catalan", "Chinese", "Croatian", "Czech", "Danish", "Dutch", "Estonian", 
            "Finnish", "French", "Galician", "German", "Greek", "Hebrew", "Hindi", "Hungarian", 
            "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh", "Korean", 
            "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian", 
            "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", 
            "Spanish", "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", 
            "Vietnamese", "Welsh"
            ))
            
            art_style = st.selectbox("Art Style", options=(
                "Cartoon",
                "Anime", 
                "Renaissance Painting"
            ))
            
            story_voice = st.selectbox("Which voice would you like to use?", 
                options=('Aria', 'Roger', 'Sarah', 'Laura', 'Charlie', 'George', 'Callum', 'River', 'Liam', 'Charlotte', 'Alice', 'Matilda', 'Will', 'Jessica', 'Eric', 'Chris', 'Brian', 'Daniel', 'Lily', 'Bill', 'Vincent'))
            
            
            
            st.write("If your story is ready, hit the submit button!")
            submitted = st.form_submit_button("Submit")
            if submitted:    
                if story_language!="No":
                    story_prompt = f"Translate the following story into {story_language}: \n\n{story}"
                else:
                    story_prompt = story
                
                # Generate image with selected art style
                image_prompt = f"Create a child-friendly illustration in {art_style} style that captures this story:\n\n" + story
                
                images_directory = Path(__file__).parent / "images"
                os.makedirs(images_directory, exist_ok=True) 
                OPEN_AI_IMAGE.get_image(title,image_prompt, "dall-e-3")
                imagefilename = OPEN_AI_IMAGE.filename_from_input(title) + ".png"
                image = Image.open(images_directory / imagefilename)

                # Display prompts before generating
                format_prompts(story_prompt, "", image_prompt, story_voice)

                # Then generate everything
                if story_language != "No":
                    story = OPEN_AI_TEXT.get_completion(story_prompt)
                
                #Generate and store text to speech
                voices_directory = Path(__file__).parent / "voices"
                os.makedirs(voices_directory, exist_ok=True) 
                audio_to_read = ELEVEN_LABS_VOICE.text_to_speech(title, story, story_voice)

                with open(audio_to_read,'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    format_story(title,story,image,audio_bytes)