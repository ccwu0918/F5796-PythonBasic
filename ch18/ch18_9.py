# 參閱18-38頁

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="gemma3:1b", streaming=True)    # 用「串流」輸出
prompt = ChatPromptTemplate([  # 建立模板
    ("system", "你是專業廚師。" ),
    ("human", "請用繁體中文說明 {dish} 的做法。")
])

chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"dish": "芝加哥熱狗"}):
    print(chunk, end="", flush=True)  # 逐一顯示收到的回應字詞