# 參閱19-22頁

import streamlit as st
count = 0
if st.button('累進計數'):
    count += 1
st.write(f"計數值：{count}")