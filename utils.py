import yaml
import requests
import os
from tqdm import tqdm
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


def load_config(filepath) -> dict:
    with open(filepath) as file:
        config = yaml.safe_load(file)
    return config


def get_response(prompt: str, url):
    request = {"query": prompt}
    response = requests.post(url, json=request)
    return response


def postprocessing(text):
    out = []
    for item in text:
        out.append({"content": item.page_content, "meta": item.metadata})
    return out


def load_pages(data_dir):
    files = []
    for file in tqdm(os.listdir(data_dir)):
        loader = PyPDFLoader(os.path.join(data_dir, file))
        pages = loader.load_and_split()
        files += pages
    return files


def create_db(pages: list, chunk_size: int, embedding_model):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=200,
        length_function=len,
    )
    pages = text_splitter.split_documents(pages)
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    db = FAISS.from_documents(pages, embeddings)
    return db
