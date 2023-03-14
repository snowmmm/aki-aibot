from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from transformers import pipeline

app = Flask(__name__)

line_bot_api = LineBotApi('<Your Channel Access Token>')
handler = WebhookHandler('<Your Channel Secret>')
generator = pipeline('text-generation', model='gpt2')

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_message = event.message.text
    bot_response = generator(user_message, max_length=50, do_sample=False)
    reply_message = bot_response[0]["generated_text"]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run()
