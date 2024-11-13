import os

import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model
from gemini_utility import load_gemini_1_5_flash_model
from gemini_utility import load_embedding_response
from gemini_utility import gemini_pro_response
from PIL import Image
working_directory=os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Gemini AI",
    page_icon="A",
    layout="centered"
)

with st.sidebar:
    selected=option_menu(menu_title="Gemini AI",options=["ChatBot","Image Captioning","Embedded Text","Ask me Anything"],menu_icon="robot",icons=['chat-dots-fill','image-fill','textarea-t','patch-question-fill'],default_index=0)

def translate_role_for_streamlit(user_role):
    if user_role=='model':
        return "assistant"
    else:
        return user_role

if selected=="ChatBot":
    model=load_gemini_pro_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session=model.start_chat(history=[])

    st.title("ChatBot")

    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt=st.chat_input("Ask Gemini Pro...")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response=st.session_state.chat_session.send_message(user_prompt)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)


if selected == "Image Captioning":
    st.title("Image Captioning")

    uploaded_image = st.file_uploader("Upload an Image...", type=["jpg", "jpeg", "png"])

    if st.button("Generate caption"):
        image = Image.open(uploaded_image)
        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "write a short caption for this image"

        # Switch to the new model
        caption = load_gemini_1_5_flash_model(default_prompt, image)

        with col2:
            st.info(caption)

if selected=="Embedded Text":
    st.title("Embedded Text")

    input_text=st.text_area(label="",placeholder="Enter the text to get embeddings")

    if st.button("Get embeddings"):
        response=load_embedding_response(input_text)
        st.markdown(response)

if selected=="Ask me Anything":
    st.title("Ask me Anything")

    user_prompt=st.text_area(label="",placeholder="Ask me Anything")
    if st.button("Get an Answer"):
       response=gemini_pro_response(user_prompt)
       st.markdown(response)