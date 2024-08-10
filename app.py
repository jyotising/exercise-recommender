import streamlit as st
import numpy as np
import google.generativeai as genai
import pathlib
import textwrap
import PIL.Image
import tempfile
import os
import time


# Calling the google api key
google_api_key = st.secrets["general"]["api_key"]

genai.configure(api_key=google_api_key)


# Main app design starts from here

## Header -> Exercise is all you need
html_content = """
<h1 style='text-align: left;'>
    <span style="font-size: 48px; font-style: italic; 
                 background: linear-gradient(to right, #8B0000, #FF8C00, #FFD700); 
                 -webkit-background-clip: text;
                 -webkit-text-fill-color: transparent;">
        Exercise is all you Need
    </span>
    <span style="font-size: 70px;">&#127939;</span>
</h1>
"""

st.markdown(html_content, unsafe_allow_html=True)

# Initialize session state for selected model and conversation history
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "gemini-1.5-flash"  # Default model

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# function to reset chat conversation history
def reset_conversation():
    st.session_state.conversation = []

# function to save chat history
def add_to_conversation(prompt, response):
    st.session_state.conversation.append({"prompt": prompt, "response": response})

# Model to be chosen for running the app
selected_model = st.sidebar.selectbox(label='Choose your model',options=['gemini-1.5-flash','gemini-1.5-pro','gemini-1.0-pro (supports text only)'],key='model_selector')

# Checking if the model has changed
if selected_model != st.session_state.selected_model:
    st.session_state.selected_model = selected_model
    reset_conversation()  # Resetting the conversation history

# Temperature setting to be used
if selected_model == 'gemini-1.0-pro (supports text only)':
    temp = st.sidebar.select_slider('Temperature, *(increasing this will get you more creative outputs)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2],value=0.0)
else:
    temp = st.sidebar.select_slider('Temperature, *(increasing this will get you more creative outputs)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.5,1.7,2.0],value=0.0)


# Defining which model to use and storing it in a variable which will be fed into the api
model_to_use = 'gemini-1.0-pro' if selected_model == 'gemini-1.0-pro (supports text only)' else selected_model

# This is the uploaded file works only when gemini-1.5-flash or gemini-1.5-pro is selected
if model_to_use != 'gemini-1.0-pro':
    vfile = st.sidebar.file_uploader("Upload your workout video for suggestion")

    if vfile is not None:
        # Save the uploaded file to a temporary directory
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(vfile.read())
            video_path = temp_file.name
            # st.write(f"Video saved to temporary file: {video_path}")
        
            # st.write(f"Uploading file...")
            video_file = genai.upload_file(path=video_path)
            # st.write(f"Completed upload: {video_file.uri}")
        
            while video_file.state.name == "PROCESSING":
                print('.', end='')
                time.sleep(10)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise ValueError(video_file.state.name)


#Prompt list below
start_prompt ="Introduce yourself as a fitness buddy"

# Very basic prompt gives good results as a starting point, but is unable to give a good description about itself when asked and always expects a follow
# up question to give suggestions about the exercise, so this prompt gives average performance
p0 = """Hi Gemini, You are a gym instructor and 
you need to give suggestions based on what the person asks from you regarding their exercise.
"""

# Decent prompt but asks follow up questions to give better recommendations, also tells that it is a gym instructor on every answer. When asked
# what are you sometimes it tells that it is a llm
p1 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person is doing or asking about.
The person may give a video of their workout and ask suggestion about it or they might just ask about an exercise without giving the workout video,
you need to handle both the cases effectively.

You tell that you are a Gym Instructor if the person asks about you.
"""

# In this prompt, the bot tells that it is gym instructor even while answering questions and it still asks follow up questions while answering 
# questions, although it introduces itself fairly
p2 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person is doing or asking about.
The person may give a video of their workout and ask suggestion about it or they might just ask about an exercise without giving the workout video,
you need to handle both the cases effectively.
You need not ask follow up questions, try to give your best response based on a single user input

You tell that you are a Gym Instructor if the person asks about you.
"""

# Good prompt gives recommendation based on single question and does not ask follow up question. Introduces itself fairly good
p3 = """
Hi Gemini, You are a gym instructor and 
you need to give suggestions based on what the person asks from you regarding their exercise.
You need not ask follow up questions, try to give your best response based on a single user input.
"""

# This is also a good prompt, introduces itself in a short and crisp manner and also gives some good recommendations based on the exercise question
# and does not ask follow up questions, currently using this for gemini-1.5-pro and gemini-1.5-flash
p4 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person is doing or asking about.
The person may give a video of their workout and ask suggestion about it or they might just ask about an exercise without giving the workout video,
you need to handle both the cases effectively.
You need not ask follow up questions, try to give your best response based on a single user input

Only tell that you are a Gym Instructor if the person asks you about yourself.
Also if the person aks about on how to use the app, tell the person that they can upload their workout video
and an input prompt to get suggestion about their exercise or just ask something related to exercise.
"""

# This is the prompt for gemini-1.0-pro, needs to be optimized
p5 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person asks about.
You need not ask follow up questions, try to give your best response based on a single user input

Only tell that you are a Gym Instructor if the person asks you about yourself.
Also if the person aks about on how to use the app, tell the person that they can ask questions regarding their workout
to get suggestion based on it or just ask anything related to an exercise.
"""

# # Setting the input prompt
# prompt_0 = p5 if model_to_use == 'gemini-1.0-pro' else p4
# prompt_1 = "Introduce yourself as a Fitness Buddy"
# response_1 = model.generate_content(prompt_1)


# prompt_2 = st.chat_input("Ask anything about your workout...")

# if prompt_2 is not None:
#     st.markdown("<b style='color:#2491F9;'>Me:</b>" + " " + prompt_2, unsafe_allow_html=True)



# if model_to_use != 'gemini-1.0-pro':
#     if prompt_2 is None:
#         st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_1.text, unsafe_allow_html=True)
#     elif prompt_2 is not None and vfile is None:
#         prompt_2 = prompt_0 + " " + prompt_2
#         response_2 = model.generate_content(prompt_2)
#         st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)
#     elif prompt_2 is not None and vfile is not None:
#         prompt_2 = prompt_0 + " " + prompt_2
#         response_2 = model.generate_content([prompt_2, video_file], request_options={"timeout": 600})
#         st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)
# else:
#     if prompt_2 is None:
#         st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_1.text, unsafe_allow_html=True)
#     elif prompt_2 is not None:
#         prompt_2 = prompt_0 + " " + prompt_2
#         response_2 = model.generate_content(prompt_2)
#         st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)



# Chat Completion from here

if model_to_use == 'gemini-1.0-pro':
    model = genai.GenerativeModel(
    model_to_use,
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,
        temperature=temp,
    ))
    starting_response = model.generate_content(start_prompt)
    st.markdown("<b style='color:#01D78D;'>Fitness Buddy: </b>" + starting_response.text, unsafe_allow_html=True)

    user_prompt = st.chat_input("Ask anything about your workout...")

    if user_prompt is not None:
        chat_history = "\n".join([f"User: {entry['prompt']}\nAI: {entry['response']}" for entry in st.session_state.conversation])
        full_prompt = f"{p5}\n{chat_history}\nUser: {user_prompt}"
        response = model.generate_content(full_prompt)
        add_to_conversation(user_prompt,response.text)
        # st.session_state.conversation.append({"prompt": user_prompt, "response": response.text})

    # Display the conversation history
    for entry in st.session_state.conversation:
        # st.markdown(f"Me: {entry['prompt']}")
        # st.markdown(f"<b style='color:#2491F9;'>Me:</b>" + " " + {entry['prompt']}, unsafe_allow_html=True)
        # st.markdown("<b style='color:#01D78D;'>Fitness Buddy: </b>" + starting_response.text, unsafe_allow_html=True)
        st.markdown(f"<b style='color:#2491F9;'>Me:</b> {entry['prompt']}", unsafe_allow_html=True)
        st.markdown(f"<b style='color:#01D78D;'>Fitness Buddy:</b> {entry['response']}", unsafe_allow_html=True)
        # st.write(f"Fitness Buddy: {entry['response']}")?\
else:
    model = genai.GenerativeModel(
    model_to_use,
    system_instruction=p4,
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,
        temperature=temp,
    ))
    starting_response = model.generate_content(start_prompt)
    st.markdown("<b style='color:#01D78D;'>Fitness Buddy: </b>" + starting_response.text, unsafe_allow_html=True)

    user_prompt = st.chat_input("Ask anything about your workout...")

    if user_prompt is not None and vfile is None:
        chat_history = "\n".join([f"User: {entry['prompt']}\nAI: {entry['response']}" for entry in st.session_state.conversation])
        full_prompt = f"{chat_history}\nUser: {user_prompt}"
        response = model.generate_content(full_prompt)
        add_to_conversation(user_prompt,response.text)
        # prompt_2 = prompt_0 + " " + prompt_2
        # response_2 = model.generate_content(prompt_2)
        # st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)
    elif user_prompt is not None and vfile is not None:
        chat_history = "\n".join([f"User: {entry['prompt']}\nAI: {entry['response']}" for entry in st.session_state.conversation])
        full_prompt = f"{chat_history}\nUser: {user_prompt}"
        response = model.generate_content([full_prompt, video_file], request_options={"timeout": 600})
        add_to_conversation(user_prompt,response.text)
        # prompt_2 = prompt_0 + " " + prompt_2
        # response_2 = model.generate_content([prompt_2, video_file], request_options={"timeout": 600})
        # st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)

    # Display the conversation history
    for entry in st.session_state.conversation:
        # st.markdown(f"Me: {entry['prompt']}")
        # st.markdown(f"<b style='color:#2491F9;'>Me:</b>" + " " + {entry['prompt']}, unsafe_allow_html=True)
        # st.markdown("<b style='color:#01D78D;'>Fitness Buddy: </b>" + starting_response.text, unsafe_allow_html=True)
        st.markdown(f"<b style='color:#2491F9;'>Me:</b> {entry['prompt']}", unsafe_allow_html=True)
        st.markdown(f"<b style='color:#01D78D;'>Fitness Buddy:</b> {entry['response']}", unsafe_allow_html=True)
        # st.write(f"Fitness Buddy: {entry['response']}")?\











