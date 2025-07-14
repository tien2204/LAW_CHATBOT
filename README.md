# 🇻🇳 VN-Law Chatbot (RAG) – Hệ thống hỏi đáp pháp luật Việt Nam

Chatbot sử dụng mô hình RAG (Retrieval-Augmented Generation) để trả lời các câu hỏi về pháp luật Việt Nam bằng cách truy xuất dữ liệu từ kho văn bản luật và tích hợp cùng mô hình ngôn ngữ lớn (LLM).

## 🧱 Kiến trúc hệ thống
- **Backend**: FastAPI + LangChain + ChromaDB (local vector store)
- **Frontend**: React + Vite + TailwindCSS + Three.js (giao diện 3D robot)
- **Embedding**: `paraphrase-multilingual-mpnet-base-v2`
- **LLM**: GPT-4o-mini hoặc Mixtral/Groq API
- **Reranker**: `bge-reranker-base`

---

## 📦 Yêu cầu hệ thống

| Thành phần | Ghi chú |
|-----------|--------|
| Python >= 3.10 | Khuyến nghị dùng 3.11 |
| Node.js >= 18 | Để chạy frontend |
| pip, venv | Dựng môi trường Python |
| Docker (tuỳ chọn) | Nếu muốn chạy toàn bộ bằng `docker-compose` |
| GPU (tuỳ chọn) | Tăng tốc embed |

---

## 🚀 Cài đặt & Chạy thử

### 🔁 1. Clone repository
```bash
git clone git@github.com:tien2204/LAW_CHATBOT.git
cd LAW_CHATBOT
```

### 🧠 2. Backend – FastAPI + LangChain
```bash
cd backend
cp .env.example .env             # điền GROQ_API_KEY (hoặc OPENAI_API_KEY) va SERP_API_KEY,
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python build_vector_db.py       # tạo vector store (~15–20 phút lần đầu)
uvicorn app.main:app --reload --port 8000
```

### 💬 3. Frontend – React + Vite + Tailwind
```bash
cd ../frontend
npm install
npm run dev                     # http://localhost:5173
```

### 🐳 Tuỳ chọn: Dùng Docker
```bash
docker-compose up --build
```

---

## 🧪 Giao diện thử nghiệm

- Giao diện web hiển thị khung chat + robot 3D có thể kéo thả
- Trả lời kèm điều/khoản luật – hiển thị ở cả khung chat và bong bóng robot
- Truy vấn ví dụ: `Thời hiệu khởi kiện hợp đồng dân sự là bao lâu?`

---

## 📁 Cấu trúc thư mục

```
vn-law-chatbot/
├── backend/
│   ├── app/
│   ├── build_vector_db.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── tailwind.config.js
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Tùy chỉnh nâng cao

### ✅ RAG-Hybrid
- Kết hợp Embedding ANN + BM25 → Rerank
- Hạn chế Hallucination
- Trả về nguồn trích dẫn như `[§Khoản 2 Điều 429]`

### 🌐 Fallback Web Search (tuỳ chọn)
- Khi không tìm thấy quy định, chatbot fallback sang SerpAPI
- Yêu cầu biến môi trường `SERPAPI_API_KEY` trong `.env`

---

## 🧾 Kiểm tra nhanh

| Lệnh | Kết quả mong đợi |
|------|------------------|
| `python --version` | Python 3.11.x |
| `node -v`           | v18 hoặc v20 |
| `curl http://localhost:8000/docs` | Swagger UI của FastAPI |
| Truy cập `http://localhost:5173` | Hiển thị chatbot và robot |

---

## 📘 Tham khảo

- [Vietnamese Law Corpus (HuggingFace)](https://huggingface.co/datasets/clapAI/vietnamese-law-corpus)
- [LangChain RAG](https://docs.langchain.com/docs/use-cases/question-answering)
- [ChromaDB](https://www.trychroma.com/)
- [Groq API](https://console.groq.com)

---

> Nếu bạn gặp lỗi `ModuleNotFoundError` → kiểm tra lại đường dẫn file, đúng thư mục, và đã kích hoạt môi trường ảo.
