import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from pydantic import BaseModel

import vecstore


# Simple query model
class Query(BaseModel):
    query: str


def main():
    app = FastAPI()
    load_dotenv()

    embedding_engine = vecstore.get_openai_embedding_engine()
    db = vecstore.connect_to_vector_db(os.environ["INDEX_NAME"], embedding_engine)
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
