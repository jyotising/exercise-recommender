import streamlit as st
import numpy as np
import google.generativeai as genai
import pathlib
import textwrap
import PIL.Image

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate= lambda _: True))

google_api_key = 'AIzaSyBD7mFBuZXkYdoTlZi5EhArFtEpN2pxgzU'

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
st.subheader('Upload your workout video and prompt for a suggestion', divider='blue')


# Setting the input prompt
prompt = st.chat_input("Enter input prompt...")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")


# Model to be chosen for running the app
model_to_use = st.sidebar.selectbox(label='Choose your model',options=['gemini-1.5-pro','gemini-1.5-flash'])

# Temperature setting to be used
temp = st.sidebar.select_slider('Temperature',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],value=0.0)

# This is the uploaded file
uploaded_file = st.sidebar.file_uploader("Choose a video")


model = genai.GenerativeModel(model_to_use)

# Make the LLM request.
# print("Making LLM inference request...")
response = model.generate_content([prompt],
                                  request_options={"timeout": 600})
# print(response.text)

st.write(response.text)






