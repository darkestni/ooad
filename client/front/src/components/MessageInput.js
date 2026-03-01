import React, { useState } from "react";
import { Input, Button } from "antd";
import { SendOutlined } from "@ant-design/icons";

export default function MessageInput({ onSendMessage, disabled, theme, t }) {
  const [text, setText] = useState("");

  const send = () => {
    if (!text.trim()) return;
    onSendMessage(text);
    setText("");
  };

  return (
    <div
      className="message-input-wrapper"
      style={{
        display: "flex",
        padding: 12,
        borderRadius: 14,
        backdropFilter: "blur(12px)",
        background:
          theme === "light"
            ? "rgba(255,255,255,0.55)"
            : "rgba(20,20,20,0.55)",
        border:
          theme === "light"
            ? "1px solid rgba(200,220,255,0.6)"
            : "1px solid rgba(255,255,255,0.15)",
      }}
    >
      {/* 输入框 */}
      <Input
        size="large"
        value={text}
        placeholder={t.inputPlaceholder}   // ⭐ 国际化 placeholder
        onPressEnter={send}
        disabled={disabled}
        onChange={(e) => setText(e.target.value)}
        style={{
          borderRadius: 10,
          background: theme === "light" ? "#ffffff" : "#2a2a33",
        }}
      />

      {/* 发送按钮 */}
      <Button
        type="primary"
        disabled={disabled}
        icon={<SendOutlined />}
        onClick={send}
        style={{
          marginLeft: 12,
          padding: "0 22px",
          borderRadius: 10,
          background:
            theme === "light"
              ? "linear-gradient(135deg,#6ea8ff,#a181ff)"
              : "linear-gradient(135deg,#4c8eff,#6a5cff,#3778ff)",
          border: "none",
        }}
      >
        {t.send}   {/* ⭐ 国际化按钮 */}
      </Button>
    </div>
  );
}
