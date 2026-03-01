// =============================================
// ⭐ 完全适配参考前端的 API 版本（最终稳定版）
// =============================================

const API_BASE = "http://localhost:9876/api";

// ----------------------------------------------------------
// ⭐ 通用 JSON POST 封装
// ----------------------------------------------------------
export async function postJSON(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  return await res.json();
}

// ----------------------------------------------------------
// ⭐ 通用 FormData POST（用于上传教材）
// ----------------------------------------------------------
export async function postFormData(path, formData) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    body: formData   // ❗不能手动加 Content-Type，让浏览器添加 boundary
  });

  return await res.json();
}

// ----------------------------------------------------------
// ⭐ 注册 register — 参考前端格式
// ----------------------------------------------------------
export async function registerUser(username, password, confirmPassword) {
  return await postJSON("/auth", {
    type: "register",
    username,
    password,
    confirm_password: confirmPassword
  });
}

// ----------------------------------------------------------
// ⭐ 登录 login — 参考前端格式
// 返回结构示例：
// {
//   "type": "history",
//   "status": 200,
//   "token": "...",
//   "content": [ ... 历史消息 ... ]
// }
// ----------------------------------------------------------
export async function loginUser(username, password) {
  return await postJSON("/auth", {
    type: "login",
    username,
    password,
    confirm_password: password
  });
}

// ----------------------------------------------------------
// ⭐ 提问 /question — 参考前端格式
// {
//   token: "...",
//   text: "用户问题",
//   images: [   // base64，如果没有就是 []
//   ]
// }
// ----------------------------------------------------------
export async function askQuestion(token, text, images = []) {
  return await postJSON("/question", {
    token,
    text,
    images
  });
}

// ----------------------------------------------------------
// ⭐ 上传教材 /upload-textbook（FormData）
// ----------------------------------------------------------
export async function uploadTextbook(token, file) {
  const form = new FormData();
  form.append("token", token);
  form.append("file", file); // File 对象

  return await postFormData("/upload-textbook", form);
}

// ----------------------------------------------------------
// ⭐ 删除教材 /delete-textbook
// 后端参数：
// { token, path }
// ----------------------------------------------------------
export async function deleteTextbook(token, path) {
  return await postJSON("/delete-textbook", {
    token,
    path
  });
}

// ----------------------------------------------------------
// ⭐ 导出到 Notion /export
// ----------------------------------------------------------
export async function exportToNotion(token) {
  return await postJSON("/export", {
    token
  });
}
