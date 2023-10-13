""" postgresql setting """
import tiktoken
import os
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.vectorstores.pgvector import PGVector
from dotenv import load_dotenv
from db.provider import Provider
from utils import util
from core.config import SentenceTransformerConfig

class PGVectorProvider(Provider):
    """pgvector class"""
    def __init__(self, embeddings):
        self.chunk_size = 100
        # 取 10% 的overlap
        self.chunk_overlap = self.chunk_size//10
        self.embeddings = embeddings
    
    def get_db_obj(self, pgvector_config, collection_name):

        store = PGVector(connection_string=pgvector_config, embedding_function=self.embeddings, collection_name=collection_name)
        return store

    def get_pgvector_config(self):
        load_dotenv()
        connection_setting = PGVector.connection_string_from_db_params(
            driver=os.getenv('DRIVER'),
            host=os.getenv('HOST'),
            port=int(os.getenv('PORT')),
            database=os.getenv('DATABASE'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
        )
        return connection_setting

    def update_data(self, docs, collection_name, pgvector_config: str, delete_collection: bool = False):
        PGVector.from_documents(
            documents= docs,
            embedding = self.embeddings,
            collection_name= collection_name,
            distance_strategy = DistanceStrategy.COSINE,
            connection_string= pgvector_config,
            pre_delete_collection= delete_collection)
    
    def delete_collection(self, store):

        try:
            store.delete_collection()
            return True
        except Exception as err:
            print(f"{err}")
            return False
    
    def num_tokens_from_string(self, string: str, encoding_name = "cl100k_base"):

        if not string:
            return 0

        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    def chunk_data_to_docs(self, filename, embedding_type):

        data_frame = self.read_csv(filename = filename)
        new_list = []
        for i in range(len(data_frame.index)):
            text = data_frame['content'][i]
            text_splitter = self.get_text_splitter(self.chunk_size, self.chunk_overlap)
            split_text = text_splitter.split_text(text)
            for split_pass in split_text:
                if embedding_type == 'e5':
                    split_pass = "passage:" + split_pass
                new_list.append([data_frame['title'][i],
                    "passage:" + split_pass,
                    data_frame['link'][i]])
        
        return self.get_docs(new_list, ['title', 'content', 'url'])
        

sbert_embeddings = util.set_embedding(SentenceTransformerConfig.model)
PGVector_obj = PGVectorProvider(sbert_embeddings)
