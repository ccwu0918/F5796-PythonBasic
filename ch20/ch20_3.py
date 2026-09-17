# 參閱20-9頁

from langchain_community.document_loaders import (
    DirectoryLoader, 
    UnstructuredMarkdownLoader )

dir_path = './docs/'
db_path = "./chroma_db"
loader = DirectoryLoader(dir_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
docs = loader.load()  # 載入文件