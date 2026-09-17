# 參閱20-24頁

import os 
import shutil
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredMarkdownLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from langchain_ollama import OllamaEmbeddings

dir_path = './docs/'
db_path = "./chroma_db"
loader = DirectoryLoader(dir_path, glob="**/*.md",
                         loader_cls=UnstructuredMarkdownLoader)
docs = loader.load()

# 載入文件 # 建立分割器然後分割文件
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

print(f"\n已將文件分割成{len(chunks)}個片段。") 

if chunks: 
    print("最後一個片段內容：\n", chunks[-1].page_content) 
    print("中繼資料：", chunks[-1].metadata) 
    print("內容字數：", len(chunks[-1].page_content))

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

if os.path.exists(db_path): 
    print(f"發現舊的資料庫，正在刪除: {db_path}")
    shutil.rmtree(db_path) # 刪除整個資料夾

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=db_path # 指定儲存路徑
)

print(f"成功將{len(chunks)}個文本塊寫入{db_path} ")