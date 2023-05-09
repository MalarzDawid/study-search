from fastapi import FastAPI
from schema import StoreQuery
from utils import load_config, postprocessing
from utils import create_db, load_pages


config = load_config("config.yaml")

# Prepare dataset
pages = load_pages(config["DATA_DIR"])
db = create_db(pages, config["CHUNK_SIZE"], config["MODEL_EMBEDDINGS"])


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def store_query(q: StoreQuery, k: int = 4):
    try:
        docs = db.similarity_search(q.query, k=k)
        output = postprocessing(docs)
        return output
    except Exception as e:
        return {"Error": f"{e}"}
