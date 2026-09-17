# 參閱19-10頁

from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import ollama
import streamlit as st

local_list = ollama.list()  # 取得本地模型清單
models = [item.model for item in local_list.models]

st.title("世界特色美食百科")
model_name = st.selectbox("請選擇模型", models)
area = st.text_input("國家、區域或都市")
dishes = st.number_input("美食種類",min_value=1,max_value=5, value=3)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是熟悉世界各地特色美食的料理家。" ),
    ("human", "請用繁體中文回答:{area}的{dishes}種代表美食，謝謝。") 
])

if st.button("提問"):
    try:
        container = st.empty()
        llm = ChatOllama(model=model_name, temperature=0.1, streaming=True)
        chain = prompt | llm | StrOutputParser()

        response = ""
        for token in chain.stream({"area": area, "dishes": dishes}):
            response += token
            container.write(response)

    except Exception as e:
        st.error(f"出錯啦：{e}")
