# 參閱20-30頁

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 定義詞嵌入模型
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
db_path = "./chroma_db"

# 載入詞向量資料庫
vector_store = Chroma(
    persist_directory=db_path,
    embedding_function=embedding_model  # 提供詞嵌入模型
)

# 定義提取器
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold", 
    search_kwargs={'score_threshold': 0.5, 'k': 2}
)

# 定義處理使用者提問的語言模型物件
llm = ChatOllama(model="gemma3:1b")

# 5. 定義 Prompt 和 Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是親切的NEO 3D列印機客戶服務人員，請用繁體中文簡潔地回答問題，並說出3D列印機的型號名稱。" ),
    ("human", '''請根據以下產品資訊回答問題，
     產品資訊：{context}
     問題：{input}
    ''')
])

# 建立一個將檢索到的文件內容格式化的函式
# def format_docs(docs):
#     return "\n".join(d.page_content for d in docs)

def format_docs(docs):
    chunks = []  # 存放格式化後的每個片段的列表
    
    for d in docs:
        headers = []  # 儲存標題文字的列表
        if "Header 1" in d.metadata:  # 從中繼資料提取標題1
            headers.append(d.metadata['Header 1'])
        if "Header 2" in d.metadata:  # 從中繼資料提取標題2
            headers.append(d.metadata['Header 2'])
        
        header_str = "\n".join(headers)  # 組合標題和內容
        content_str = d.page_content
        chunks.append(f"{header_str}\n{content_str}")

    return "\n\n------\n\n".join(chunks) # 用分隔符號組合全部片段

# 建立完整的 RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

while True:
    q = input("提問（輸入'bye'結束） > ")
    if q.lower() == "bye":
        break
    
    # 執行 RAG Chain
    resp = rag_chain.invoke(q)
    print(resp)
    print("-" * 30)