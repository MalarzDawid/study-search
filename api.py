import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from pydantic import BaseModel

import utils
import vecstore


# Simple query model
class Query(BaseModel):
    query: str


def main():
    app = FastAPI()
    load_dotenv()

    # Download or load OpenAI embeddings
    cache_dir = Path(os.environ["CACHE_DIR"])
    if os.path.exists(cache_dir):
        if os.path.exists(cache_dir / os.environ["EMBEDDINGS_PICKLE"]):
            embedding_engine = utils.load_pickle(
                cache_dir / os.environ["EMBEDDINGS_PICKLE"]
            )
            db = vecstore.connect_to_vector_db(
                os.environ["INDEX_NAME"], embedding_engine
            )
        else:
            raise FileExistsError(f"Problem with {os.environ['EMBEDDINGS_PICKLE']}")
    else:
        import docstore

        cache_dir = (
            Path(os.path.join("data", "cache")) if cache_dir == "" else cache_dir
        )
        os.makedirs(cache_dir, exist_ok=True)
        embedding_engine = vecstore.get_openai_embedding_engine()
        utils.save_pickle(embedding_engine, cache_dir / "emb.pkl")
        db_client = docstore.get_database()
        docs = docstore.get_documents(db_client)
        docs, metadatas = vecstore.prep_documents_for_vecstore(docs)
        db = vecstore.create_vector_db(
            os.environ["INDEX_NAME"], embedding_engine, docs, metadatas, save=True
        )

    llm = OpenAI(model_name=os.environ["LLM_MODEL"])
    chain = load_qa_with_sources_chain(llm, chain_type="stuff")

    @app.post("/query")
    def get_answer(query: Query):
        sources = db.similarity_search(query.query, k=5)
        result = chain(
            {"input_documents": sources, "question": query.query},
            return_only_outputs=True,
        )
        answer = result["output_text"]
        return {"answer": answer, "q": query.query}

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
