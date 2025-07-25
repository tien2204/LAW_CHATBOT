import { useState } from "react";
import ChatBox from "./components/ChatBox.jsx";
import Robot from "./components/Robot.jsx";

export default function App() {
  const [messages, setMsgs] = useState([]);

  // Hàm gửi prompt đến server và nhận phản hồi
  const send = (prompt) => {
    setMsgs((prev) => [...prev, { role: "user", text: prompt }]);
    setMsgs((prev) => [...prev, { role: "bot", text: "" }]);

    const ev = new EventSource(`/stream?q=${encodeURIComponent(prompt)}`);

    ev.onmessage = (e) => {
      if (e.data.includes("[CITATIONS]")) {
        ev.close();
        return;
      }
      setMsgs((prev) => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1].text += e.data;
        return newMsgs;
      });
    };
    ev.onerror = () => ev.close();
  };

  return (
    // Dùng flex cho layout chính
    <div className="h-screen w-full flex bg-[#F9F9F9]">
      {/* ===== Panel Robot (Trái) ===== */}
      {/* Cho panel này một màu nền riêng và chiếm 1/3 không gian */}
      <div className="w-1/3 bg-gray-800 relative overflow-hidden hidden md:block">
        <Robot lastBotMsg={messages.filter((m) => m.role === "bot").at(-1)?.text} />
      </div>

      {/* ===== Panel Chat (Phải) ===== */}
      {/* Panel này chiếm phần không gian còn lại */}
      <div className="w-full md:w-2/3 flex flex-col">
        <ChatBox messages={messages} onPrompt={send} />
      </div>
    </div>
  );
}