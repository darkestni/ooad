const API_BASE = "http://localhost:9876/api";

// 通用封装
async function postJSON(url, body) {
  const res = await fetch(`${API_BASE}${url}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
}

const reg = await postJSON("/auth", { //注册
  type: "register",
  username: "alice",
  password: "p@ssw0rd",
  confirm_password: "p@ssw0rd"
});

const login = await postJSON("/auth", {//登录
  type: "login",
  username: "alice",
  password: "p@ssw0rd",
  confirm_password: "p@ssw0rd" 
});

const up = await postJSON("/upload-textbook", {//上传教材
  token: "<user_token>",
  file_path: "E:/docs/xxx.pdf"
});

const del = await postJSON("/delete-textbook", {//删除教材
  token: "<user_token>",
  path: "D:/project/textbook/xxx(1).pdf"   // 需要能定位到本地复制的那份
});

const qa = await postJSON("/question", {//问问题
  token: "<user_token>",
  text: "请解析第 3 题。",
  images: [
    "E:/docs/math/q3.png",
    "E:/docs/math/step2.jpg"
  ]
  session_id:"234"
});

const ex = await postJSON("/export",{
  token: "<user_token>",
});