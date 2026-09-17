import os
import shutil
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredWordDocumentLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

dir_path = './docs/'
db_path = "./chroma_db"

loader = DirectoryLoader(
    dir_path,
    glob="**/*.docx", 
    loader_cls=UnstructuredWordDocumentLoader,
    show_progress=True, # 加上進度條，方便觀察載入進度
    use_multithreading=True # 加速載入多個檔案
)

print("正在載入 Word 文件...")
docs = loader.load()  # 載入文件

if not docs:
    print(f"在 '{dir_path}' 路徑下找不到任何 .docx 檔案，請檢查路徑或檔案是否存在。")
else:
    # 建立分割器然後分割文件
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    
    print(f"\n已將文件分割成 {len(chunks)} 個片段。")
    if chunks:
        print("最後一個片段內容預覽：\n", chunks[-1].page_content[:200] + "...") # 預覽前200字元
        print("中繼資料：", chunks[-1].metadata)
        print("內容字數：", len(chunks[-1].page_content))
    
    # 嵌入與儲存向量資料庫
    embedding_model = OllamaEmbeddings(model="nomic-embed-text") 
    
    if os.path.exists(db_path):
        print(f"發現舊的資料庫，正在刪除: {db_path}")
        shutil.rmtree(db_path)  # 刪除整個資料夾
    
    print("正在建立向量資料庫...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=db_path
    )
    
    print(f"成功將 {len(chunks)} 個文本塊寫入 {db_path}")