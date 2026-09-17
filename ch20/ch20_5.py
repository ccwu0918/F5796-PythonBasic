# 參閱20-17頁

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

prompt = ChatPromptTemplate.from_messages([ # 定義提問模板
    ("system", "你是親切的NEO 3D列印機客戶服務人員。" ),
    ("human", '''請根據以下內容，用繁體中文簡潔地回答問題： {context}
     問題：{input} ''')
])

chain = prompt | llm | StrOutputParser()

while True:
    q = input("提問（輸入'bye'結束） > ")
    if q.lower() == "bye":
        break

    docs = retriever.invoke(q) # 從向量資料庫檢索相關文件
    txt = "\n".join([d.page_content for d in docs]) # 將相關文件內容合併成一個字串

    resp = chain.invoke({ # 呼叫自然語言模型
        "context": txt,
        "input": q
    })

    print(resp)
    print("-" * 30)