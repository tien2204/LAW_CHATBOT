import { useRef, useEffect } from "react";

export default function ChatBox({ messages, onPrompt }) {
  const input = useRef();
  const bottom = useRef();

  // scroll cuối
  useEffect(() => bottom.current?.scrollIntoView({ behavior: "smooth" }), [messages]);

  return (
    <div className="flex flex-col h-full">
      {/* history */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`px-3 py-2 rounded-lg ${
              m.role === "user" ? "bg-green-100 ml-auto" : "bg-white mr-auto"
            } max-w-[75%] whitespace-pre-wrap`}
          >
            {m.text}
          </div>
        ))}
        <div ref={bottom} />
      </div>

      {/* input */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const q = input.current.value.trim();
          if (q) onPrompt(q);
          input.current.value = "";
        }}
        className="p-3 border-t flex"
      >
        <input
          ref={input}
          className="flex-1 border rounded-lg px-3 py-2 mr-2 outline-none"
          placeholder="Hãy nhập câu hỏi pháp luật…"
        />
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg">
          Gửi
        </button>
      </form>
    </div>
  );
}
