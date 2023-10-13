""" config setting """
import os 
from dotenv import load_dotenv

load_dotenv()

class KindOfPrompt:
    """ prompt config """
    multi_QA_prompt =  "{Instruction}\n{document}\nQuestion: {question}\nAnswer:"

class SentenceTransformerConfig:
    """ sentence transformer config """
    model = os.getenv("EMBEDDING_MODEL")

class LlmConfig:
    """ llama 2 setting """
    model = os.getenv("GGML_MODEL")

class RetrivevalConfig:
    """ retrieval setting """
    top_k = 3
