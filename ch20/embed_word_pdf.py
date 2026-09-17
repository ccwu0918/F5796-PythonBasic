import os
import shutil
# 引用所有需要的載入器
from langchain_community.document_loaders import (
    DirectoryLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPDFLoader
)
# 用於過濾掉複雜（不支援的）中繼資料
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

dir_path = './docs/'
db_path = "./chroma_db"

# 為每種文件類型建立一個 DirectoryLoader
# 載入 Markdown 檔案
loader_md = DirectoryLoader(
    dir_path,
    glob="**/*.md", 
    loader_cls=UnstructuredMarkdownLoader
)

# 載入 Word 檔案
loader_docx = DirectoryLoader(
    dir_path,
    glob="**/*.docx", 
    loader_cls=UnstructuredWordDocumentLoader,
    # show_progress=True,
    # use_multithreading=True
)

# 載入 PDF 檔案
loader_pdf = DirectoryLoader(
    dir_path,
    glob="**/*.pdf", 
    loader_cls=UnstructuredPDFLoader
)

# 載入所有文件然後合併
print("正在載入 Word 文件...")
docs_docx = loader_docx.load()

print("\n正在載入 Markdown 文件...")
docs_md = loader_md.load()

print("\n正在載入 PDF 文件...")
docs_pdf = loader_pdf.load()

all_docs = docs_docx + docs_md + docs_pdf
print(f"\n成功載入 {len(all_docs)} 份文件。")


if not all_docs:
    print(f"在 '{dir_path}' 路徑下找不到任何支援的檔案 (.docx, .md, .pdf)。")
else:
    # 過濾掉複雜的中繼資料
    # 避免因 PDF 等文件的複雜中繼資料導致後續存入資料庫時出錯
    filtered_docs = filter_complex_metadata(all_docs)

    # 建立分割器然後分割文件
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(filtered_docs)
    
    print(f"\n已將所有文件分割成 {len(chunks)} 個片段。")
    if chunks:
        last_chunk = chunks[-1]  # 預覽最後一個片段的資訊
        source_file = os.path.basename(last_chunk.metadata.get('source', 'N/A'))
        print(f"最後一個片段來自檔案: {source_file}")
        print("內容預覽：\n", last_chunk.page_content[:200] + "...")
        print("中繼資料：", last_chunk.metadata)
        print("內容字數：", len(last_chunk.page_content))
    
    # 嵌入與儲存向量資料庫
    embedding_model = OllamaEmbeddings(model="nomic-embed-text") 
    
    if os.path.exists(db_path):
        print(f"\n發現舊的資料庫，正在刪除: {db_path}")
        shutil.rmtree(db_path)
    
    print("\n正在建立向量資料庫...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=db_path
    )
    
    print(f"\n成功將 {len(chunks)} 個文本塊寫入 {db_path}")
