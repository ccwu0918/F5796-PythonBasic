# 參閱21-28頁

from model import sheet
from datetime import datetime
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    StickerMessageContent,
    LocationMessageContent
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    StickerMessage,
    LocationMessage,
    TemplateMessage,
    # 範本與動作
    ConfirmTemplate,
    MessageAction,
    URIAction,
    ButtonsTemplate
)

gs = sheet.GoogleSheet('谷歌試算表','LINE線上報修')

configuration = Configuration(access_token='你的頻道存取令牌')
handler = WebhookHandler('你的頻道密鑰')

line_bot_api = MessagingApi(ApiClient(configuration))

users = {}

def check_user(id, name):
    global users

    if id not in users:
        users[id] = {
            'name':name,
            'logs':{'日期時間':'', '經緯度':'', '地址':'', '事由':''},
            'save':False 
        }

app = Flask(__name__)

def reply_text(token, id, txt):
    global users
    me = users[id]

    if me['save']  == False:
        if '報修' in txt:
            queries = ConfirmTemplate(
                text=f"{me['name']}您好，請問要回報查修地點嗎？", 
                actions=[
                    URIAction(
                        label='回報地點',
                        uri='line://nv/location'
                    ),
                    MessageAction(label='不需要', text='不需要')
                ])

            temp_msg = TemplateMessage(alt_text='確認訊息',
                                        template=queries)

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=token,
                    messages=[
                        temp_msg
                    ]
                )
            )
            me['save'] = True # 開始紀錄訊息
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=token,
                    messages=[
                        TextMessage(text="收到訊息了，謝謝！")
                    ]
                )
            )
    else:
        if txt=='不需要':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=token,
                    messages=[
                        TextMessage(text="好的，請大致描述狀況。")
                    ]
                )
            )
        elif me['logs']['事由'] == '':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=token,
                    messages=[
                        TextMessage(text="我記下來了，辛苦您了！")
                    ]
                )
            )
            me['logs']['事由'] = txt  # 儲存事由
            # 日期要設置成台北時間
            dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            me['logs']['日期時間'] = dt
            me['save'] = False   # 紀錄完畢

            print('資料紀錄:', me['logs'])
            logs = [id, me['name'], me['logs']['日期時間'], 
                        me['logs']['經緯度'], me['logs']['地址'], me['logs']['事由']]
            gs.append_row(logs)

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

@handler.default()
def default(event):
    print('捕捉到事件：', event)

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

    _id = event.source.user_id
    profile = line_bot_api.get_profile(_id)
    _name = profile.display_name
    # 紀錄用戶資料
    print('大頭貼網址：', profile.picture_url)
    print('狀態消息：', profile.status_message)
    check_user(_id, _name)

    txt=event.message.text  # 讀取使用者輸入的文字

    reply_text(event.reply_token, _id, txt)

# 處理地點訊息
@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event):
    global users
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

    me = users[event.source.user_id]
    
    addr=event.message.address         # 地址
    lat=str(event.message.latitude)    # 緯度，使用str()轉成字串格式。
    lon=str(event.message.longitude)   # 經度

    if addr is None:
        msg=f'收到GPS座標：({lat}, {lon})\n謝謝您！'
    else:
        msg=f'收到GPS座標：({lat}, {lon})。\n地址：{addr}\n謝謝您！'

    print(msg)
    print(f"save: {me['save']}")

    if  me['save']:
        me['logs']['經緯度'] = f'({lat}, {lon})'
        me['logs']['地址'] = addr

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text='請問是什麼狀況呢？')
                ]
            )
        )
    else:
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=msg)
                ]
            )
        )

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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run()