# LAW_CHATBOT
## 1️⃣ Backend
```bash
cd backend
cp .env.example .env        # điền GROQ_API_KEY
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
python build_vector_db.py   # ~15‑20' lần đầu
uvicorn app.main:app --reload --port 8000
```
2️⃣ Frontend
```bash
cd ../frontend
npm i
npm run dev
```
Truy cập http://localhost:5173
 Kéo thả robot 3‑D; đặt câu hỏi – hệ thống sẽ trích điều/khoản và hiển thị song song ở bong bóng robot + khung chat.
