import json
from pprint import pprint

from flask import Flask, request
from flask.templating import render_template
from slacker import Slacker

from meme_generator import *
from settings import SLACK_WEBHOOK_URL
from slack_communicator import get_direct_messages, get_user_map, get_user, post_meme_to_webhook

app = Flask(__name__)


@app.route("/meme")
def meme():
    text = request.args["text"]
    channel_id = request.args["channel_id"]
    user_id = request.args["user_id"]

    if text.startswith("list"):
        return list_memes()

    meme, top, bottom = parse_message(text)

    meme_url = build_url(meme, top, bottom)

    payload = get_user(user_id)
    payload["channel"] = channel_id

    attachments = [{"image_url": meme_url, "fallback": "Oops. Try  again."}]
    payload.update({"attachments": attachments})

    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except Exception as e:
        return e

    return "Success!", 200


@app.route("/")
def hello():
    slack = Slacker('xoxp-48784475313-48780293991-48732636563-5803262f4f')
    user_id_name_map = get_user_map(slack)
    user_name_id = {v: k for k, v in user_id_name_map.items()}

    messages = get_direct_messages(slack, user_id_name_map, 'ktisha')
    pprint(messages)
    return render_template("base1.html", title=messages[0]['text'], messages=messages, user1=user_name_id['stan'],
                           user2=user_name_id['ktisha'])
