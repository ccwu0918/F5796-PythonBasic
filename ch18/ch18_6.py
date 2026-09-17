# 參閱18-33頁

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
llm = ChatOllama(model="gemma3:1b")    # 建立語言模型物件

template = PromptTemplate.from_template( 
    "請翻譯成繁體中文：{msg}"
)
chain = template | llm    # 建立流程鏈
resp = chain.invoke({     
    "msg": "I like dogs." # 從「流程鏈」發起提問
 })

print(resp.content)       # 取得回應訊息