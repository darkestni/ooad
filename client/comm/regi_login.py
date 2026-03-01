import os
import requests
from dotenv import load_dotenv
load_dotenv()
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "https://your-server.example.com")
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10.0"))


def submit_auth(username: str, password: str, confirm_password: str, type: str):
    """
    1) 确认用户名、密码不为空
    2) 密码与确认一致
    3) 以 JSON 发送到服务器
    4) JSON 中包含 action（register/login）、username、password

    返回：
        True  表示服务器返回了 HTTP 200（不解析内容）
        False 表示服务器返回了非 200 或请求失败
    """
    # 1) & 2) 本地校验
    if not isinstance(username, str) or not username.strip():
        return {"success": False,"msg": "用户名不能为空"}
    if not isinstance(password, str) or not password.strip():
        return {"success": False,"msg": "密码不能为空"}
    if password != confirm_password:
        return {"success": False,"msg": "两次密码不一致"}
    if type not in ("register", "login"):
        return {"success": False,"msg": "action 必须是 'register' 或 'login'"}

    #发送 JSON
    url = f"{SERVER_BASE_URL}"
    payload = {
        "type": type,
        "username": username,
        "password": password
    }

    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT)
        print("DEBUG status:", resp.status_code)
        print("DEBUG body:", resp.text)
    except requests.RequestException as e:
        return {"success": False,"msg": "发生错误，错误类型："+str(e)}

    if type == "register":
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("token", {})
            return {"success": True,"msg": {"token": token}}
        elif resp.status_code == 201:
            return {"success": False,"msg": "用户已存在"}
        else:
            return {"success": False,"msg": "其他错误"}
    if type == "login" :
        if resp.status_code == 200:
            data = resp.json()
            return {"success":True,"msg":data}
        elif resp.status_code == 201:
            return {"success": False,"msg": "密码错误！"}
        else:
            return {"success": False,"msg": "其他错误"}
if __name__ == "__main__":
    result1 = submit_auth("1234","124","124","login")
    print(f"结果: {result1}\n")