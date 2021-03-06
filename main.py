from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, ImageMessage
)
import os
import json
import st_main

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    tmp = json.loads(body)

    # handle webhook bodya
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.type == "message":

        # botを起動するとき
        if event.message.text == "お腹空いた":
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='お好み焼きかたこ焼き、どちらが食べたいですか？'),
                ]
            )
        # 食べたいものを入力してもらった時
        elif event.message.text == "お好み焼き" or event.message.text == "たこ焼き":
           
            # 選択されたデータを保存する
            f = open('data.txt')
            f.write(event.message.text+"\n")
            f.close()
            
            # 検索数の入力を求める
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='現在地から近い順にお店を表示します'),
                    TextSendMessage(text='欲しい店舗の数を教えてください!'),
                ]
            )
            
        # 結果を表示する数を受け取った時
        elif event.message.text.isdecimal():
            # 選択されたデータを保存する
            f = open('data.txt')
            f.write(event.message.text+"\n")
            f.close()
            
            # 位置情報の入力を求める
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='これから'+event.message.text+'のお店を検索するよ！'),
                    TextSendMessage(text='位置情報を送ってね！'),
                    TextSendMessage(text='line://nv/location'),
                ]
            )

        # 例外処理
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='何をいっているのかまるでわからない'),
                ]
            )


# 位置情報を受け取った時
@handler.add(MessageEvent, message=LocationMessage)
def hanndle_get_map(event):
    print(event.message.latitude)
    print(event.message.longitude)
    


# 画像を受け取った時
@handler.add(MessageEvent, message=ImageMessage)
def handle_get_picture(event):


    event.message.text = "test"
            
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
