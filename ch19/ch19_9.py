# 參閱19-18頁

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (ChatPromptTemplate, 
                                    MessagesPlaceholder)
from langchain_community.chat_message_histories import ChatMessageHistory

# 定義聊天訊息紀錄物件
chat_hist = ChatMessageHistory()
llm = ChatOllama(model="gemma3:1b")

# 提示模板和鏈的定義不變
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是星際大戰的天行者路克，現在是專業導遊。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "請用繁體中文回答：{input}")
])

chain = prompt | llm | StrOutputParser()
while True:
    q = input("遊客：")
    if q == "bye":
        chat_hist.clear()
        break
    print("導遊：", end="")
    
    resp = chain.invoke({  # 發起提問，附帶對話紀錄
        "input": q,        # 使用者的訊息
        "history": chat_hist.messages # 對話紀錄
    })
    print(resp) # 顯示完整回應
    chat_hist.add_user_message(q)   # 將此次使用者提問存入對話紀錄
    chat_hist.add_ai_message(resp)  # 將此次回應存入對話紀錄