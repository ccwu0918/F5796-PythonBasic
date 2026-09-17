# 參閱19-16頁

from langchain_core.messages import SystemMessage  # 系統訊息類別                                               # 
from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()  # 建立「聊天訊息紀錄」物件

# 新增系統訊息
history.add_message(SystemMessage(content="你是專業導遊")) 
history.add_user_message("法國的首都？")    

# 新增使用者訊息
history.add_ai_message("法國的首都是巴黎")   # 新增 AI 助手訊息
print("訊息紀錄：", history.messages)

history.clear()
print("\n清除紀錄後：", history.messages)