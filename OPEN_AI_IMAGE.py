import requests
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY').strip()
client = OpenAI(api_key=api_key)

# Downloads an image from the given url.
def download_image(filename, url):
  response = requests.get(url)
  if response.status_code == 200:
    with open(filename, 'wb') as file:
      file.write(response.content)
  else:
    print("error downloading image from URL:", url)

    # Generates a file name from the user's input.
def filename_from_input(prompt):
  alphanum = ""
  for character in prompt:
    if character.isalnum() or character == " ":
      alphanum += character
  alphanumSplit = alphanum.split()
  if len(alphanumSplit) > 4:
    alphanumSplit = alphanumSplit[:4]
  return "_".join(alphanumSplit)

# Create an image
# If model is not specified, the default is DALL-E-2.
def get_image(title, image_prompt, model="dall-e-3"):
    # Sanitize the image prompt to be more DALL-E friendly
    safe_prompt = "Create a child-friendly, colorful illustration suitable for a children's book showing: " + image_prompt
    safe_prompt = safe_prompt.replace("Generate a picture depicting the story below.", "")
    safe_prompt = safe_prompt.replace("Do not put any written language in the picture.", "")
    
    try:
        n = 1   # Number of images to generate
        image = client.images.generate(
            prompt=safe_prompt,
            model=model,
            n=n,
            size="1024x1024",
            quality="standard"
        )
        
        for i in range(n):
            filename = "images/" + filename_from_input(title) + ".png"
            download_image(filename, image.data[i].url)

        return image
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise
'''
if __name__ == "__main__":
  title = "water boy"
  image_prompt = "The following is a bedtime story for a young child. Generate a picture that depicts the story. Do not put any written language in the picture:\n"
  from pathlib import Path
  from PIL import Image
  import streamlit as st
  images_directory = Path(__file__).parent / "images"
  os.makedirs(images_directory, exist_ok=True) 
  get_image(title,image_prompt, "dall-e-3")
  
  
  imagefilename = filename_from_input(title)
  image = Image.open(str(Path(__file__).parent)+'/'+imagefilename+'_1.png')
  st.image(image)
'''