""" Util function """
import os
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import LlamaCpp
from core.config import RetrivevalConfig

def set_prompt(prompt_type: str):
    """you can change your prompt formet from config"""
    prompt = PromptTemplate.from_template(prompt_type)
    return prompt

def set_embedding(embedding_model):
    """ set Embedding model """
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model,
        model_kwargs={'device': 'cpu'}
    )
    return embeddings

def get_llm(model_path: str, temp, max_tokens, top_p, top_k, context_len):
    """ set LLM model """
    llm = LlamaCpp(model_path=model_path,
                temperature = temp,
                max_tokens = max_tokens,
                top_p = top_p,
                top_k = top_k,
                n_ctx = context_len
                )
    return llm

def get_db():
    """ set PGVector """
    from db import pgvector_provider
    connection_setting = pgvector_provider.PGVector_obj.get_pgvector_config()
    store = pgvector_provider.PGVector_obj.get_db_obj(pgvector_config=connection_setting, collection_name=os.getenv('COLLECTION_NAME'))

    return store

def get_retrieval_doc(store, query):
    query = 'query:'+query
    docs = store.similarity_search_with_score(
        query, k = RetrivevalConfig.top_k)

    return docs


def combine_doc_query(docs, query, prompt):
    documents = ''
    content_title = []
    content_link = []
    instruction = 'Write an accurate, engaging, and concise answer for the given question using only the provided search results (some of which might be irrelevant). Use an unbiased and journalistic tone.'
    count = 1

    for text, score in docs:
        print(score)
        passage = text.page_content
        passage = passage.split("passage:")[-1]
        documents += f"Document [{count}] " + passage + '\n'
        if text.metadata['title'] not in content_title:
            content_title.append(text.metadata['title'])
            content_link.append(text.metadata['url'])
        count += 1

    query = query.split('query:')[-1]

    prompt_add_query = prompt.format(
        Instruction=instruction, document=documents, question=query)

    return prompt_add_query, content_title, content_link


def get_response(query, db_config, llm_model, prompt_formet):
    docs = get_retrieval_doc(db_config, query)
    final_prompt, title, link = combine_doc_query(docs, query, prompt_formet)
    ans = llm_model(final_prompt)

    response = ans + "\n---\n參考資料：\n"

    for i in range(len(title)):
        response += f"[{i+1}] " + title[i] + " 連結: " + link[i]

    return response
