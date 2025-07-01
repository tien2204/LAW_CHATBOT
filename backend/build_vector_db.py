"""
Chạy một lần để tạo Chroma vector store:  python build_vector_db.py
"""
import pathlib, tqdm, os
from datasets import load_dataset
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from app.config import get_settings

SET = get_settings()
DB_DIR = pathlib.Path(SET.chroma_dir)

print(">> Tải corpora …")
ds = load_dataset("clapAI/vietnamese-law-corpus", split="train")
# ví dụ demo lấy 30k đoạn; sửa theo máy
LIMIT = 30_000
docs_raw = [d["content"] for d in ds.select(range(min(LIMIT, len(ds))))]

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
chunks = sum([splitter.split_text(t) for t in tqdm.tqdm(docs_raw)], [])

print(f">> Tổng chunk: {len(chunks):,}")

emb = HuggingFaceEmbeddings(model_name=SET.embed_model)
vectors = emb.embed_documents(chunks)

client = chromadb.PersistentClient(path=str(DB_DIR))
col = client.get_or_create_collection(SET.collection_name)
col.add(ids=[f"id_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors)
print("✅  Chroma vector store created.")

