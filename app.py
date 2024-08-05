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

# This is the title of the web app
# st.title(':orange[_Exercise_] :blue[_is all you_] :green[_need_] :runner:')

# st.markdown("""
#     <h1 style="text-left: center;">
#         <span style="color:#FC4B29;"><i>Exercise</i></span> 
#         <span style="color:#FC4B29;"><i>is all you</i></span> 
#         <span style="color:#FC4B29;"><i>need</i></span> 
#         <span>&#127947</span>
#         <img src="link_here" alt="Lifting Weights" style="width:100px;height:100px;">
#     </h1>
#     """, unsafe_allow_html=True)

# st.markdown("""
#     <h1 style="text-left: center;">
#         <span style="color:#FC4B29;"><i>Exercise</i></span> 
#         <span style="color:#FC4B29;"><i>is all you</i></span> 
#         <span style="color:#FC4B29;"><i>need</i></span> 
#         <span>&#127939</span>
#     </h1>
#     """, unsafe_allow_html=True)

# st.image("plank_with_lateral_raise.gif",width=400)

# html_content = """
# <h1 style='text-align: left;'>
#     <span style="font-size: 48px; font-style: italic; 
#                  background: linear-gradient(to right, darkblue, lightblue);
#                  -webkit-background-clip: text;
#                  background-clip: text;
#                  color: transparent;">
#         Exercise is all you Need
#     </span>
#     <span style="font-size: 80px;">&#127939</span>
# </h1>
# """

# html_content = """
# <h1 style='text-align: left;'>
#     <span style="font-size: 48px; font-style: italic; 
#                  background: linear-gradient(to right, #00008B, #ADD8E6); /* DarkBlue to LightBlue */
#                  -webkit-background-clip: text;
#                  background-clip: text;
#                  color: transparent;">
#         Exercise is all you Need
#     </span>
#     <span style="font-size: 80px;">&#127939;</span>
# </h1>
# """

# html_content = """
# <h1 style='text-align: left;'>
#     <span style="font-size: 48px; font-style: italic; 
#                  background: -webkit-linear-gradient(left, #00008B, #ADD8E6); 
#                  -webkit-background-clip: text;
#                  color: transparent;">
#         Exercise is all you Need
#     </span>
#     <span style="font-size: 80px;">&#127939;</span>
# </h1>
# """
# html_content = """
# <h1 style='text-align: left;'>
#     <span style="font-size: 48px; font-style: italic; 
#                  background: -webkit-linear-gradient(left, #8B0000, #FF6347); 
#                  -webkit-background-clip: text;
#                  color: transparent;">
#         Exercise is all you Need
#     </span>
#     <span style="font-size: 80px;">&#127939;</span>
# </h1>
# """
# html_content = """
# <h1 style='text-align: left;'>
#     <span style="font-size: 48px; font-style: italic; 
#                  background: linear-gradient(to right, #8B0000, #FF6347); 
#                  -webkit-background-clip: text;
#                  -webkit-text-fill-color: transparent;">
#         Exercise is all you Need
#     </span>
#     <span style="font-size: 80px;">&#127939;</span>
# </h1>
# """
html_content = """
<h1 style='text-align: left;'>
    <span style="font-size: 48px; font-style: italic; 
                 background: linear-gradient(to right, #8B0000, #FF8C00, #FFD700); 
                 -webkit-background-clip: text;
                 -webkit-text-fill-color: transparent;">
        Exercise is all you Need
    </span>
    <span style="font-size: 80px;">&#127939;</span>
</h1>
"""

st.markdown(html_content, unsafe_allow_html=True)

# ht = """
# <h1>Exercise is all you need</h1>
# <img src="plank_with_lateral_raise.gif" alt="Plank with lateral Raise" width="400">
# """
# st.markdown(ht, unsafe_allow_html=True)
# st.markdown(
#     """
#     <div style="display: flex; justify-content: flex-start;">
#         <img src="plank_with_lateral_raise.gif" alt="Exercise GIF" style="width: 400px; height: auto;">
#     </div>
#     """, 
#     unsafe_allow_html=True
# )


# Codes for emoji
# 1.	🏃 (Person Running) - &#127939;
# 2.	🏋️ (Person Lifting Weights) - &#127947;
# 3.	🚴 (Person Biking) - &#128690;
# 4.	🤸 (Person Cartwheeling) - &#129336;
# 5.	🧘 (Person in Lotus Position) - &#129496;
# 6.	🏊 (Person Swimming) - &#127946;
# 7.	🤾 (Person Playing Handball) - &#129342;
# 8.	🤽 (Person Playing Water Polo) - &#129341;
# 9.	🏌️ (Person Golfing) - &#127948;
# 10.	🏄 (Person Surfing) - &#127940;

# Subheader
# st.subheader('Get a suggestion for your workout', divider='blue')

# subheader_text = "Get a suggestion for your workout"
# text_color = "#ADD8E6"  # Light blue for text
# divider_color = "#F84C70"  # Blue for divider
# font_size = "28px"  # Adjust the font size as needed

# # HTML content for the styled subheader
# html_content = f"""
# <h2 style='color:{text_color}; border-bottom: 2px solid {divider_color}; padding-bottom: 10px; margin-bottom: 20px; font-size: {font_size};'>
#     {subheader_text}
# </h2>
# """

# # Display the styled subheader
# st.markdown(html_content, unsafe_allow_html=True)

# subheader_text = "Get a suggestion for your workout"
# gradient_text = "linear-gradient(to right, #EC008C, #FC6767)"
# gradient_border = "linear-gradient(to right, #00F5AO, #00D9F5)"  # Gradient from dark orange to yellow-orange
# font_size = "28px"  # Adjust the font size as needed

# # HTML content for the styled subheader
# html_content = f"""
# <h2 style="
#     font-size: {font_size};
#     background: {gradient_text};
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     border-bottom: 2px solid;
#     border-image: {gradient_text} 1;
#     padding-bottom: 10px;
#     margin-bottom: 20px;">
#     {subheader_text}
# </h2>
# """

# # Display the styled subheader
# st.markdown(html_content, unsafe_allow_html=True)


# Model to be chosen for running the app
model_to_use = st.sidebar.selectbox(label='Choose your model',options=['gemini-1.5-flash','gemini-1.5-pro','gemini-1.0-pro (supports text only)'])

# Temperature setting to be used
temp = st.sidebar.select_slider('Temperature, *(increasing this will get you more creative outputs)*',options=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.5,1.7,2.0],value=0.0)

# This is the uploaded file
if model_to_use != 'gemini-1.0-pro (supports text only)':
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

# if vfile is not None:
#     # Save the uploaded file to a temporary directory
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
#         temp_file.write(vfile.read())
#         video_path = temp_file.name
#         # st.write(f"Video saved to temporary file: {video_path}")
        
#         # st.write(f"Uploading file...")
#         video_file = genai.upload_file(path=video_path)
#         # st.write(f"Completed upload: {video_file.uri}")
        
#         while video_file.state.name == "PROCESSING":
#             print('.', end='')
#             time.sleep(10)
#             video_file = genai.get_file(video_file.name)
            
#         if video_file.state.name == "FAILED":
#             raise ValueError(video_file.state.name)

model_to_use = 'gemini-1.0-pro' if model_to_use == 'gemini-1.0-pro (supports text only)' else model_to_use 

model = genai.GenerativeModel(
    model_to_use,
    generation_config=genai.GenerationConfig(
        max_output_tokens=2000,
        temperature=temp,
    ))

# Chat history initialized
# chat = model.start_chat(history=[]) 

#Prompt list below

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
# and does not ask follow up questions
p4 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person is doing or asking about.
The person may give a video of their workout and ask suggestion about it or they might just ask about an exercise without giving the workout video,
you need to handle both the cases effectively.
You need not ask follow up questions, try to give your best response based on a single user input

Only tell that you are a Gym Instructor if the person asks you about yourself.
Also if the person aks about on how to use the app, tell the person that they can upload their workout video
and an input prompt to get suggestion about their exercise or just ask something related to exercise.
"""

p5 = """
Hi Gemini! You are a Gym instructor and you need to give suggestions based on which type of exercise the person asks about.
You need not ask follow up questions, try to give your best response based on a single user input

Only tell that you are a Gym Instructor if the person asks you about yourself.
Also if the person aks about on how to use the app, tell the person that they can ask questions regarding their workout
to get suggestion based on it or just ask anything related to an exercise.
"""

# Setting the input prompt
prompt_0 = p5 if model_to_use == 'gemini-1.0-pro' else p4
prompt_1 = "Respond as if you are a Gym Instructor"
# response_1 = model.generate_content(prompt_1, stream=True)
response_1 = model.generate_content(prompt_1)

# st.write(response_1.text)

prompt_2 = st.chat_input("Ask anything regarding your workout...")

if prompt_2 is not None:
    # st.markdown("<div style='text-align: right;'><b style='color:blue;'>User:</b></div>" + " " + prompt_2, unsafe_allow_html=True)
    st.markdown("<b style='color:#2491F9;'>User:</b>" + " " + prompt_2, unsafe_allow_html=True)
    # st.write("**User:**" + " " + prompt_2)
    # st.write("__User:__" + prompt_2)
    # st.write(prompt_2)


# st.write(len(prompt_2))

if model_to_use != 'gemini-1.0-pro':
    if prompt_2 is None:
        st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_1.text, unsafe_allow_html=True)
    elif prompt_2 is not None and vfile is None:
        prompt_2 = prompt_0 + " " + prompt_2
        response_2 = model.generate_content(prompt_2)
        st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)
    elif prompt_2 is not None and vfile is not None:
        prompt_2 = prompt_0 + " " + prompt_2
        response_2 = model.generate_content([prompt_2, video_file], request_options={"timeout": 600})
        st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)
else:
    if prompt_2 is None:
        st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_1.text, unsafe_allow_html=True)
    elif prompt_2 is not None:
        prompt_2 = prompt_0 + " " + prompt_2
        response_2 = model.generate_content(prompt_2)
        st.markdown("<b style='color:#01D78D;'>Fitness Buddy:</b>" + " " + response_2.text, unsafe_allow_html=True)



# if prompt_2 is None:
#     for chunk in response_1:
#         st.write(chunk.text)
#         # st.markdown(f"{chunk.text}\n\n---\n\n")
#         # st.markdown(f"<div style='padding: 10px; font-size: 18px; line-height: 1.6;'>{chunk.text}</div>", unsafe_allow_html=True)
#         # st.markdown(f"<div style='padding: 10px; border-bottom: 1px solid #ddd;'>{chunk.text}</div>", unsafe_allow_html=True)
# else:
#     prompt_2 = prompt_0 + " " + prompt_2
#     response_2 = model.generate_content(prompt_2,stream=True)
#     for chunk in response_2:
#         st.write(chunk.text)
#         # st.markdown(f"{chunk.text}\n\n---\n\n")
#         # st.markdown(f"<div style='padding: 10px; font-size: 18px; line-height: 1.6;'>{chunk.text}</div>", unsafe_allow_html=True)
#         # st.markdown(f"<div style='padding: 10px; border-bottom: 1px solid #ddd;'>{chunk.text}</div>", unsafe_allow_html=True)

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





