// src/pages/LoginPage.js
import React, { useState, useEffect, useRef } from "react";
import { Input, Button, message } from "antd";
import { Link, useNavigate } from "react-router-dom";

import { loginUser } from "../services/api";
import { postJSON } from "../services/api";

import "./AuthPage.css";

// 手机号验证正则（中国大陆）
const PHONE_REG = /^1[3-9]\d{9}$/;

const LoginPage = ({ onLogin }) => {
  const [loginMode, setLoginMode] = useState("password"); // password | sms
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // 验证码登录模式
  const [phone, setPhone] = useState("");
  const [smsCode, setSmsCode] = useState("");
  const [isPhoneValid, setIsPhoneValid] = useState(false);
  const [smsCountdown, setSmsCountdown] = useState(0);

  const navigate = useNavigate();

  // 🌌 星空背景画布（保持你的设计）
  const starCanvas = useRef(null);
  const meteorCanvas = useRef(null);
  const nebulaCanvas = useRef(null);
  const particleCanvas = useRef(null);

  /* --------------------------------------------------
     星空动画（原样复制）
  -------------------------------------------------- */
  useEffect(() => {
    const starCtx = starCanvas.current.getContext("2d");
    const meteorCtx = meteorCanvas.current.getContext("2d");
    const nebulaCtx = nebulaCanvas.current.getContext("2d");
    const particleCtx = particleCanvas.current.getContext("2d");

    let w = window.innerWidth;
    let h = window.innerHeight;

    [starCanvas, meteorCanvas, nebulaCanvas, particleCanvas].forEach((ref) => {
      ref.current.width = w;
      ref.current.height = h;
    });

    const stars = Array.from({ length: 350 }).map(() => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 1.2 + 0.2,
      speed: Math.random() * 0.2 + 0.05,
    }));

    function drawStars() {
      starCtx.clearRect(0, 0, w, h);
      starCtx.fillStyle = "rgba(255,255,255,0.9)";
      stars.forEach((s) => {
        starCtx.beginPath();
        starCtx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        starCtx.fill();
        s.y += s.speed;
        if (s.y > h) {
          s.y = 0;
          s.x = Math.random() * w;
        }
      });
    }

    const meteors = [];
    function spawnMeteor() {
      meteors.push({
        x: Math.random() * w,
        y: -20,
        length: Math.random() * 230 + 120,
        speed: Math.random() * 6 + 4,
        opacity: Math.random() * 0.4 + 0.3,
      });
    }
    function drawMeteors() {
      meteorCtx.clearRect(0, 0, w, h);
      meteors.forEach((m, i) => {
        meteorCtx.strokeStyle = `rgba(180,180,255,${m.opacity})`;
        meteorCtx.lineWidth = 2.2;
        meteorCtx.beginPath();
        meteorCtx.moveTo(m.x, m.y);
        meteorCtx.lineTo(m.x - m.length, m.y + m.length * 0.4);
        meteorCtx.stroke();

        m.x -= m.speed;
        m.y += m.speed * 0.4;
        if (m.y > h || m.x < -200) meteors.splice(i, 1);
      });

      if (Math.random() < 0.01) spawnMeteor();
    }

    function drawNebula() {
      nebulaCtx.clearRect(0, 0, w, h);
      const g = nebulaCtx.createRadialGradient(
        w * 0.65, h * 0.35, 0,
        w * 0.65, h * 0.35, w * 0.8
      );
      g.addColorStop(0, "rgba(120,80,255,0.6)");
      g.addColorStop(0.4, "rgba(80,40,200,0.3)");
      g.addColorStop(1, "rgba(0,0,0,0)");
      nebulaCtx.fillStyle = g;
      nebulaCtx.fillRect(0, 0, w, h);
    }

    const particles = Array.from({ length: 60 }).map(() => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 3 + 1,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      alpha: Math.random() * 0.5 + 0.3,
    }));

    function drawParticles() {
      particleCtx.clearRect(0, 0, w, h);
      particles.forEach((p) => {
        particleCtx.fillStyle = `rgba(180,170,255,${p.alpha})`;
        particleCtx.beginPath();
        particleCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        particleCtx.fill();

        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
      });
    }

    function animate() {
      drawStars();
      drawNebula();
      drawParticles();
      drawMeteors();
      requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener("resize", () => {
      w = window.innerWidth;
      h = window.innerHeight;
      [starCanvas, meteorCanvas, nebulaCanvas, particleCanvas].forEach((ref) => {
        ref.current.width = w;
        ref.current.height = h;
      });
      drawNebula();
    });
  }, []);

  /* ------------------------------------------------------
      手机号实时校验
  ------------------------------------------------------ */
  useEffect(() => {
    setIsPhoneValid(PHONE_REG.test(phone));
  }, [phone]);

  /* ------------------------------------------------------
      获取验证码（模拟）
  ------------------------------------------------------ */
  const sendSMS = () => {
    if (!isPhoneValid) {
      return message.error("请输入合法手机号");
    }
    message.success("验证码已发送（模拟）");
    setSmsCountdown(60);
  };

  useEffect(() => {
    if (smsCountdown <= 0) return;
    const timer = setTimeout(() => setSmsCountdown(smsCountdown - 1), 1000);
    return () => clearTimeout(timer);
  }, [smsCountdown]);

  /* ------------------------------------------------------
      登录 - 密码模式
  ------------------------------------------------------ */
  const handlePasswordLogin = async () => {
  if (!username || !password)
    return message.error("请输入用户名和密码");

  // ⭐ 使用后端真实 API 格式
  const res = await postJSON("/auth", {
    type: "login",
    username,
    password,
    confirm_password: password, // 后端要求字段
  });

  // ⭐ 后端登录成功条件
  if (res.success && res.msg && res.msg.token) {
    message.success("登录成功");

    // 保存 token
    localStorage.setItem("token", res.msg.token);

    // 保存历史消息（如果有）
    localStorage.setItem("history", JSON.stringify(res.msg.content || []));

    navigate("/chat");
  } else {
    message.error(res.msg || "登录失败");
  }
};



  /* ------------------------------------------------------
      登录 - 验证码模式（模拟）
  ------------------------------------------------------ */
  const handleSMSLogin = () => {
    if (!isPhoneValid) return message.error("手机号不正确");
    if (!smsCode) return message.error("请输入验证码");

    message.success("使用验证码登录成功（模拟）");
    localStorage.setItem("token", "sms-login-token");
    if (onLogin) onLogin("sms-login-token", []);
    navigate("/chat");
  };

  /* ------------------------------------------------------
      微信登录按钮
  ------------------------------------------------------ */
  const handleWeChatLogin = () => {
    message.loading("正在调用微信授权...", 1);
    setTimeout(() => {
      message.success("微信登录成功");
      localStorage.setItem("token", "wechat-token");
      if (onLogin) onLogin("wechat-token", []);
      navigate("/chat");
    }, 1000);
  };

  return (
    <>
      {/* 星空背景层 */}
      <canvas ref={starCanvas} id="auth-stars"></canvas>
      <canvas ref={meteorCanvas} id="auth-meteors"></canvas>
      <canvas ref={nebulaCanvas} id="auth-nebula"></canvas>
      <canvas ref={particleCanvas} id="auth-particles"></canvas>

      {/* 登录卡片 */}
      <div className="auth-container">
        <div className="glass-card">

          <h1 className="auth-title">欢迎回来</h1>

          {/* 登录模式切换 */}
          <div style={{ color: "#dce1ff", marginBottom: 20 }}>
            <span
              style={{
                marginRight: 20,
                cursor: "pointer",
                color: loginMode === "password" ? "#fff" : "#9ab",
              }}
              onClick={() => setLoginMode("password")}
            >
              密码登录
            </span>
            <span
              style={{
                cursor: "pointer",
                color: loginMode === "sms" ? "#fff" : "#9ab",
              }}
              onClick={() => setLoginMode("sms")}
            >
              验证码登录
            </span>
          </div>

          {loginMode === "password" && (
            <>
              <Input
                className="auth-input"
                size="large"
                placeholder="用户名"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />

              <Input.Password
                className="auth-input"
                size="large"
                placeholder="密码"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <Button
                className="auth-button"
                size="large"
                onClick={handlePasswordLogin}
              >
                登录
              </Button>
            </>
          )}

          {loginMode === "sms" && (
            <>
              <Input
                className="auth-input"
                size="large"
                placeholder="手机号"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                status={phone && !isPhoneValid ? "error" : ""}
              />

              <div style={{ display: "flex", gap: 10 }}>
                <Input
                  className="auth-input"
                  size="large"
                  placeholder="验证码"
                  value={smsCode}
                  onChange={(e) => setSmsCode(e.target.value)}
                />
                <Button
                  disabled={!isPhoneValid || smsCountdown > 0}
                  onClick={sendSMS}
                >
                  {smsCountdown > 0 ? `${smsCountdown}s` : "获取验证码"}
                </Button>
              </div>

              <Button
                className="auth-button"
                size="large"
                onClick={handleSMSLogin}
              >
                登录
              </Button>
            </>
          )}

          {/* 微信登录 */}
          <Button
            size="large"
            onClick={handleWeChatLogin}
            style={{
              marginTop: 18,
              width: "100%",
              height: 48,
              borderRadius: 12,
              background: "linear-gradient(135deg,#1AAD19,#22C55E)",
              border: "none",
              color: "white",
              fontWeight: 600,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 10,
              boxShadow: "0 0 16px rgba(40,200,80,0.8)",
              transition: "all 0.25s ease",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.transform = "translateY(-4px) scale(1.03)")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.transform = "translateY(0) scale(1)")
            }
          >
            <img src="/wechat.svg" alt="" style={{ width: 26, height: 26 }} />
            微信登录
          </Button>

          <p className="auth-footer">
            还没有账号？ <Link to="/register">立即注册</Link>
          </p>
        </div>
      </div>
    </>
  );
};

export default LoginPage;
