// ================================================
// ProtectedRoute.js — Final Safe Version
// ================================================
import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const [ready, setReady] = useState(false);
  const [authed, setAuthed] = useState(false);

  useEffect(() => {
    // ⭐ 延迟判断，等待 localStorage 完全可用
    setTimeout(() => {
      const token = localStorage.getItem("token");

      if (token && token !== "null" && token !== "") {
        setAuthed(true);
      }

      setReady(true);
    }, 30); // 30ms 最稳定
  }, []);

  // ⭐ 第一次不要急着跳转，等 token 判定完毕
  if (!ready) return null;

  return authed ? children : <Navigate to="/login" replace />;
}
