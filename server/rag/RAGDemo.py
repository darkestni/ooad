import os
import json
from typing import List, Dict, Tuple

# LangChain & Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

# --- 配置区域 ---
# 请确保设置了环境变量 OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = "sk-..." 

class SystemConfig:
    PERSIST_DIRECTORY = "chroma_db_production"
    # 使用 BGE 模型进行高质量嵌入
    EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5" 
    DEVICE = "cpu" # 或 "cuda"

# --- 1. 初始化核心组件 (单例模式思想) ---
print("--- 初始化系统模型 ---")
embeddings = HuggingFaceBgeEmbeddings(
    model_name=SystemConfig.EMBEDDING_MODEL_NAME,
    model_kwargs={"device": SystemConfig.DEVICE},
    encode_kwargs={"normalize_embeddings": True}
)

# 初始化向量数据库连接
vectorstore = Chroma(
    persist_directory=SystemConfig.PERSIST_DIRECTORY,
    embedding_function=embeddings
)

# 初始化 LLM (用于路由判定)
llm_router = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# 初始化重排模型 (用于比对匹配 Chunk)
reranker = FlashrankRerank()

# --- 业务逻辑类定义 ---

class KnowledgeBaseManager:
    """
    对应需求 1: 网络接收端给我 id data(.pdf), 我输出(id, chunk[])给数据库。
    """
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def upload_data(self, doc_id: str, pdf_path: str) -> List[str]:
        """
        处理上传的 PDF，切分并存入数据库
        """
        print(f"\n[写入流程] 正在处理文档 ID: {doc_id}, 路径: {pdf_path}")
        
        # 1. 加载 PDF
        try:
            loader = PyPDFLoader(pdf_path)
            raw_docs = loader.load()
        except Exception as e:
            print(f"[错误] 无法加载 PDF: {e}")
            return []

        # 2. 切分 (Chunking)
        chunks = self.text_splitter.split_documents(raw_docs)

        # 3. 注入 Metadata (将 doc_id 绑定到每个 chunk)
        for i, chunk in enumerate(chunks):
            chunk.metadata["doc_id"] = doc_id
            chunk.metadata["chunk_index"] = i
        
        # 4. 存入向量数据库 (持久化)
        self.vector_db.add_documents(chunks)
        
        # 5. 返回 chunk 内容列表 (模拟输出给数据库记录)
        chunk_contents = [doc.page_content for doc in chunks]
        print(f"[写入完成] 已存储 {len(chunks)} 个切片到向量库。")
        
        # 返回 (id, chunk[]) 格式供上层调用者使用
        return chunk_contents

class IntelligentAssistant:
    """
    对应需求 2: 处理用户问题，记录历史，判断检索，匹配 Chunk，返回给调用方。
    """
    def __init__(self, vector_db, llm, reranker_model):
        self.vector_db = vector_db
        self.llm = llm
        self.reranker = reranker_model

    def _mock_db_history_log(self, user_id: str, query: str, image_path: str = None):
        """
        模拟：给数据库初始问题让数据库做历史记录写入
        """
        # 在实际生产中，这里是 SQL INSERT 操作
        log_entry = f"User: {user_id} | Query: {query} | Image: {image_path if image_path else 'None'}"
        print(f"[数据库记录] 已写入历史记录: {log_entry}")

    def _check_retrieval_necessity(self, query: str) -> bool:
        """
        模拟：问 AI 是否需要检索数据库 (Router)
        """
        prompt = PromptTemplate.from_template(
            """You are a router. Analyze the user input determine if it requires external knowledge (like specific documents, facts not in general knowledge) to answer.
            Input: {query}
            Return ONLY the word 'YES' or 'NO'.
            """
        )
        chain = prompt | self.llm
        response = chain.invoke({"query": query})
        decision = response.content.strip().upper()
        print(f"[AI 决策] 是否需要检索: {decision}")
        return "YES" in decision

    def _perform_retrieval_and_match(self, query: str) -> List[Document]:
        """
        模拟：数据库给我一大推数据资料，我将问题做成 chunk 跟数据资料比对得到匹配的 chunk
        """
        # 1. 粗排/召回 (Retrieval): 获取"一大推数据资料" (比如 Top 50)
        # 这里直接使用向量库的相似度搜索作为初筛
        large_pile_docs = self.vector_db.similarity_search(query, k=20)
        print(f"[数据库召回] 初步获取了 {len(large_pile_docs)} 条相关资料。")

        # 2. 精排/比对 (Rerank): 使用 Flashrank 将问题与资料比对
        # Flashrank 会计算 query 和 doc 之间的相关性分数并重新排序
        compressed_docs = self.reranker.compress_documents(
            documents=large_pile_docs, 
            query=query
        )
        
        # 3. 过滤: 只保留分数较高的 Top K (这里假设取前 3 个最匹配的)
        final_chunks = compressed_docs[:3]
        print(f"[Chunk比对] 精确匹配到 {len(final_chunks)} 个最佳切片。")
        return final_chunks

    def handle_user_query(self, user_id: str, query: str, image_path: str = None):
        """
        主流程入口
        """
        print(f"\n--- 开始处理请求: '{query}' ---")
        
        # Step 1: 记录历史
        self._mock_db_history_log(user_id, query, image_path)

        # Step 2: 问 AI 是否需要检索
        needs_retrieval = self._check_retrieval_necessity(query)

        matched_chunks = []
        
        if needs_retrieval:
            # Step 3: 如果需要，执行检索和比对 (RAG 核心流程)
            matched_docs = self._perform_retrieval_and_match(query)
            # 提取内容返回
            matched_chunks = [doc.page_content for doc in matched_docs]
        else:
            print("[逻辑] 不需要检索，直接进入闲聊模式（返回空资料）。")

        # Step 4: 返回给大模型调用方
        # 这里的返回值包含：是否进行了检索、匹配到的知识片段
        result_package = {
            "query": query,
            "retrieval_performed": needs_retrieval,
            "matched_chunks": matched_chunks
        }
        
        return result_package

# --- 模拟运行流程 (Demo) ---

if __name__ == "__main__":
    # 实例化服务
    kb_manager = KnowledgeBaseManager(vectorstore)
    assistant = IntelligentAssistant(vectorstore, llm_router, reranker)

    # ==========================================
    # 场景 1: 上传资料 (对应要求 1)
    # ==========================================
    # 注意：请确保目录下有一个真实的 pdf 文件，或者注释掉这两行
    # 为了演示，假设我们有一个 'sample.pdf'
    pdf_file_path = "sample_document.pdf" # 替换为你实际的 PDF 路径
    
    # 创建一个假的 PDF 用于测试 (如果文件不存在)
    if not os.path.exists(pdf_file_path):
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf_file_path)
        c.drawString(100, 750, "Project A is a secret web application project.")
        c.drawString(100, 730, "The deadline is October 27th.")
        c.drawString(100, 710, "It requires Python and Java skills.")
        c.save()

    doc_id_input = "DOC_001"
    # 调用上传接口
    chunks_output = kb_manager.upload_data(doc_id_input, pdf_file_path)
    # print(f"API 输出给数据库的 Chunk 数据: {chunks_output[:1]}...")

    # ==========================================
    # 场景 2: 用户提问 (对应要求 2)
    # ==========================================
    
    # Case A: 需要检索的问题
    user_question_1 = "What is the deadline for Project A?"
    user_image_1 = "screenshot.png" # 假设用户传了图片
    
    result_1 = assistant.handle_user_query("USER_123", user_question_1, user_image_1)
    
    print("\n--- 最终返回给大模型调用方的数据 (Case A) ---")
    print(json.dumps(result_1, indent=2, ensure_ascii=False))
    
    # Case B: 不需要检索的闲聊
    user_question_2 = "Hello, how are you today?"
    result_2 = assistant.handle_user_query("USER_123", user_question_2)
    
    print("\n--- 最终返回给大模型调用方的数据 (Case B) ---")
    print(json.dumps(result_2, indent=2, ensure_ascii=False))