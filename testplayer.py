import streamlit as st

# Configure the page
st.set_page_config(page_title="Audio Test Player")

# Add a title
st.title("Audio Test Player")

try:
    # Read the audio file
    with open('test_audio.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()
        
    # Add some text above the player
    st.write("Here's your test audio:")
    
    # Play the audio using streamlit
    st.audio(audio_bytes, format='audio/mp3')
    
except FileNotFoundError:
    st.error("Could not find test_audio.mp3. Make sure you've generated the audio file first!")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")