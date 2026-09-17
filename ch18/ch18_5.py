# 參閱18-31頁

from langchain_ollama import ChatOllama   # 引用提示詞模板
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model="gemma3:1b")       # 建立語言模型物件
template = PromptTemplate.from_template(  # 建立模板物件
    "請翻譯成繁體中文：{msg}"               # 在預留位置（msg）填入文字 "I like dogs."，合成提示詞
)
 
prompt = template.invoke({"msg": "I like dogs."}) 
resp = llm.invoke(prompt)  # 傳入提示詞給語言模型，發起提問
print(resp.content)        # 從回應物件的 content 屬性取得生成文字