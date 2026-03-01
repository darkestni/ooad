
// src/hooks/useTypingEffect.js

import { useState, useEffect } from "react";

/**
 * ChatGPT 风格逐字打字效果 Hook
 * @param {string} fullText 完整文本
 * @param {number} speed 每个字间隔（毫秒）
 */
export default function useTypingEffect(fullText, speed = 30) {
  const [typingText, setTypingText] = useState("");

  useEffect(() => {
    if (!fullText || fullText.length === 0) {
      setTypingText("");
      return;
    }

    let index = 0;
    setTypingText(""); // 每次开始前清空

    const interval = setInterval(() => {
      setTypingText((prev) => prev + fullText[index]);
      index++;

      if (index >= fullText.length) clearInterval(interval);
    }, speed);

    return () => clearInterval(interval);
  }, [fullText, speed]);

  return typingText;
}
