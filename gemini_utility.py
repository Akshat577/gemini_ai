import os
import json
from PIL import Image
import google.generativeai as genai

working_directory=os.path.dirname(os.path.abspath(__file__))

config_file_path=f"{working_directory}/config.json"
config_data=json.load(open(config_file_path))

google_api_key=config_data['GOOGLE_API_KEY']

genai.configure(api_key=google_api_key)

def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

def load_gemini_1_5_flash_model(prompt, image):
    gemini_1_5_flash_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_1_5_flash_model.generate_content([prompt, image])
    result = response.text
    return result

def load_embedding_response(input_text):
    embedding_model="models/embedding-001"
    embedding=genai.embed_content(content=input_text,model=embedding_model,
                                  task_type="retrieval_document")
    embedding_list=embedding["embedding"]
    return embedding_list

def gemini_pro_response(user_prompt):
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    response=gemini_pro_model.generate_content(user_prompt)
    return response.text
