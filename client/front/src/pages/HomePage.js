import React, { useEffect, useRef } from "react";
import { Layout, Button, Typography, Row, Col, Card } from "antd";
import { useNavigate } from "react-router-dom";

import "./HomePage.css";


const { Header, Content, Footer } = Layout;
const { Title, Paragraph } = Typography;

const HomePage = () => {
  const navigate = useNavigate();

  // ==== 星空、流星、星云、粒子 Canvas ====
  const starCanvas = useRef(null);
  const meteorCanvas = useRef(null);
  const nebulaCanvas = useRef(null);
  const particleCanvas = useRef(null);

  /*--------------------------------------------------
   🌌 动态星空 / 流星 / 星云 / 粒子光晕逻辑
   （这一部分在“第 2 部分”发送）
  --------------------------------------------------*/
 useEffect(() => {
  const starCtx = starCanvas.current.getContext("2d");
  const meteorCtx = meteorCanvas.current.getContext("2d");
  const nebulaCtx = nebulaCanvas.current.getContext("2d");
  const particleCtx = particleCanvas.current.getContext("2d");

  let w = window.innerWidth;
  let h = window.innerHeight;

  // 设定 Canvas 尺寸
  [starCanvas, meteorCanvas, nebulaCanvas, particleCanvas].forEach((ref) => {
    ref.current.width = w;
    ref.current.height = h;
  });

  /* --------------------------------------------------------
   🌟 1. 星空背景（静态 + 微动）
  -------------------------------------------------------- */
  const stars = Array.from({ length: 350 }).map(() => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: Math.random() * 1.2 + 0.2,
    speed: Math.random() * 0.2 + 0.05,
  }));

  function drawStars() {
    starCtx.clearRect(0, 0, w, h);
    starCtx.fillStyle = "rgba(255,255,255,0.8)";

    stars.forEach((s) => {
      starCtx.beginPath();
      starCtx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      starCtx.fill();

      // 微微下坠
      s.y += s.speed;
      if (s.y > h) {
        s.y = 0;
        s.x = Math.random() * w;
      }
    });
  }

  /* --------------------------------------------------------
   ☄️ 2. 流星动画
  -------------------------------------------------------- */
  const meteors = [];

  function spawnMeteor() {
    const x = Math.random() * w;
    meteors.push({
      x,
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

    // 随机生成流星（每 1～3 秒）
    if (Math.random() < 0.01) spawnMeteor();
  }

  /* --------------------------------------------------------
   🌈 3. 星云（发光渐变层）
  -------------------------------------------------------- */
  function drawNebula() {
    nebulaCtx.clearRect(0, 0, w, h);

    const gradient = nebulaCtx.createRadialGradient(
      w * 0.65,
      h * 0.35,
      0,
      w * 0.65,
      h * 0.35,
      w * 0.8
    );
    gradient.addColorStop(0, "rgba(120,80,255,0.6)");
    gradient.addColorStop(0.4, "rgba(80,40,200,0.3)");
    gradient.addColorStop(1, "rgba(0,0,0,0)");

    nebulaCtx.fillStyle = gradient;
    nebulaCtx.fillRect(0, 0, w, h);
  }

  /* --------------------------------------------------------
   ✨ 4. 粒子光晕（漂浮微光）
  -------------------------------------------------------- */
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

      // 漂浮边界反弹
      if (p.x < 0 || p.x > w) p.vx *= -1;
      if (p.y < 0 || p.y > h) p.vy *= -1;
    });
  }

  /* --------------------------------------------------------
   🎞 主动画循环
  -------------------------------------------------------- */
  function animate() {
    drawStars();
    drawNebula();
    drawParticles();
    drawMeteors();
    requestAnimationFrame(animate);
  }

  animate();

  /* --------------------------------------------------------
   📐 监听窗口变化
  -------------------------------------------------------- */
  window.addEventListener("resize", () => {
    w = window.innerWidth;
    h = window.innerHeight;

    [starCanvas, meteorCanvas, nebulaCanvas, particleCanvas].forEach((ref) => {
      ref.current.width = w;
      ref.current.height = h;
    });

    drawNebula(); // 星云需重画
  });
}, []);


  return (
    <>
      {/* 星空背景 Canvas 层 */}
      <canvas ref={starCanvas} id="canvas-stars" />
      <canvas ref={meteorCanvas} id="canvas-meteors" />
      <canvas ref={nebulaCanvas} id="canvas-nebula" />
      <canvas ref={particleCanvas} id="canvas-particles" />

      <Layout className="homepage-wrapper">

        {/* ------------------------------------------ */}
        {/* 🔝 顶部导航栏 */}
        {/* ------------------------------------------ */}
        <Header className="homepage-header">
          <div className="nav-buttons">
            <Button type="text" className="nav-btn" onClick={() => navigate("/login")}>
              登录
            </Button>
          </div>
        </Header>

        {/* ------------------------------------------ */}
        {/* 🌌 Hero 主视觉区 */}
        {/* ------------------------------------------ */}
        <Content className="homepage-content">
          <div className="hero">
            <Title className="hero-title">智能学习助手系统</Title>
            <Paragraph className="hero-subtitle">
              探索浩瀚星空知识，AI 将成为你最可靠的学习伙伴。
            </Paragraph>

            <div className="hero-buttons">
              <Button
                size="large"
                className="btn-primary hero-main-btn"
                onClick={() => navigate("/login")}
              >
                开始使用
              </Button>
            </div>
          </div>

          {/* ------------------------------------------ */}
          {/* ⭐ 三大核心功能 */}
          {/* ------------------------------------------ */}
          <Row gutter={24} className="feature-section">
            <Col span={8}>
              <Card className="feature-card" title="知识宇宙">
                <p>构建你的知识星图，像掌握星辰一样掌握知识。</p>
              </Card>
            </Col>

            <Col span={8}>
              <Card className="feature-card" title="AI 智能路径">
                <p>AI 自动推导最佳学习路线，不走弯路。</p>
              </Card>
            </Col>

            <Col span={8}>
              <Card className="feature-card" title="全程陪伴">
                <p>无论作业、自学还是考试，AI 永远伴你左右。</p>
              </Card>
            </Col>
          </Row>

          {/* ------------------------------------------ */}
          {/* 🔥 六大 AI 能力展示模块 */}
          {/* ------------------------------------------ */}
          <div className="section-title">AI 的六大核心能力</div>
          <Row gutter={24} className="ai-skills">
            {[
              { icon: "🧠", title: "知识理解", desc: "深入理解你学习的每个知识点。" },
              { icon: "✨", title: "智能检索", desc: "海量知识中为你找到最需要的内容。" },
              { icon: "📘", title: "教材解析", desc: "上传教材，AI 自动标记知识点与知识结构。" },
              { icon: "📝", title: "自动练习题", desc: "为你生成个性化练习题与解析。" },
              { icon: "📊", title: "学习诊断", desc: "自动识别弱点，给出提升方向。" },
              { icon: "🤖", title: "智能导师", desc: "像私人老师一样回答你的问题。" },
            ].map((item, i) => (
              <Col span={8} key={i}>
                <div className="ai-skill-card">
                  <div className="ai-skill-icon">{item.icon}</div>
                  <div className="ai-skill-title">{item.title}</div>
                  <div className="ai-skill-desc">{item.desc}</div>
                </div>
              </Col>
            ))}
          </Row>

          {/* ------------------------------------------ */}
          {/* 🚀 学习路径大 Banner */}
          {/* ------------------------------------------ */}
          <div className="big-banner">
            <div className="banner-content">
              <h2>AI 为你规划最优学习路径</h2>
              <p>不再迷茫，从今天开始系统化学习。</p>
            </div>
          </div>

          {/* ------------------------------------------ */}
          {/* 📘 教材解析模块 */}
          {/* ------------------------------------------ */}
          <div className="section-title">智能教材解析</div>

          <Row gutter={24} className="教材解析-section">
            {[
              {
                title: "📤 上传教材",
                desc: "支持 PDF、图片、截图，一键上传。",
              },
              {
                title: "🔍 AI 自动解析",
                desc: "自动提取知识点、目录结构、关键公式。",
              },
              {
                title: "📚 知识星图展示",
                desc: "构建你的专属知识脉络，全局掌握教材内容。",
              },
            ].map((step, i) => (
              <Col span={8} key={i}>
                <div className="step-card">
                  <div className="step-title">{step.title}</div>
                  <div className="step-desc">{step.desc}</div>
                </div>
              </Col>
            ))}
          </Row>

          {/* ------------------------------------------ */}
          {/* 📚 学科模块（Knowledge Areas） */}
          {/* ------------------------------------------ */}
          <div className="section-title">支持多学科全覆盖</div>

          <Row gutter={24} className="subject-section">
            {[
              "数学 🧮",
              "物理 ⚛️",
              "化学 🧪",
              "计算机 💻",
              "经济学 📈",
              "英语 🇬🇧",
            ].map((subj, i) => (
              <Col span={8} key={i}>
                <div className="subject-card">{subj}</div>
              </Col>
            ))}
          </Row>

          {/* ------------------------------------------ */}
          {/* 🗣 用户评价（Testimonials） */}
          {/* ------------------------------------------ */}
          <div className="section-title">他们这样说</div>
          <Row gutter={24} className="testimonial-section">
            {[
              {
                name: "Xiao Li",
                text: "AI 帮我自动整理考试范围，期末直接起飞！",
              },
              {
                name: "Zhang Wei",
                text: "像私人家教一样，有问必答。",
              },
              {
                name: "Lin",
                text: "上传教材后，AI 自动帮我画出了整个知识网络，非常强！",
              },
            ].map((item, i) => (
              <Col span={8} key={i}>
                <Card className="testimonial-card">
                  <p className="testimonial-text">“{item.text}”</p>
                  <p className="testimonial-name">—— {item.name}</p>
                </Card>
              </Col>
            ))}
          </Row>

          {/* ------------------------------------------ */}
          {/* 🔥 大 CTA Banner */}
          {/* ------------------------------------------ */}
          <div className="cta-banner">
            <h2>准备好开始探索知识宇宙了吗？</h2>
            <Button
              size="large"
              className="btn-primary cta-btn"
              onClick={() => navigate("/login")}
            >
              立即开始
            </Button>
          </div>
        </Content>

        {/* ------------------------------------------ */}
        {/* 🛰 页脚 */}
        {/* ------------------------------------------ */}
        <Footer className="footer">
          © 2025 Intelligent Learning Assistant · Made with ❤️ & AI
        </Footer>
      </Layout>
    </>
  );
};

export default HomePage;
