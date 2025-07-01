from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from .config import get_settings

_settings = get_settings()

emb = HuggingFaceEmbeddings(model_name=_settings.embed_model)

vectordb = Chroma(
    persist_directory=_settings.chroma_dir,
    collection_name=_settings.collection_name,
    embedding_function=emb,
)
