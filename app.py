import os
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, ImageMessage, ImageSendMessage

app = Flask(__name__)

# 設置Line Bot的Channel access token及Channel secret
line_bot_api = LineBotApi('K7jkNovEJpCqafdqEuZh1TFGcr5JegkjJHC6l6v2+ZfLlNoByJUGgGnuY6yJ3dELGESLXwru742Ku2ijGgGtUHJ2150By86Wj6kzZKySFnmkyU4jHhK//pyfRoi4bU/VvGS/wKeOzBYP8NyV3q1CqQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2a9a171886e678889fc9972e25c3580c')


# Line Bot接收Webhook的路由
@app.route('/webhook', methods=['POST'])
def webhook():
    # 驗證Line Bot的簽名
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 處理收到的圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    # 取得圖片網址
    message_content = line_bot_api.get_message_content(event.message.id)

    # 建立資料夾（如果不存在）
    if not os.path.exists("images"):
        os.makedirs("images")

    # 儲存圖片檔案
    with open(f"images/{event.message.id}.jpg", "wb") as f:
        for chunk in message_content.iter_content():
            f.write(chunk)


if __name__ == '__main__':
    app.run()
