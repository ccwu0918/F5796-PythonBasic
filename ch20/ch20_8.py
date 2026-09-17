# 參閱20-24頁

import os
import shutil

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

# --- 載入原始文件 ---
db_path = "./chroma_db"
dir_path = './docs/'
loader = DirectoryLoader(dir_path, glob="**/*.md", loader_cls=TextLoader)
docs = loader.load()

headers = [   # 定義分割的「標題」等級單位
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers) # 分割物件

chunks = []
for d in docs:
    chunks += splitter.split_text(d.page_content)

print(f"\n已將文件分割成{len(chunks)}個片段。")
if chunks:
    print("最後一個片段內容：", chunks[-1].page_content)
    print("中繼資料：", chunks[-1].metadata)
    print("內容字數：", len(chunks[-1].page_content))

if os.path.exists(db_path):
    print(f"發現舊的資料庫，正在刪除: {db_path}")
    shutil.rmtree(db_path) # 刪除整個資料夾

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma.from_documents(
    documents=chunks,       # 存入分割後的文本塊
    embedding=embedding_model, # 指定詞嵌入模型
    persist_directory=db_path  # 指定資料庫的儲存路徑
)

print(f"成功將{len(chunks)}個分割文本寫入{db_path}")