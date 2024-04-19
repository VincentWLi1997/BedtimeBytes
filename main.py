import streamlit as st
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation
import storyforms

# create our streamlit app
st.button("Start Story Time!", type="primary")

storyforms.assistedform()

'''
open=False
assisted=False
        
col1, col2 = st.columns(2)
with col1:
    if st.button("Let me submit an open-ended prompt", type="secondary"):
        st.write("this one")
with col2:
    if st.button("Use a menu to decide what's in my story", type="secondary"):
        st.write("this one")
        
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Click me', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    st.write('Button clicked!')
    st.slider('Select a value')
    
'''