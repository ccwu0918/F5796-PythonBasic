# 參閱18-36頁

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="gemma3:1b")  # 建立語言模型物件
prompt = ChatPromptTemplate([        # 預設用 from_message() 建立模板
    ("system", "你是把 {input} 翻譯成 {output} 的得力助手。" ),
    ("human", "請翻譯：{question}")
])

chain = prompt | llm | StrOutputParser()
resp = chain.invoke({
    "input":"英文",
    "output":"繁體中文",
    "question":"Life is short, I use Python."
})
print(resp)  # 輸出生成的字串