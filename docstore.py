import os
import hashlib
import os
import pymongo

MONGO_COLLECTION = "transcripts"
CHUNK_SIZE = 250


def get_documents(client, db="docs", collection=MONGO_COLLECTION):
    db = client.get_database(db)
    collection = db.get_collection(collection)
    docs = collection.find()
    return docs


def get_database() -> pymongo.MongoClient:
    mongodb_password = os.environ["MONGODB_PASSWORD"]
    mongodb_uri = os.environ["MONGODB_URI"]
    connection_string = f"mongodb+srv://dbSoftwareTesting:{mongodb_password}@{mongodb_uri}/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string)
    return client


def upload_docs(
    client: pymongo.MongoClient,
    offline_dir: str,
    version: str,
    db: str = "docs",
    collection: str = MONGO_COLLECTION,
    chunk_size: int = CHUNK_SIZE,
) -> None:
    db = client.get_database(db)
    collection = db.get_collection(collection)
    requesting = []
    for item in os.listdir(offline_dir):
        with open(os.path.join(offline_dir, item), "r") as f:
            text = f.readlines()
        text = [line.strip() for line in text]
        text = " ".join(text)

        metadata = {}
        m = hashlib.sha256()
        m.update(text.encode("utf-8"))
        metadata["sha256"] = m.hexdigest()
        metadata["version"] = version
        metadata["source"] = item
        document = {"text": text, "metadata": metadata}
        requesting.append(pymongo.InsertOne(document=document))

        if len(requesting) >= chunk_size:
            collection.bulk_write(requesting)
            requesting = []
    if requesting:
        collection.bulk_write(requesting)
        requesting = []


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    db_client = get_database()
    upload_docs(db_client, "data/transcript", "base")
