import streamlit as st
import story_text_generation as story_text_generation
import story_image_generation as story_image_generation
import story_voice_generation as story_voice_generation
import storyforms


# create our streamlit app
st.button("Start Story Time!", type="primary")

storyforms.openform()

