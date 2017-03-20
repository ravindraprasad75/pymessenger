"""
This bot listens for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

ACCESS_TOKEN = os.environ["FB_ACCESS_TOKEN"]

bot = Bot(ACCESS_TOKEN)

# ADD BUTTON AS FIRST ENTRY
buttons = [{
            "type":"postback",
            "title":"Start Query",
            "payload":"USER_START_QUERY"
          }]


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == os.environ["FB_VERIFY_TOKEN"]:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200

        return "Hello world 4", 200

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for messaging_event in messaging:
                if messaging_event.get('message'):
                    recipient_id = messaging_event['sender']['id']
                    if messaging_event['message'].get('text'):
                        message = messaging_event['message']['text']
                        bot.send_text_message(recipient_id, message)

                    if messaging_event['message'].get('text'):
                        message = messaging_event['message']['text']
                        if message == "button":
                            bot.send_button_message(recipient_id, message, buttons)

                    if messaging_event['message'].get('attachments'):
                        for att in messaging_event['message'].get('attachments'):
                            bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    pass
        return "Success"


if __name__ == '__main__':
    app.run(debug=True)

