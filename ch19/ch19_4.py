# 參閱19-6頁

import streamlit as st

customer_name = st.text_input('**姓名**', 
                              placeholder='請輸入您的大名')

num_of_cups = st.number_input('**杯數**', 
                              min_value=1, max_value=10, value=1)

toppings = ['珍珠', '芋圓', '椰果', '粉粿']
selected_toppings = st.multiselect('加料', toppings, 
                                   default=['珍珠'], placeholder='請選擇')

ice_level = ['去冰', '少冰', '正常冰', '多冰']
ice = st.radio('冰塊', ice_level,index=2, horizontal=True)

sugar_level = st.slider('甜度', 0, 100, 50)

take_out = st.checkbox('外帶')

if st.button('送出'):
    if not customer_name:
        st.warning('請輸入您的大名')
    else:
        if not selected_toppings:
            selected_toppings = ['無']

        st.write(f"""
            **{customer_name}** 您好，您的飲品選擇如下：
            - 杯數：{num_of_cups}
            - 加料：{", ".join(selected_toppings)}
            - 冰塊：{ice}
            - 甜度：{sugar_level}% \n
            {'**外帶**' if take_out else '**內用**'}
        """)
