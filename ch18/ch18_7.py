# 參閱18-34頁

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="gemma3:1b")   # 建立語言模型物件
template = PromptTemplate.from_template( 
    "請翻譯成繁體中文：{msg}"
)   # 建立提示詞模板

chain = template | llm | StrOutputParser() # 最後轉成字串格式
resp = chain.invoke({  # 從「流程鏈」發起提問
    "msg": "I like dogs."
})
print(resp)            # resp 的值即是字串格式的回應