# 參閱21-25頁

import os
import sys
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)
# 確保 chroma_db 路徑正確
db_path = "./chroma_db"

if not os.path.exists(db_path):
    print(f"出錯了～無法讀取ChromaDB路徑：'{db_path}'。")
    sys.exit(1) # 終止程式

configuration = Configuration(access_token='你的頻道存取令牌')
handler = WebhookHandler('你的頻道密鑰')

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma(
    persist_directory=db_path,
    embedding_function=embedding_model
)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.6, 'k': 2}
)

llm = ChatOllama(model="gemma3:1b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是3D列印機客戶服務人員" ),
    ("human", '''請根據以下產品資訊，用繁體中文簡潔地回答問題。
     產品資訊：{context}
     問題：{input}
    ''')
])

def format_docs(docs):
    return "\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print("模型與資料庫載入完成，伺服器準備就緒。")

@app.route('/')
def index():
    return 'Welcome to Line Bot!'

@app.route("/callback", methods=['POST'])
def callback():
    # 取得X-Line-Signature標頭值
    signature = request.headers['X-Line-Signature']

    # 取得請求本體
    body = request.get_data(as_text=True)
    app.logger.info("請求本體：" + body)

    try:  # 處理webhook本體
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("驗證錯誤～請檢查您的頻道存取令牌/頻道密鑰。")
        abort(400) # 中止請求（400 Bad Request）

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    q=event.message.text
    print(f"接收到問題: {q}")
    # 使用 RAG chain 產生答案
    resp = rag_chain.invoke(q)
    print(f"產生的答案: {resp}")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=resp)]
            )
        )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)