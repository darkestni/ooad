import psycopg2
from psycopg2._json import Json
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def _get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def db_exists(table, column, value):
    sql = f"SELECT 1 FROM {table} WHERE {column}=%s LIMIT 1"

    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (value,))
            return cur.fetchone() is not None
    finally:
        conn.close()


def db_select(table, column=None, value=None, order_by=None):
    if column is None:
        sql = f"SELECT * FROM {table}"
        params = ()
    else:
        sql = f"SELECT * FROM {table} WHERE {column}=%s"
        params = (value,)

    if order_by:
        sql += f" ORDER BY {order_by}"

    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def db_exists_multi(table, conditions: dict) -> bool:
    """
    通用多条件查询是否存在：
    db_exists_multi("users", {"username": "abc", "password": "123"})
    """
    if not conditions:
        raise ValueError("conditions cannot be empty")

    columns = list(conditions.keys())
    values = list(conditions.values())

    where_clause = " AND ".join([f"{col}=%s" for col in columns])
    sql = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1"

    conn = _get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, values)
            return cur.fetchone() is not None
    finally:
        conn.close()

def db_insert(table, data: dict):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))

    # 对值做适配：如果是 dict/list，用 Json 包起来
    adapted_values = []
    for v in data.values():
        if isinstance(v, (dict, list)):
            adapted_values.append(Json(v))
        else:
            adapted_values.append(v)

    values = tuple(adapted_values)

    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, values)
            conn.commit()
            return True
    finally:
        conn.close()


def db_delete(table, column, value):
    """
    从指定表删除 column = value 的所有行。
    返回受影响的行数。
    用法：db_delete("token", "token", some_token)
    """
    sql = f"DELETE FROM {table} WHERE {column}=%s"

    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (value,))
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()
