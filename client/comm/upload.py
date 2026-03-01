# import base64
# import json
# import os
# import shutil
# import time
# from tkinter import filedialog
#
# import requests
# from dotenv import load_dotenv
# load_dotenv()
# SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "https://your-server.example.com")
# TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "40.0"))
#
# import os
# import time
# import json
# import base64
# import requests
#
# TEXTBOOK_DIR = os.path.join(os.getcwd(), "textbook")
#
#
# def upload_file(token, file_obj):
#     """
#     上传文件给服务器，只在本地保存一个 meta 文件（不保存 pdf 实体）。
#     参数:
#         token: 用户 token
#         file_obj: 已打开的文件对象(二进制模式)，例如 open(path, "rb") 得到的对象
#     返回:
#         dict: {"success": bool, "msg": str}
#     """
#     if file_obj is None:
#         return {"success": False, "msg": "文件对象为空"}
#
#     # 文件名（只保留名字部分）
#     raw_name = getattr(file_obj, "name", "unnamed")
#     filename = os.path.basename(raw_name)
#
#     # 读内容并 base64
#     try:
#         file_content = file_obj.read()
#     except Exception as e:
#         return {"success": False, "msg": "读取文件失败: " + str(e)}
#
#     if not file_content:
#         return {"success": False, "msg": "文件内容为空"}
#
#     base64_data = base64.b64encode(file_content).decode("utf-8")
#
#     # 生成唯一编号
#     unique_id = f"{int(time.time() * 1e6)}"
#
#     # 确保 textbook 目录存在
#     os.makedirs(TEXTBOOK_DIR, exist_ok=True)
#
#     # 生成 meta 文件路径（只保存 meta，不保存 pdf）
#     # 你也可以改成 f".{filename}.meta" 看你更喜欢哪种命名
#     meta_filename = f"{unique_id}.meta"
#     meta_path = os.path.join(TEXTBOOK_DIR, meta_filename)
#
#     # 写 meta 文件
#     meta_data = {
#         "id": unique_id,
#         "original": filename,
#         "timestamp": time.ctime(),
#         "meta_file": meta_filename,
#     }
#     try:
#         with open(meta_path, "w", encoding="utf-8") as f:
#             json.dump(meta_data, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         return {"success": False, "msg": "写入元数据失败: " + str(e)}
#
#     # 发送给服务器
#     url = f"{SERVER_BASE_URL}"
#     payload = {
#         "type": "upload",
#         "token": token,
#         "textbook": {
#             "name": filename,
#             "file_id": unique_id,
#             "data": base64_data,
#         },
#     }
#
#     try:
#         resp = requests.post(url, json=payload, timeout=TIMEOUT)
#     except requests.RequestException as e:
#         return {"success": False, "msg": "发生错误，错误类型：" + str(e)}
#
#     if resp.status_code == 200:
#         return {
#             "success": True,
#             "msg": "上传成功！",
#             "file_id": unique_id,
#             "meta_path": meta_path,
#         }
#     else:
#         return {"success": False, "msg": "上传失败！"}
#
#
# def delete(token, meta_file_obj):
#     """
#     删除服务器上的文件，并删除本地 meta 文件。
#     参数:
#         token: 用户 token
#         meta_file_obj: 已打开的 meta 文件对象 (例如 open("xxx.meta", "r"))
#     返回:
#         dict: {"success": bool, "msg": str}
#     """
#
#     if meta_file_obj is None:
#         return {"success": False, "msg": "meta 文件对象为空"}
#
#     # 获取 meta 文件真实名字（如 textbook/123456789.meta）
#     meta_path = meta_file_obj.name
#
#     # 尝试读取 meta 内容
#     try:
#         meta_data = json.load(meta_file_obj)
#     except Exception as e:
#         return {"success": False, "msg": "读取 meta 文件失败: " + str(e)}
#     finally:
#         meta_file_obj.close()
#
#     # 获取 file_id
#     file_id = meta_data.get("id")
#     if not file_id:
#         return {"success": False, "msg": "meta 文件中缺少 file_id"}
#
#     payload = {
#         "type": "delete",
#         "token": token,
#         "file_id": file_id
#     }
#
#     url = f"{SERVER_BASE_URL}"
#
#     try:
#         resp = requests.post(url, json=payload, timeout=TIMEOUT)
#     except requests.RequestException as e:
#         return {"success": False, "msg": "发生错误，错误类型：" + str(e)}
#
#     if resp.status_code == 200:
#         # 删除本地 meta 文件
#         try:
#             os.remove(meta_path)
#         except OSError:
#             pass  # 删不掉也不影响服务器删除结果
#
#         return {"success": True, "msg": "删除成功！"}
#     else:
#         return {"success": False, "msg": "删除失败！"}
#
#
#
# if __name__ == "__main__":
#     token = "krgI-9n_edHkkfWms5aeHIS4IQ576NXWZsO7kZOoC9I"
#     with open(r"E:\OOAD\OOAD Project EN.pdf", "rb") as f:
#         res = upload_file(token, f)
#         print(res)
#         # 这里 res 里可以拿到 file_id / meta_path
#
#     # 删除时，用 meta 的路径
#     # with open("D:\\Learn\\Lv3\\object\\sample\\Intelligent-Learning-Assistant\\client\\comm\\textbook\\1764512705468726.meta", "r", encoding="utf-8") as meta:
#     #     res = delete(token, meta)
#     #     print(res)
import base64
import json
import os
import shutil
import time
from tkinter import filedialog

import requests
from dotenv import load_dotenv
load_dotenv()
SERVER_BASE_URL = os.getenv("SERVER_BASE_URL", "https://your-server.example.com")
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "40.0"))

import os
import time
import json
import base64
import requests

TEXTBOOK_DIR = os.path.join(os.getcwd(), "textbook")


def upload_file(token, file_obj):
    """
    上传文件给服务器，只在本地保存一个 meta 文件（不保存 pdf 实体）。
    参数:
        token: 用户 token
        file_obj: 已打开的文件对象(二进制模式)，例如 open(path, "rb") 得到的对象
    返回:
        dict: {"success": bool, "msg": str}
    """
    if file_obj is None:
        return {"success": False, "msg": "文件对象为空"}

    # 文件名（只保留名字部分）
    # raw_name = getattr(file_obj, "name", "unnamed")
    # filename = os.path.basename(raw_name)
    filename = getattr(file_obj, "filename", None)

    # 2. 退而求其次，用普通文件对象的 name
    if not filename:
        filename = getattr(file_obj, "name", None)

    # 3. 再次兜底：避免 None
    if not filename:
        filename = "uploaded.pdf"  # 随便给个默认值，避免崩

    # 只要 filename 在这里是 "xxx.pdf" / "xxx.docx" / "xxx.pptx"，
    # 远端就能正确识别扩展名
    filename = os.path.basename(filename)

    # 读内容并 base64
    try:
        file_content = file_obj.read()
    except Exception as e:
        return {"success": False, "msg": "读取文件失败: " + str(e)}

    if not file_content:
        return {"success": False, "msg": "文件内容为空"}

    base64_data = base64.b64encode(file_content).decode("utf-8")

    # 生成唯一编号
    unique_id = f"{int(time.time() * 1e6)}"

    # 确保 textbook 目录存在
    os.makedirs(TEXTBOOK_DIR, exist_ok=True)

    # 生成 meta 文件路径（只保存 meta，不保存 pdf）
    # 你也可以改成 f".{filename}.meta" 看你更喜欢哪种命名
    meta_filename = f"{unique_id}.meta"
    meta_path = os.path.join(TEXTBOOK_DIR, meta_filename)

    # 写 meta 文件
    meta_data = {
        "id": unique_id,
        "original": filename,
        "timestamp": time.ctime(),
        "meta_file": meta_filename,
    }
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"success": False, "msg": "写入元数据失败: " + str(e)}

    # 发送给服务器
    url = f"{SERVER_BASE_URL}"
    payload = {
        "type": "upload",
        "token": token,
        "textbook": {
            "name": filename,
            "file_id": unique_id,
            "data": base64_data,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        return {"success": False, "msg": "发生错误，错误类型：" + str(e)}

    if resp.status_code == 200:
        return {
            "success": True,
            "msg": "上传成功！",
            "file_id": unique_id,
            "meta_path": meta_path,
        }
    else:
        print(resp.text)
        return {"success": False, "msg": "上传失败！"}


def delete(token, meta_file_obj):
    """
    删除服务器上的文件，并删除本地 meta 文件。
    参数:
        token: 用户 token
        meta_file_obj: 已打开的 meta 文件对象 (例如 open("xxx.meta", "r"))
    返回:
        dict: {"success": bool, "msg": str}
    """

    if meta_file_obj is None:
        return {"success": False, "msg": "meta 文件对象为空"}

    # 获取 meta 文件真实名字（如 textbook/123456789.meta）
    meta_path = meta_file_obj.name

    # 尝试读取 meta 内容
    try:
        meta_data = json.load(meta_file_obj)
    except Exception as e:
        return {"success": False, "msg": "读取 meta 文件失败: " + str(e)}
    finally:
        meta_file_obj.close()

    # 获取 file_id
    file_id = meta_data.get("id")
    if not file_id:
        return {"success": False, "msg": "meta 文件中缺少 file_id"}

    payload = {
        "type": "delete",
        "token": token,
        "file_id": file_id
    }

    url = f"{SERVER_BASE_URL}"

    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT)
    except requests.RequestException as e:
        return {"success": False, "msg": "发生错误，错误类型：" + str(e)}

    if resp.status_code == 200:
        # 删除本地 meta 文件
        try:
            os.remove(meta_path)
        except OSError:
            pass  # 删不掉也不影响服务器删除结果

        return {"success": True, "msg": "删除成功！"}
    else:
        return {"success": False, "msg": "删除失败！"}



if __name__ == "__main__":
    token = "C3xJqc-eV4cTcss3YEk9NmYJood1X1OVyZaYK8MaL5c"
    with open(r"E:\OOAD\OOAD Project EN.pdf", "rb") as f:
        res = upload_file(token, f)
        print(res)
        # 这里 res 里可以拿到 file_id / meta_path

    # 删除时，用 meta 的路径
    # with open("D:\\Learn\\Lv3\\object\\sample\\Intelligent-Learning-Assistant\\client\\comm\\textbook\\1764512705468726.meta", "r", encoding="utf-8") as meta:
    #     res = delete(token, meta)
    #     print(res)