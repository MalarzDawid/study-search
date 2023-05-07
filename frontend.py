import streamlit as st
from utils import get_response, load_config

config = load_config("config.yaml")

st.title("Study-Search 📝")

with st.form("form"):
    input_data = st.text_input("Prompt")
    submitted = st.form_submit_button("Submit")

    if submitted:
        response = get_response(input_data, config["BACKEND"]).json()

        for item in response:
            c = st.expander(label=str(item["meta"]["page"]))
            c.write(item["content"])
