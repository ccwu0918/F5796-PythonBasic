# 參閱20-12頁

from langchain_community.document_loaders import (
    DirectoryLoader, UnstructuredMarkdownLoader)
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

dir_path = './docs/'
db_path = "./chroma_db"

# 內含原始文件的資料夾路徑 # 詞向量資料庫的存檔路徑
loader = DirectoryLoader(dir_path, glob="**/*.md",
                         loader_cls=UnstructuredMarkdownLoader) 
docs = loader.load()

# 採用具備詞嵌入功能的語言模型建立「詞嵌入物件」
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma.from_documents(
    documents=docs,  # 指定儲存的文件
    embedding=embedding_model, # 指定詞嵌入物件
    persist_directory=db_path # 指定資料庫的儲存路徑
)

print(f"成功將{len(docs)}個文本寫入{db_path}")