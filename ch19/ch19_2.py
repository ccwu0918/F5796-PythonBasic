# 參閱19-5頁

import streamlit as st

st.title("今日格言")
col1, col2 = st.columns(2)

with col1:
    st.header("上聯")
    st.write("今日事今日畢")
with col2:
    st.header("下聯")
    st.write("過了今日就不必")