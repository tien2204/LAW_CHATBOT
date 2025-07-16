"""
Chạy một lần để tạo Chroma vector store:  python build_vector_db.py
"""
import pathlib, tqdm, os
from datasets import load_dataset
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from app.config import get_settings

SET = get_settings()
DB_DIR = pathlib.Path(SET.chroma_dir)

print(">> Tải corpora …")
ds = load_dataset("clapAI/vietnamese-law-corpus", split="train")
# ví dụ demo lấy 30k đoạn; sửa theo máy
LIMIT = 30000
docs_raw = [d["content"] for d in ds.select(range(min(LIMIT, len(ds))))]

splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
chunks = sum([splitter.split_text(t) for t in tqdm.tqdm(docs_raw)], [])

print(f">> Tổng chunk: {len(chunks):,}")

print(">> Khởi tạo HuggingFaceEmbeddings …")
emb = HuggingFaceEmbeddings(model_name=SET.embed_model)
print(">> Đã khởi tạo xong.")

print(">> Bắt đầu tạo embedding cho các chunk …")
vectors = emb.embed_documents(chunks)
print(">> Tạo xong embedding.")

client = chromadb.PersistentClient(path=str(DB_DIR))

# Xoá collection nếu đã tồn tại
try:
    client.delete_collection(SET.collection_name)
except Exception as e:
    print(f"Warning: {e}")

# Tạo collection mới
col = client.get_or_create_collection(SET.collection_name)
BATCH_SIZE = 40000  # dưới ngưỡng 41666
for i in range(0, len(chunks), BATCH_SIZE):
    batch_chunks = chunks[i:i+BATCH_SIZE]
    batch_vectors = vectors[i:i+BATCH_SIZE]
    batch_ids = [f"id_{j}" for j in range(i, i+len(batch_chunks))]

    col.add(
        ids=batch_ids,
        documents=batch_chunks,
        embeddings=batch_vectors
    )

print("✅  Chroma vector store created.")

