""" base provider class """
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DataFrameLoader

class Provider:
    """ base class """

    def read_csv(self, filename: str):
        """ get dataframe from csv """
        return pd.read_csv(filename)
    
    def get_docs(self, data_list, header):
        """ get dataframe """
        new_df = pd.DataFrame(data_list, columns=header)
        loader = DataFrameLoader(new_df, page_content_column = 'content')
        docs = loader.load()

        return docs

    def get_text_splitter(self, chunk_size, chunk_overlap):
        """ get langchain spliter obj """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap  = chunk_overlap,
            length_function = len
        )

        return text_splitter
    
    