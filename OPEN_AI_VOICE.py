import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY').strip())

def text_to_speech(title, text, voice_name="alloy"):
    try:
        # Generate audio using OpenAI
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_name,  # OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        # Save to file
        voices_file_path = Path(__file__).parent / "voices"
        os.makedirs(voices_file_path, exist_ok=True)
        output_path = voices_file_path / f"{title}.mp3"
        
        # Stream response to file
        response.stream_to_file(str(output_path))
            
        return str(output_path)
        
    except Exception as e:
        print(f"Error in text to speech: {str(e)}")
        raise

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
                
