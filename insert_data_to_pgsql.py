""" CRUD function """
import os
from db.pgvector_provider import PGVector_obj
from dotenv import load_dotenv

def insert_data_to_postgresql(file_name:str, collection_name: str, delete_collection: bool):
    docs = PGVector_obj.chunk_data_to_docs(file_name, embedding_type='e5')
    db_config = PGVector_obj.get_pgvector_config()
    PGVector_obj.update_data(docs=docs, collection_name=collection_name, pgvector_config=db_config, delete_collection=delete_collection)


if __name__ == "__main__":
    load_dotenv()
    insert_data_to_postgresql('./data/mental_article.csv', os.getenv('COLLECTION_NAME'), True)
