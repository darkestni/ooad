import base64
import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "https://your-server.example.com")
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10.0"))

def upload_question(token: str, text: str = "", images=None,session_id: int = 1):
    """
    上传“问题”，问题可以只包含文字、只包含图片，或文字+多张图片。
    图片不附带文件名
    参数:
      - image_paths: None / 单个路径 / [路径, 路径, ...]
    """
    # 1) 归一化图片列表
    if images is None:
        image_list = []
    elif isinstance(images, (list, tuple)):
        image_list = list(images)
    else:
        image_list = [images]

    images_b64 = []
    for p in image_list:
        if not os.path.exists(p):
            return {"success": False, "msg": f"图片不存在: {p}"}
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        images_b64.append(b64)

    # 3) 生成问题唯一编号（也可用 uuid4().hex）
    question_id = time.time()

    payload = {
        "type": "question",
        "token": token,
        "timestamp":question_id,
        "session_id":session_id,
        "payload": [
            {"text": text.strip() if text else ""},
            {"image": images_b64}  # 可能是空列表
        ]
    }

    # 5) 发送
    try:
        resp = requests.post(SERVER_BASE_URL, json=payload, timeout=TIMEOUT)
        if resp.status_code == 200:
            return {"success": True,"msg": {"answer": resp.json().get("answer"),"session_id": resp.json().get("session_id")}}

        else:
            return {"success": False, "msg": "出错了！"}
    except requests.RequestException as e:
        return {"success": False, "msg": "发生错误，错误类型："+str(e)}

if __name__ == "__main__":
    token = "KATYl13VMlVJUFjokFKbGuaVYJz1DtMnQ9zyYRlvbHE"
    img = r"D:\Learn\f9a66536d84c70229af5912b44341c7a.png"
    result = upload_question(token, "帮我解析这张图", images=img, session_id=1)
    print(result)