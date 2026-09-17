# 參閱21-15頁

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
    TextMessage,
    StickerMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    StickerMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='你的Channel access token（頻 道存取令牌）')
handler = WebhookHandler('你的Channel secret（頻道密鑰）')

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

    # 處理webhook本體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("驗證錯誤～請檢查您的頻道存取令牌/頻道密鑰。")
        abort(400) # 中止請求（400 Bad Request）

    return 'OK'

@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    StickerMessage(
                        package_id=event.message.package_id,
                        sticker_id=event.message.sticker_id
                    )
                ]
            )
        )

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

    user_msg = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    display_name = profile.display_name

    reply = f"{display_name}您好：\n你說：{user_msg}"

    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text=reply),
                StickerMessage(
                    package_id='3',
                    sticker_id='233'
                )
            ]
        )
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)