# 參閱19-14頁

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm = ChatOllama(model="gemma3:1b")

# 提示模板和鏈的定義不變
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是星際大戰的天行者路克，現在是專業導遊。"),
    ("human", "請用繁體中文回答：{input}")
])

chain = prompt | llm | StrOutputParser()
while True:
    q = input("遊客：")
    if q == "bye":
        break

    print("導遊：", end="")
    resp = chain.invoke({
        "input": q # 使用者的訊息
    })
    print(resp)   # 輸出 AI 的回應