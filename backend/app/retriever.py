"""
Hybrid retrieval  = 0.7 * EmbeddingSim  + 0.3 * BM25
Sau đó Encoder rerank  →  trả về (doc, score)
"""
from typing import List, Tuple
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from FlagEmbedding import FlagReranker
from langchain.docstore.document import Document
from .db import vectordb

# 1) ANN
_ann = vectordb.as_retriever(search_kwargs={"k": 12})

# 2) BM25 (dùng chính corpus)
_bm25 = BM25Retriever.from_documents(
    [Document(page_content=d)
     for d in vectordb.get(include=["documents"])["documents"]]
)
_bm25.k = 12

# 3) Hybrid
_hybrid = EnsembleRetriever(retrievers=[_ann, _bm25], weights=[0.7, 0.3])

"""
from .config import get_settings
from FlagEmbedding import FlagReranker

SET = get_settings()

_reranker = FlagReranker(
    model_name_or_path=SET.rerank_model,
    use_fp16=True
)

Dong bo ten model voi phan 4 neu muon dung model tu file config.py
"""
# 4) Encoder reranker
_reranker = FlagReranker(
    model_name_or_path="BAAI/bge-reranker-v2-m3",
    use_fp16=True
)

def hybrid_retrieve(query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
    docs = _hybrid.get_relevant_documents(query)
    ranked = _reranker.rerank(query, docs, top_n=top_k, return_sorted=True)
    return [(d, s) for d, s in ranked]           # k tài liệu + điểm
