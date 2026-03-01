// src/pages/RegisterPage.js
import React, { useState, useEffect, useRef } from "react";
import { Input, Button, message } from "antd";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";
import { postJSON } from "../services/api";


import "./AuthPage.css";

const PHONE_REG = /^1[3-9]\d{9}$/;

const RegisterPage = () => {
  const [phone, setPhone] = useState("");
  const [safePhone, setSafePhone] = useState("");
  const [showRawPhone, setShowRawPhone] = useState(false); // 显示 / 隐藏

  const [isPhoneValid, setIsPhoneValid] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const navigate = useNavigate();

  // 星空背景（保持你的样式）
  const starCanvas = useRef(null);
  const meteorCanvas = useRef(null);
  const nebulaCanvas = useRef(null);
  const particleCanvas = useRef(null);

  useEffect(() => {
    setIsPhoneValid(PHONE_REG.test(phone));

    // 自动生成安全手机号（138****4001）
    if (PHONE_REG.test(phone)) {
      setSafePhone(phone.replace(/^(\d{3})\d{4}(\d{4})$/, "$1****$2"));
    }
  }, [phone]);

  /* 星空动画（略，与你 LoginPage 一致，可直接复制） */
  // ----------------------------------------------------------
  useEffect(() => {
    // 略，此处与你原来的完全一致
  }, []);
  // ----------------------------------------------------------

 const handleRegister = async () => {
  if (!isPhoneValid) return message.error("请输入合法手机号");
  if (!username) return message.error("请输入用户名");
  if (!password || !confirmPassword)
    return message.error("请输入密码");
  if (password !== confirmPassword)
    return message.error("两次密码不一致");

  // ⭐ 调用后端注册 API
  const res = await postJSON("/auth", {
    type: "register",
    username,
    password,
    confirm_password: confirmPassword, // 后端要求字段
  });

  // 后端注册成功表示：
  // {
  //   status: 200,
  //   token: "...",  // 注册后不一定返回 token
  //   ...
  // }

  if (res.status === 200) {
    message.success("注册成功，请登录");
    navigate("/login");
  } else {
    message.error("注册失败");
  }
};


  return (
    <>
      <canvas ref={starCanvas} id="auth-stars"></canvas>
      <canvas ref={meteorCanvas} id="auth-meteors"></canvas>
      <canvas ref={nebulaCanvas} id="auth-nebula"></canvas>
      <canvas ref={particleCanvas} id="auth-particles"></canvas>

      <div className="auth-container">
        <div className="glass-card">
          <h1 className="auth-title">注册账号</h1>
          <p className="auth-subtitle">加入智能学习助手</p>

          {/* 手机号 */}
          <div style={{ display: "flex", gap: 10 }}>
            <Input
              className="auth-input"
              size="large"
              placeholder="手机号"
              value={showRawPhone ? phone : safePhone || phone}
              onChange={(e) => setPhone(e.target.value)}
              status={phone && !isPhoneValid ? "error" : ""}
            />

            {/* 展示 / 隐藏按钮 */}
            <Button
              onClick={() => setShowRawPhone(!showRawPhone)}
            >
              {showRawPhone ? "隐藏" : "显示"}
            </Button>
          </div>

          <Input
            className="auth-input"
            size="large"
            placeholder="设置用户名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <Input.Password
            className="auth-input"
            size="large"
            placeholder="设置密码"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Input.Password
            className="auth-input"
            size="large"
            placeholder="确认密码"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />

          <Button
            className="auth-button"
            size="large"
            disabled={!isPhoneValid}
            onClick={handleRegister}
          >
            注册
          </Button>

          <p className="auth-footer">
            已有账号？ <Link to="/login">点击登录</Link>
          </p>
        </div>
      </div>
    </>
  );
};

export default RegisterPage;
