from langchain.retrievers import BM25Retriever, EnsembleRetriever
from flag_embedding import BGEM3CrossEncoderReranker
from langchain.docstore.document import Document
from .db import vectordb

# 1) ANN từ Chroma
ann = vectordb.as_retriever(search_kwargs={"k": 8})

# 2) BM25 fallback (tạo từ chính documents của Chroma)
bm25 = BM25Retriever.from_documents(
    [Document(page_content=d)
     for d in vectordb.get(include=["documents"])["documents"]]
)
bm25.k = 10

# 3) Ensemble
ens = EnsembleRetriever(retrievers=[ann, bm25], weights=[0.7, 0.3])

# 4) Cross‑encoder rerank (top_n=5)
reranker = BGEM3CrossEncoderReranker(model_name="BAAI/bge-reranker-base")

def retrieve(query: str, top_k: int = 5):
    docs = ens.get_relevant_documents(query)
    return reranker.rerank(query, docs, top_n=top_k)

