import React from "react";
import "./MessageList.css";
import { Avatar } from "antd";
import { UserOutlined, RobotOutlined } from "@ant-design/icons";

export default function MessageList({ messages, isTyping, t }) {
  return (
    <div className="message-list-wrapper">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`chat-msg ${msg.sender === "user" ? "user" : "ai"}`}
        >
          {/* 左侧 AI 头像 */}
          {msg.sender === "ai" && (
            <Avatar
              className="avatar"
              icon={<RobotOutlined />}
              style={{ backgroundColor: "#4f67ff" }}
            />
          )}

          {/* 气泡 */}
          <div className="bubble">{msg.text}</div>

          {/* 用户头像在右侧 */}
          {msg.sender === "user" && (
            <Avatar
              className="avatar"
              icon={<UserOutlined />}
              style={{ backgroundColor: "#3da5ff" }}
            />
          )}
        </div>
      ))}

      {/* AI 输入中 */}
      {isTyping && (
        <div className="chat-msg ai">
          <Avatar
            className="avatar"
            icon={<RobotOutlined />}
            style={{ backgroundColor: "#4f67ff" }}
          />
          {/* 保持你原本的“···” */}
          <div className="bubble typing">···</div>
        </div>
      )}
    </div>
  );
}
