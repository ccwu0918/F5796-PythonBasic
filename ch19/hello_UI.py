# 參閱19-4頁
# streamlit run hello_ui.py --server.port 8080

import streamlit as st

st.set_page_config(
    page_title="AI翻譯社",
    page_icon="🤖"
)

st.title("歡迎光臨 🤖 AI翻譯社")
st.write("""
    我是採用本地語言模型的翻譯機器人，可以翻譯
    **多國文字**。\n\n想更了解我嗎？請參閱 
    📖 [swf.com.tw](https://swf.com.tw) 網站。
""")
