# 參閱19-24頁

from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
import streamlit as st

st.title("AI導遊")

llm = ChatOllama(model="gemma2:2b", streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是星際大戰的天行者路克，現在是專業導遊。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "請用繁體中文回答：{input}")

])

chain = prompt | llm | StrOutputParser()

# 在「會談」中新增history變數，儲存對話紀錄。
if "history" not in st.session_state:
    st.session_state.history = ChatMessageHistory() # 建立聊天訊息紀錄物件

if len(st.session_state.history.messages) == 0:  # 如果對話紀錄是空的
    st.session_state.history.add_ai_message("您好！我是您的導遊😉") 

# 把「會談」中的對話紀錄呈現在頁面
for msg in st.session_state.history.messages:  # 逐一取出每一個訊息物件
    with st.chat_message(msg.type):
        st.write(msg.content) # 顯示訊息內容

if user_input := st.chat_input("請在此輸入訊息"):
    with st.chat_message("human"): # 插入代表使用者的圖示和編排區域
        st.write(user_input) # 在此編排區寫入使用者的輸入內容

    with st.chat_message("assistant"): # 插入代表AI的圖示和編排區域
        container = st.empty()  # 在此編排區建立預留空間
        response = ""  # 宣告儲存回應的變數

        for token in chain.stream({ # 發起串流，傳入使用者輸入和對話紀錄
                "input": user_input, 
                "history": st.session_state.history.messages
            }):
            response += token  # 串接回應文字
            container.write(response)  # 在預留空間寫入回應文字
            
    st.session_state.history.add_user_message(user_input)
    st.session_state.history.add_ai_message(response)
