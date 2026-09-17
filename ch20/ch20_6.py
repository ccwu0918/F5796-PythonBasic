# 參閱20-19頁

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 定義詞嵌入模型物件
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

db_path = "./chroma_db" # 向量資料庫的存檔路徑

vector_store = Chroma( # 定義查詢詞向量資料庫用的物件
    persist_directory=db_path, # 資料庫路徑
    embedding_function=embedding_model # 詞嵌入模型物件
)

retriever = vector_store.as_retriever( ) # 定義提取器

# 與使用者交流的自然語言模型物件
llm = ChatOllama(model="gemma3:1b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是親切的NEO 3D列印機客戶服務人員。" ),
    ("human", '''請根據以下內容，用繁體中文簡潔地回答問題：
     {context}
     問題：{input} 
     ''')
    ])

def format_docs(docs): # 將詞向量搜尋結果整合成字串的函式
    return "\n".join(d.page_content for d in docs)

rag_chain = ( # 建立 RAG 流程鏈
{"context": retriever | format_docs, 
 "input": RunnablePassthrough()}
 | prompt     # 用上面產生的字典值，對自然語言模型發起提問
 | llm
 | StrOutputParser() # 最後輸出字串
)

while True:
    q = input("提問（輸入'bye'結束） > ")
    if q.lower() == "bye":
        break

    resp = rag_chain.invoke(q) # 從「RAG 流程鏈」發起提問
    print(resp)
    print("-" * 30)