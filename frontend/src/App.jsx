import { useState, useRef, useEffect } from "react";
import ChatBox from "./components/ChatBox.jsx";
import Robot from "./components/Robot.jsx";

export default function App() {
  const [messages, setMsgs] = useState([]);

  // thêm tin nhắn
  const push = (role, text) =>
    setMsgs((m) => [...m, { role, text }]);

  // gửi prompt tới /stream (SSE)
  const send = (prompt) => {
    push("user", prompt);
    push("bot", ""); // tạo tin nhắn bot
  
    const ev = new EventSource(`/stream?q=${encodeURIComponent(prompt)}`);
    let answer = "";
  
    ev.onmessage = (e) => {
      answer += e.data;
  
      if (answer.endsWith("[CITATIONS]") || answer.endsWith("]")) return;
  
      setMsgs(prev => {
        const last = prev.at(-1);
        if (!last || last.role !== "bot") return prev;
        const updated = [...prev];
        updated[updated.length - 1] = { ...last, text: answer };
        return updated;
      });
    };
  
    ev.onerror = () => ev.close();
    ev.addEventListener("end", () => ev.close());
  };
  


  return (
    <div className="h-screen flex bg-neutral-100">
      {/* Left – Robot */}
      <div className="w-1/2 relative overflow-hidden">
        <Robot lastBotMsg={messages.filter(m=>m.role==='bot').at(-1)?.text}/>
      </div>

      {/* Right – Chat */}
      <div className="w-1/2 border-l flex flex-col">
        <ChatBox messages={messages} onPrompt={send}/>
      </div>
    </div>
  );
}
