// ===============================================
// ChatPage.js — Final Stable Version (Auto-Preserve Token + i18n)
// ===============================================

import React, { useState, useEffect } from "react";
import {
  Layout,
  message,
  Modal,
  Tabs,
  Slider,
  Switch,
  Button,
} from "antd";

import AppHeader from "../components/AppHeader";
import Sidebar from "../components/Sidebar";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";

import { askQuestion, uploadTextbook } from "../services/api";
import { postJSON } from "../services/api";

import useTypingEffect from "../hooks/useTypingEffect";

import { translations } from "../i18n"; // ⭐ 多语言
import "./ChatPage.css";

const { Sider, Content } = Layout;
const HEADER_HEIGHT = 72;

export default function ChatPage() {
  const token = localStorage.getItem("token");

  // 语言
  const lang = localStorage.getItem("lang") || "zh";
  const t = translations[lang];

  // 主题
  const [theme, setTheme] = useState(
    localStorage.getItem("theme") || "cosmic"
  );

  const toggleTheme = () => {
    const next = theme === "light" ? "cosmic" : "light";
    setTheme(next);
    localStorage.setItem("theme", next);
  };

  // 设置弹窗
  const [settingsVisible, setSettingsVisible] = useState(false);

  // 聊天
  const [messages, setMessages] = useState([]);
  const [aiFullReply, setAiFullReply] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);


  const typingText = useTypingEffect(
    isTyping ? aiFullReply : "",
    isTyping ? 10 : null
  );

  // ============================
  // 加载历史消息
  // ============================
  useEffect(() => {
    async function loadHistory() {
      try {
       const res = await postJSON("/question", {
            token,
            text: "history",
            images: []
          });
        if (res.type === "history" && Array.isArray(res.content)) {
          const list = res.content.map((m, index) => {
            let text = "";

            if (Array.isArray(m.payload)) {
              text = m.payload[0]?.text || "";
            } else if (typeof m.payload === "object" && m.payload !== null) {
              text = m.payload.text || "";
            } else {
              text = String(m.payload || "");
            }

            return {
              id: index,
              sender: m.role === "LLM" ? "ai" : "user",
              text,
            };
          });

          setMessages(list);
        }
      } catch (err) {
        console.log("加载历史失败：", err);
      }
    }

    loadHistory();
  }, [token]);

  // ============================
  // 打字机效果更新消息
  // ============================
  useEffect(() => {
    if (!isTyping || typingText === "") return;

    setMessages((prev) => {
      const list = [...prev];
      list[list.length - 1].text = typingText;
      return list;
    });

    if (typingText === aiFullReply) {
      setIsTyping(false);
    }
  }, [typingText, isTyping, aiFullReply]);

  // ============================
  // 星空动画
  // ============================
  useEffect(() => {
    if (theme !== "cosmic") return;
    const stars = document.getElementById("chat-stars");
    if (!stars) return;

    const ctx = stars.getContext("2d");

    function resize() {
      stars.width = window.innerWidth;
      stars.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    const starList = Array.from({ length: 130 }).map(() => ({
      x: Math.random() * stars.width,
      y: Math.random() * stars.height,
      r: Math.random() * 1.2 + 0.3,
    }));

    let frameId;
    function animate() {
      ctx.clearRect(0, 0, stars.width, stars.height);
      ctx.fillStyle = "#fff";

      starList.forEach((s) => {
        ctx.globalAlpha = 0.4 + Math.random() * 0.6;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
      });

      frameId = requestAnimationFrame(animate);
    }
    animate();

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener("resize", resize);
    };
  }, [theme]);

  // ============================
  // 发送消息
  // ============================
  const handleSendMessage = async (text) => {
  if (!text.trim()) return;

  setMessages((prev) => [
    ...prev,
    { id: Date.now(), sender: "user", text },
  ]);

  setIsTyping(true);

  // ⭐ 使用你自己的 API
  const res = await postJSON("/question", {
    token,
    text,
    images: []
  });

  if (!res.success) {
    setIsTyping(false);
    return message.error("AI 回复失败");
  }

  const aiText = res.msg || "";

  setMessages((prev) => [
    ...prev,
    { id: Date.now() + 1, sender: "ai", text: "" },
  ]);

  setAiFullReply(aiText);
};


  // ============================
  // 上传教材
  // ============================
  const handleUploadTextbook = async (file) => {
  const token = localStorage.getItem("token");

  const formData = new FormData();
  formData.append("token", token);
  formData.append("file", file);  // ⭐关键：直接把 File 对象放入 FormData

  try {
    const res = await fetch("http://localhost:8080/api/upload-textbook", {
      method: "POST",
      body: formData, // ⭐ 不要写 Content-Type，让浏览器自动加 boundary
    });

    const data = await res.json();

    if (data.success) {
      message.success("上传成功");

      // 写入本地文件列表（前端展示用）
      setUploadedFiles((prev) => [
        ...prev,
        { name: file.name, size: file.size }
      ]);
    } else {
      message.error("上传失败: " + data.msg);
    }
  } catch (err) {
    message.error("上传失败");
  }
};

const handleDeleteFile = async (file) => {
  const token = localStorage.getItem("token");

  const res = await postJSON("/delete-textbook", {
    token,
    path: file.name   // ⭐ 必须是 path，符合你的 API
  });

  if (res.success) {
    message.success("删除成功");
    setUploadedFiles((prev) => prev.filter((f) => f.name !== file.name));
  } else {
    message.error("删除失败");
  }
};





  // ============================
  // ⭐ 语言切换（自动保留 token）
  // ============================
  const handleLanguageChange = (value) => {
    const oldToken = localStorage.getItem("token");

    localStorage.setItem("lang", value);

    // ⭐ 刷新前重新写回 token，保证不会丢失
    setTimeout(() => {
      localStorage.setItem("token", oldToken);
      window.location.reload();
    }, 10);
  };

  // ============================
  // ⭐ 清除缓存（保留 token）
  // ============================
  const handleClearCache = () => {
    const tk = localStorage.getItem("token");

    localStorage.clear();
    localStorage.setItem("token", tk); // ⭐ 保留 token

    window.location.reload();
  };

  return (
    <Layout className={`chat-page ${theme}`}>
      {theme === "cosmic" && <canvas id="chat-stars"></canvas>}

     {/* Header */}
<AppHeader
  theme={theme}
  toggleTheme={toggleTheme}
  onOpenSettings={() => setSettingsVisible(true)}
  t={t}
/>

      {/* 主体 */}
      <Layout style={{ paddingTop: HEADER_HEIGHT }}>
      <Sider width={260} className="chat-sider">
 <Sidebar
  uploadedFiles={uploadedFiles}
  onUploadTextbook={handleUploadTextbook}
  onDeleteFile={handleDeleteFile}
  theme={theme}
  t={t}
/>


</Sider>
      <Content className="chat-content">
  <MessageList
    messages={messages}
    isTyping={localStorage.getItem("typing-indicator") !== "off" && isTyping}
    typingText={typingText}
    t={t}
  />
  <MessageInput
    onSendMessage={handleSendMessage}
    theme={theme}
    t={t}
  />
</Content>
      </Layout>

      {/* ============================
          ⭐ 设置弹窗 Modal
      ============================ */}
      <Modal
        title={t.settings}
        open={settingsVisible}
        onCancel={() => setSettingsVisible(false)}
        footer={null}
        centered
        width={520}
        style={{
          backdropFilter: "blur(18px)",
        }}
        bodyStyle={{
          paddingTop: 0,
          paddingBottom: 20,
          background:
            theme === "light"
              ? "rgba(255,255,255,0.7)"
              : "rgba(30,30,40,0.65)",
          backdropFilter: "blur(16px)",
          WebkitBackdropFilter: "blur(16px)",
          color: theme === "cosmic" ? "#e9ecff" : "#333",
          borderRadius: 12,
        }}
      >
        <Tabs
          defaultActiveKey="appearance"
          items={[
            // ===================== 外观 =====================
            {
              key: "appearance",
              label: t.appearance,
              children: (
                <>
                  <div className="setting-item">
                    <span>{t.themeMode}</span>
                    <Switch
                      checked={theme === "cosmic"}
                      checkedChildren="宇宙"
                      unCheckedChildren="明亮"
                      onChange={toggleTheme}
                    />
                  </div>

                  <div className="setting-item">
                    <span>{t.fontSize}</span>
                    <Slider
                      min={14}
                      max={26}
                      defaultValue={16}
                      onChange={(v) =>
                        document.documentElement.style.setProperty(
                          "--chat-font",
                          v + "px"
                        )
                      }
                    />
                  </div>

                  <div className="setting-item">
                    <span>{t.chatWidth}</span>
                    <Slider
                      min={70}
                      max={100}
                      defaultValue={80}
                      onChange={(v) =>
                        document.documentElement.style.setProperty(
                          "--chat-width",
                          v + "%"
                        )
                      }
                    />
                  </div>

                  <div className="setting-item">
                    <span>{t.bubbleStyle}</span>
                    <select
                      className="select-input"
                      defaultValue={
                        localStorage.getItem("bubble-style") || "round"
                      }
                      onChange={(e) =>
                        localStorage.setItem("bubble-style", e.target.value)
                      }
                    >
                      <option value="round">圆角</option>
                      <option value="flat">直角</option>
                      <option value="neon">霓虹</option>
                    </select>
                  </div>
                </>
              ),
            },

            // ===================== 聊天设置 =====================
            {
              key: "chat",
              label: t.chatSettings,
              children: (
                <>
                  <div className="setting-item">
                    <span>{t.showTimestamp}</span>
                    <Switch
                      defaultChecked={
                        localStorage.getItem("show-timestamp") !== "off"
                      }
                      onChange={(v) =>
                        localStorage.setItem(
                          "show-timestamp",
                          v ? "on" : "off"
                        )
                      }
                    />
                  </div>

                  <div className="setting-item">
                    <span>{t.showAvatar}</span>
                    <Switch
                      defaultChecked={
                        localStorage.getItem("show-avatar") !== "off"
                      }
                      onChange={(v) =>
                        localStorage.setItem(
                          "show-avatar",
                          v ? "on" : "off"
                        )
                      }
                    />
                  </div>

                  <div className="setting-item">
                    <span>{t.showTyping}</span>
                    <Switch
                      defaultChecked={
                        localStorage.getItem("typing-indicator") !== "off"
                      }
                      onChange={(v) =>
                        localStorage.setItem(
                          "typing-indicator",
                          v ? "on" : "off"
                        )
                      }
                    />
                  </div>
                </>
              ),
            },

            // ===================== 语言 =====================
            {
              key: "language",
              label: t.language,
              children: (
                <div className="setting-item">
                  <span>{t.uiLanguage}</span>
                  <select
                    className="select-input"
                    defaultValue={lang}
                    onChange={(e) => handleLanguageChange(e.target.value)}
                  >
                    <option value="zh">中文</option>
                    <option value="en">English</option>
                  </select>
                </div>
              ),
            },

            // ===================== 数据管理 =====================
            {
              key: "data",
              label: t.data,
              children: (
                <>
                  <Button danger block onClick={() => setMessages([])}>
                    {t.clearMessages}
                  </Button>

                  <Button
                    block
                    style={{ marginTop: 12 }}
                    onClick={handleClearCache}
                  >
                    {t.clearCache}
                  </Button>
                </>
              ),
            },

            // ===================== 账户 =====================
            {
              key: "account",
              label: t.account,
              children: (
                <>
                  <Button
                    block
                    type="primary"
                    style={{ background: "#7b8cff", border: "none" }}
                    onClick={() => {
                      localStorage.removeItem("token");
                      message.success(
                        lang === "zh" ? "已退出登录" : "Logged out"
                      );
                      window.location.href = "/login";
                    }}
                  >
                    {t.logout}
                  </Button>

                  <p style={{ opacity: 0.7, marginTop: 18 }}>
                    Intelligent Learning Assistant  
                    <br />
                    {t.version} 1.0.0
                  </p>
                </>
              ),
            },
          ]}
        />
      </Modal>
    </Layout>
  );
}
