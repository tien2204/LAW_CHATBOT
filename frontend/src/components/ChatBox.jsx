import { useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown"; // <-- 1. Import thư viện

// Component Icon đơn giản
const UserIcon = () => <div className="w-8 h-8 rounded-full bg-green-500 flex-shrink-0"></div>;
const BotIcon = () => <div className="w-8 h-8 rounded-full bg-gray-800 flex-shrink-0"></div>;

export default function ChatBox({ messages, onPrompt }) {
  const input = useRef();
  const bottom = useRef();

  // Tự động cuộn xuống cuối
  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto px-4">
      {/* ===== Lịch sử chat ===== */}
      <div className="flex-1 overflow-y-auto py-8">
        {messages.length === 0 ? (
          <div className="text-center">
            <h1 className="text-3xl font-semibold text-gray-700">Law Chatbot</h1>
            <p className="text-gray-500 mt-2">Tôi có thể giúp gì cho bạn hôm nay?</p>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`flex items-start gap-4 ${m.role === "user" ? "justify-end" : ""}`}
              >
                {m.role === "bot" && <BotIcon />}
                <div
                  className={`px-4 py-2 rounded-lg max-w-[75%] whitespace-pre-wrap shadow-sm ${
                    m.role === "user"
                      ? "bg-green-100 text-gray-800 ml-auto"
                      : "bg-white text-gray-800"
                  }`}
                >
                  {/* ▼▼▼ 2. SỬ DỤNG REACT-MARKDOWN TẠI ĐÂY ▼▼▼ */}
                  {m.text ? (
                    <ReactMarkdown>{m.text}</ReactMarkdown>
                  ) : (
                    <span className="animate-pulse">...</span>
                  )}
                  {/* ▲▲▲ THAY THẾ CHO {m.text} ▲▲▲ */}
                </div>
                {m.role === "user" && <UserIcon />}
              </div>
            ))}
          </div>
        )}
        <div ref={bottom} />
      </div>

      {/* ===== Khung nhập liệu (giữ nguyên) ===== */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const q = input.current.value.trim();
          if (q) onPrompt(q);
          input.current.value = "";
        }}
        className="py-4"
      >
        <div className="relative">
          <input
            ref={input}
            className="w-full border rounded-lg px-4 py-3 pr-16 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
            placeholder="Hãy nhập câu hỏi pháp luật…"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Gửi
          </button>
        </div>
      </form>
    </div>
  );
}