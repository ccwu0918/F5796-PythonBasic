# 參閱19-23頁

import streamlit as st

if 'count' not in st.session_state:  # 如果會談物件裡面沒有'count' 
    # 此行可寫成：st.session_state['count'] = 0
    st.session_state.count = 0

if st.button('累進計數'):
    # 此行可寫成：st.session_state['count'] += 1
    st.session_state.count += 1 

st.write(f"計數值：{st.session_state.count}")