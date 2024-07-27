import streamlit as st
import numpy as np
import google.generativeai as genai
import pathlib
import textwrap
import PIL.Image
import tempfile
import os
import time

# from IPython.display import display
# from IPython.display import Markdown

# def to_markdown(text):
#     text = text.replace('•', '  *')
#     return Markdown(textwrap.indent(text, '> ', predicate= lambda _: True))

google_api_key = st.secrets["general"]["api_key"]

genai.configure(api_key=google_api_key)

## Some exapmple codes can be taken refernce of
# import yfinance as yf

# st.title("Stocks App")
# symbol = st.text_input("Enter a stock symbol", "AAPL")
# if st.button("Get Quote"):
#     st.json(yf.Ticker(symbol).info)

# st.title('_Streamlit_ is :blue[cool] :sunglasses:')

# st.title(':orange[_Exercise_] :green[_Recommender_] :runner:')
# st.write('Hello world')
# st.markdown('***Hello world!***')

# st.write('Running Streamlit')

# st.button("Generate output", type="primary")
# if st.button("Say hello"):
#     st.write("Why hello there")
# else:
#     st.write("Goodbye")

# uploaded_file = st.sidebar.file_uploader("Choose a file")

# st.write("The selected temperature is", temp)
# st.write("The selected model is", model)





# Main app design starts from here

# This is the title of the web app
st.title(':orange[_Exercise_] :blue[_is all you_] :green[_need_] :runner:')

# Subheader
st.subheader('Get a suggestion for your workout', divider='blue')



# Model to be chosen for running the app
model_to_use = st.sidebar.selectbox(label='Choose your model',options=['gemini-1.5-pro','gemini-1.5-flash'])

# Temperature setting to be used
temp = st.sidebar.select_slider('Temperature, *(increasing this makes responses more random)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],value=0.0)

# This is the uploaded file
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


model = genai.GenerativeModel(
    model_to_use,
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,
        temperature=temp,
    ))

# Chat history initialized
# chat = model.start_chat(history=[]) 

# Setting the input prompt
prompt_0 = """Hi Gemini, You are a gym instructor and 
you need to give suggestions based on what the person asks from you regarding their exercise.
"""
prompt_1 = "Respond as if you are a Gym Instructor"
# response_1 = model.generate_content(prompt_1, stream=True)
response_1 = model.generate_content(prompt_1)

# st.write(response_1.text)

prompt_2 = st.chat_input("Ask something about your workout...")

# st.write(len(prompt_2))


if prompt_2 is None:
    st.write(response_1.text)
elif prompt_2 is not None and vfile is None:
    prompt_2 = prompt_0 + " " + prompt_2
    response_2 = model.generate_content(prompt_2)
    st.write(response_2.text)
elif prompt_2 is not None and vfile is not None:
    prompt_2 = prompt_0 + " " + prompt_2
    response_2 = model.generate_content([prompt_2, video_file], request_options={"timeout": 600})
    st.write(response_2.text)



# if prompt_2 is None:
#     for chunk in response_1:
#         # st.write(chunk.text)
#         # st.markdown(f"{chunk.text}\n\n---\n\n")
#         # st.markdown(f"<div style='padding: 10px; font-size: 18px; line-height: 1.6;'>{chunk.text}</div>", unsafe_allow_html=True)
#         st.markdown(f"<div style='padding: 10px; border-bottom: 1px solid #ddd;'>{chunk.text}</div>", unsafe_allow_html=True)
# else:
#     prompt_2 = prompt_0 + " " + prompt_2
#     response_2 = model.generate_content(prompt_2,stream=True)
#     for chunk in response_2:
#         # st.write(chunk.text)
#         # st.markdown(f"{chunk.text}\n\n---\n\n")
#         # st.markdown(f"<div style='padding: 10px; font-size: 18px; line-height: 1.6;'>{chunk.text}</div>", unsafe_allow_html=True)
#         st.markdown(f"<div style='padding: 10px; border-bottom: 1px solid #ddd;'>{chunk.text}</div>", unsafe_allow_html=True)

# prompt_2 = st.chat_input("Ask something about your workout...") or "Hi Gemini"
# response = chat.send_message(st.chat_input("Enter input prompt...") or "Hi Gemini")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")

# Make the LLM request.
# print("Making LLM inference request...")

# response = model.generate_content(prompt)
# response = model.generate_content(prompt, stream=True)
# print(response.text)

# st.write(response.text)

# st.write(for chunk in response:
#   print(chunk.text)
#   print("_"*80))

# for chunk in response:
#     st.write(chunk.text)
    # st.write("")





