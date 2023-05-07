from pydantic import BaseModel


class StoreQuery(BaseModel):
    query: str
