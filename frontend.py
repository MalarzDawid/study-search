import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("Study-Search 📝")

with st.form("form"):
    input_data = st.text_input("Prompt")
    submitted = st.form_submit_button("Submit")

    if submitted:
        response = requests.post(
            os.environ["BACKEND"], json={"query": input_data}
        ).json()
        st.write(response["answer"])
