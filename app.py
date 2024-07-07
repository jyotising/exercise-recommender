import streamlit as st
import numpy as np
# import yfinance as yf

# st.title("Stocks App")
# symbol = st.text_input("Enter a stock symbol", "AAPL")
# if st.button("Get Quote"):
#     st.json(yf.Ticker(symbol).info)

# st.title('_Streamlit_ is :blue[cool] :sunglasses:')


# st.title(':orange[_Exercise_] :green[_Recommender_] :runner:')

st.title(':orange[_Exercise_] :blue[_is all you_] :green[_need_] :runner:')

# st.write('Hello world')
# st.markdown('***Hello world!***')
st.subheader('Upload your workout video and prompt for a suggestion', divider='blue')
prompt = st.chat_input("Enter input prompt...")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
# st.write('Running Streamlit')

# st.button("Generate output", type="primary")
# if st.button("Say hello"):
#     st.write("Why hello there")
# else:
#     st.write("Goodbye")

# uploaded_file = st.sidebar.file_uploader("Choose a file")

uploaded_file = st.file_uploader("Choose a video")

model = st.sidebar.selectbox(label='Choose your model',options=['gemini-1.5-pro','gemini-1.5-flash'])

temp = st.sidebar.select_slider('Temperature',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],value=0.5)
# st.write("The selected temperature is", temp)


st.write("The selected model is", model)



