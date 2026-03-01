# import os
# import requests
# from flask import jsonify
# from dotenv import load_dotenv
#
# from server.comm.handlers.tools import verify_token
#
# load_dotenv()
#
# NOTION_VERSION = "2022-06-28"
# CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
# CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
# REDIRECT_URI = "http://localhost:8765/callback"   # 必须与客户端一致！
#
#
# def notion_headers(token):
#     return {
#         "Authorization": f"Bearer {token}",
#         "Notion-Version": NOTION_VERSION,
#         "Content-Type": "application/json"
#     }
#
#
# # ---------- 生成授权链接（逻辑函数） ----------
# def get_auth_url():
#     params = {
#         "client_id": CLIENT_ID,
#         "response_type": "code",
#         "owner": "user",
#         "redirect_uri": REDIRECT_URI,
#     }
#     query = "&".join(f"{k}={v}" for k, v in params.items())
#     auth_url = f"https://api.notion.com/v1/oauth/authorize?{query}"
#
#     return jsonify({"auth_url": auth_url})
#
#
# def find_learning_assistant_page(token):
#     url = "https://api.notion.com/v1/search"
#     payload = {"query": "Learning Assistant"}
#     r = requests.post(url, json=payload, headers=notion_headers(token))
#     r.raise_for_status()
#     results = r.json().get("results", [])
#     for page in results:
#         if page.get("object") != "page":
#             continue
#         props = page.get("properties", {})
#         title_prop = None
#         # 找到一个 type 为 "title" 的属性（一般就是名字叫 "title" 的那个）
#         for prop in props.values():
#             if isinstance(prop, dict) and prop.get("type") == "title":
#                 title_prop = prop
#                 break
#         if not title_prop:
#             continue
#         title_rich = title_prop.get("title", [])
#         if not title_rich:
#             continue
#         # 尝试从 plain_text 或 text.content 拿字符串
#         first = title_rich[0]
#         title_text = first.get("plain_text") or first.get("text", {}).get("content", "")
#         if title_text == "Learning Assistant":
#             return page["id"]
#     return None
#
#
# def create_container_page(token):
#     url = "https://api.notion.com/v1/pages"
#     payload = {
#         "parent": {"type": "workspace", "workspace": True},
#         "properties": {
#             "title": [{"type": "text", "text": {"content": "Learning Assistant"}}]
#         }
#     }
#     r = requests.post(url, json=payload, headers=notion_headers(token))
#     r.raise_for_status()
#     return r.json()["id"]
#
#
# def create_child_page(token, parent_id):
#     url = "https://api.notion.com/v1/pages"
#     payload = {
#         "parent": {"page_id": parent_id},
#         "properties": {
#             "title": [{"type": "text", "text": {"content": "New Export"}}]
#         }
#     }
#     r = requests.post(url, json=payload, headers=notion_headers(token))
#     r.raise_for_status()
#     return r.json()["id"]
#
#
# def exchange_code_for_token(code):
#     resp = requests.post(
#         "https://api.notion.com/v1/oauth/token",
#         json={
#             "grant_type": "authorization_code",
#             "code": code,
#             "redirect_uri": REDIRECT_URI,
#         },
#         auth=(CLIENT_ID, CLIENT_SECRET),
#         timeout=30,
#     )
#     data = resp.json()
#     if "access_token" not in data:
#         raise RuntimeError(f"Token exchange failed: {data}")
#     return data["access_token"]
#
#
# # ---------- 主导出逻辑（给 app.py 调用） ----------
# def handle_export(data):
#     token = data.get("token")
#     code = data.get("code")
#
#     if not token or not code:
#         return jsonify({"success": False, "msg": "missing token or code"}), 400
#
#     # 1. server 用 secret 换 token（客户端不能做）
#     check,info = verify_token(token)
#     # 2. 如果返回的不是 True，说明失败了，直接把错误 Response 返回给前端
#     if check is not True:
#         return info
#     access_token = exchange_code_for_token(code)
#
#     # 2. 找容器页，没有就创建
#     container_id = find_learning_assistant_page(access_token)
#     if not container_id:
#         container_id = create_container_page(access_token)
#
#     # 3. 创建条目
#     entry_id = create_child_page(access_token, container_id)
#
#     return jsonify({
#         "success": True,
#         "container_id": container_id,
#         "entry_id": entry_id
#     })
# export_handler.py
import os
import uuid
import base64
from PIL import Image
from io import BytesIO
import shutil
import requests
from flask import jsonify
from dotenv import load_dotenv

from server.comm.handlers.tools import verify_token
from server.comm.db import db_select  #现成的 db_select

load_dotenv()

NOTION_VERSION = "2022-06-28"
CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8765/callback"   # 必须与客户端一致！

# 临时目录：用于 base64 图片落盘
EXPORT_TMP_DIR = os.path.join("/tmp", "ila_notion_export")


def notion_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }


# ---------- 生成授权链接（逻辑函数） ----------
def get_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "owner": "user",
        "redirect_uri": REDIRECT_URI,
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    auth_url = f"https://api.notion.com/v1/oauth/authorize?{query}"
    return jsonify({"auth_url": auth_url})


def find_learning_assistant_page(token):
    url = "https://api.notion.com/v1/search"
    payload = {"query": "Learning Assistant"}
    r = requests.post(url, json=payload, headers=notion_headers(token), timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    for page in results:
        if page.get("object") != "page":
            continue
        props = page.get("properties", {})
        title_prop = None
        for prop in props.values():
            if isinstance(prop, dict) and prop.get("type") == "title":
                title_prop = prop
                break
        if not title_prop:
            continue
        title_rich = title_prop.get("title", [])
        if not title_rich:
            continue
        first = title_rich[0]
        title_text = first.get("plain_text") or first.get("text", {}).get("content", "")
        if title_text == "Learning Assistant":
            return page["id"]
    return None


def create_container_page(token):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"type": "workspace", "workspace": True},
        "properties": {
            "title": [{"type": "text", "text": {"content": "Learning Assistant"}}]
        }
    }
    r = requests.post(url, json=payload, headers=notion_headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def create_child_page(token, parent_id, title="New Export"):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": [{"type": "text", "text": {"content": title}}]
        }
    }
    r = requests.post(url, json=payload, headers=notion_headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def exchange_code_for_token(code):
    resp = requests.post(
        "https://api.notion.com/v1/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30,
    )
    data = resp.json()
    if "access_token" not in data:
        raise RuntimeError(f"Token exchange failed: {data}")
    return data["access_token"]


# ------------------ Notion 写 blocks + 上传文件 ------------------

def append_blocks(token, parent_block_id, children):
    """
    向页面（page_id 也是一个 block_id）追加 blocks
    """
    url = f"https://api.notion.com/v1/blocks/{parent_block_id}/children"
    r = requests.patch(url, json={"children": children}, headers=notion_headers(token), timeout=30)
    r.raise_for_status()
    return r.json()


def chunk_100(arr):
    for i in range(0, len(arr), 100):
        yield arr[i:i + 100]


def rt(text: str):
    return [{"type": "text", "text": {"content": text}}]


def paragraph(text: str):
    return {"type": "paragraph", "paragraph": {"rich_text": rt(text)}}


def divider():
    return {"type": "divider", "divider": {}}


def heading2(text: str):
    return {"type": "heading_2", "heading_2": {"rich_text": rt(text)}}


def extract_text_and_images(payload):
    """
    payload 是 history.payload：list[dict]
    返回: (texts: list[str], images_b64: list[str])
    """
    texts = []
    images_b64 = []
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            if "text" in item and isinstance(item["text"], str) and item["text"]:
                texts.append(item["text"])
            if "image" in item:
                imgs = item["image"]
                if isinstance(imgs, list):
                    images_b64.extend([x for x in imgs if isinstance(x, str) and x])
                elif isinstance(imgs, str) and imgs:
                    images_b64.append(imgs)
    return texts, images_b64



def save_b64_images_to_tmp_files(images_b64, tmp_dir):
    os.makedirs(tmp_dir, exist_ok=True)
    out = []

    for b64s in images_b64:
        raw = base64.b64decode(b64s, validate=False)

        # 用 Pillow 识别格式
        try:
            img = Image.open(BytesIO(raw))
            fmt = img.format.lower()   # 'png' / 'jpeg' / 'gif' / 'webp'
        except Exception:
            fmt = None

        ext = fmt if fmt else "bin"
        filename = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(tmp_dir, filename)

        with open(path, "wb") as f:
            f.write(raw)

        if fmt == "png":
            ctype = "image/png"
        elif fmt in ("jpeg", "jpg"):
            ctype = "image/jpeg"
        elif fmt == "gif":
            ctype = "image/gif"
        elif fmt == "webp":
            ctype = "image/webp"
        else:
            ctype = "application/octet-stream"

        out.append((path, ctype, filename))

    return out


def notion_create_file_upload(access_token, filename, content_type):
    """
    Step 1: create file_upload object
    """
    url = "https://api.notion.com/v1/file_uploads"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    payload = {"filename": filename, "content_type": content_type}
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["id"], data["upload_url"]


# def notion_send_file_upload(access_token, upload_url, file_path, filename):
#     """
#     Step 2: send file bytes to upload_url
#     """
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Notion-Version": NOTION_VERSION,
#         # 不要手写 Content-Type，让 requests 生成 multipart boundary
#     }
#     with open(file_path, "rb") as f:
#         files = {"file": (filename, f)}
#         r = requests.post(upload_url, files=files, headers=headers, timeout=60)
#     r.raise_for_status()
#     return r.json()
def notion_send_file_upload(access_token, upload_url, file_path, filename, content_type):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Notion-Version": NOTION_VERSION,
    }

    # 20MB 保护（Notion 小文件 direct upload 上限）
    size = os.path.getsize(file_path)
    if size > 20 * 1024 * 1024:
        raise RuntimeError(f"File too large for Notion direct upload (>20MB): {filename}, size={size}")

    with open(file_path, "rb") as f:
        # 关键：把 content_type 放进 multipart 的 file part
        files = {"file": (filename, f, content_type)}
        r = requests.post(upload_url, files=files, headers=headers, timeout=60)

    if r.status_code != 200:
        # 打印 Notion 返回的错误体（你现在缺的就是这个）
        raise RuntimeError(f"Notion upload failed: {r.status_code} {r.text}")

    return r.json()


def notion_image_block_from_file_upload(file_upload_id):
    """
    Step 3: create an image block referencing the file_upload id
    """
    return {
        "type": "image",
        "image": {
            "type": "file_upload",
            "file_upload": {"id": file_upload_id}
        }
    }


# ---------- 主导出逻辑（给 app.py 调用） ----------
def handle_export(data):
    token = data.get("token")
    code = data.get("code")

    if not token or not code:
        return jsonify({"success": False, "msg": "missing token or code"}), 400

    # 1) 验证 token -> username（严格使用你给的 verify_token 语义）
    check, info = verify_token(token)
    if check is not True:
        return info
    username = info  #verify_token 成功时第二个返回值就是 username 字符串

    # 2) notion oauth code -> access_token
    access_token = exchange_code_for_token(code)

    # 3) 找/建容器页
    container_id = find_learning_assistant_page(access_token)
    if not container_id:
        container_id = create_container_page(access_token)

    # 4) 创建导出子页（标题带 username）
    entry_id = create_child_page(access_token, container_id, title=f"Export - {username}")

    # 5) 按用户从 history 查记录（不按 session）
    rows = db_select("history", "username", username, order_by="timestamp ASC, id ASC")

    # 6) 构建 blocks，并边写边上传图片（落盘->上传->删除）
    blocks_buf = []
    blocks_buf.append(heading2("Chat History Export"))
    blocks_buf.append(paragraph(f"username: {username}"))
    blocks_buf.append(divider())

    # 确保 tmp dir 是干净的（避免残留）
    os.makedirs(EXPORT_TMP_DIR, exist_ok=True)

    for rec in rows:
        role = rec.get("role")
        ts = str(rec.get("timestamp"))
        payload = rec.get("payload")

        # header
        prefix = "👤 USER" if role == "user" else "🤖 LLM" if role == "LLM" else f"🔹 {role}"
        blocks_buf.append(paragraph(f"{prefix}  {ts}"))

        texts, images_b64 = extract_text_and_images(payload)

        # text blocks
        for t in texts:
            blocks_buf.append(paragraph(t))

        # image blocks: base64 -> temp -> notion upload -> block -> delete local
        tmp_files = save_b64_images_to_tmp_files(images_b64, EXPORT_TMP_DIR)
        try:
            for file_path, content_type, filename in tmp_files:
                file_upload_id, upload_url = notion_create_file_upload(access_token, filename, content_type)
                #notion_send_file_upload(access_token, upload_url, file_path, filename)
                notion_send_file_upload(access_token, upload_url, file_path, filename, content_type)
                blocks_buf.append(notion_image_block_from_file_upload(file_upload_id))

                # 上传后删除本地图片
                if os.path.exists(file_path):
                    os.remove(file_path)
        finally:
            # 保险：中途异常也尽量清理
            for file_path, _, _ in tmp_files:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except:
                        pass

        blocks_buf.append(divider())

        # Notion 限制：一次 append 最多 100 blocks
        if len(blocks_buf) >= 90:
            for part in chunk_100(blocks_buf):
                append_blocks(access_token, entry_id, part)
            blocks_buf = []

    # flush remaining
    if blocks_buf:
        for part in chunk_100(blocks_buf):
            append_blocks(access_token, entry_id, part)

    # 7) 清理临时目录（你只要求删图片；这里做目录级清理更彻底）
    try:
        shutil.rmtree(EXPORT_TMP_DIR, ignore_errors=True)
    except:
        pass

    return jsonify({
        "success": True,
        "container_id": container_id,
        "entry_id": entry_id,
        "exported": len(rows)
    })
