from dotenv import load_dotenv
import os
import streamlit as st
from elevenlabs.client import ElevenLabs
from pathlib import Path

# Load environment variables
load_dotenv()

client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY').strip())

def text_to_speech(title, text, voice_name="Vincent"):
    try:
        # Get all available voices
        voices = client.voices.get_all().voices
        voice_options = {v.name: v.voice_id for v in voices}
        
        if voice_name not in voice_options:
            raise ValueError(f"Voice '{voice_name}' not found. Available voices: {list(voice_options.keys())}")
        
        # Generate audio
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id=voice_options[voice_name],
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Convert generator to bytes
        audio_bytes = b"".join(chunk for chunk in audio_stream)
        
        # Save to file
        voices_file_path = Path(__file__).parent / "voices"
        os.makedirs(voices_file_path, exist_ok=True)
        output_path = voices_file_path / f"{title}.mp3"
        
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        
        return str(output_path)
        
    except Exception as e:
        print(f"Error in text to speech: {str(e)}")
        raise