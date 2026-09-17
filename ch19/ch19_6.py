# 參閱19-12頁

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st      # 引用 streamlit
import ollama

local_list = ollama.list()  # 取得本地模型清單
models = [item.model for item in local_list.models]
st.title("世界特色美食百科")
model_name = st.selectbox("請選擇模型", models)
area = st.text_input("國家、區域或都市", "台灣")
dishes = st.number_input("美食種類", min_value=1,
                         max_value=5, value=3)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "你是一位熱情的美食家，擅長介紹世界各地的代表性美食。"),
    ("human", 
     "請用繁體中文，條列式地介紹{area}的{dishes}種代表性美食，"
     "並簡短說明其特色。")
])

if st.button("開始推薦！"):
    if not area:    # 檢查使用者是否有輸入地區
        st.warning("請先輸入國家、地區或都市！")
    else:
        st.info(f"正在為您探索{area}的{dishes}種美食...")
        llm = ChatOllama(model=model_name, temperature=0.1)
        chain = prompt | llm | StrOutputParser()
        # 提問
        resp = chain.invoke({"area": area, "dishes": dishes}) 
        st.write(resp) # 在目前的版面位置顯示回應