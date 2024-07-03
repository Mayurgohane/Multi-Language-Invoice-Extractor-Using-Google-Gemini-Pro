from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure the Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set it in the .env file.")

# Function to load OpenAI model & get responses
def get_gemini_response(input_text, image_parts, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image_parts[0], prompt])
    return response.text

# Function to prepare the image parts for the API
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="Multi Language Invoice Extractor")
st.header("Multi Language Invoice Extractor")

input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit Button
submit = st.button("Tell me about the image")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image.
               """

# If submit button is clicked
if submit:
    if uploaded_file is not None:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_text, image_data, input_prompt)
            st.subheader("The Response is")
            st.write(response)
        except FileNotFoundError as e:
            st.error(str(e))
    else:
        st.error("Please upload an image to continue.")
