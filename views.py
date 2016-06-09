import json

from flask import Flask, request
from flask.templating import render_template
from slacker import Slacker

from comics_generator import parse_comics_message
from meme_generator import *
from slack_communicator import get_direct_messages, get_user_map, get_user

app = Flask(__name__)
SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")
SLACK_MEME_WEBHOOK_URL = os.environ.get("SLACK_MEME_WEBHOOK_URL")
SLACK_COMICS_WEBHOOK_URL = os.environ.get("SLACK_COMICS_WEBHOOK_URL")


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
        requests.post(SLACK_MEME_WEBHOOK_URL, data=json.dumps(payload))
    except Exception as e:
        return e

    return "Success!", 200


@app.route("/")
def hello():
    # text = request.args["text"]
    messages_count = 10#parse_comics_message(text)

    slack = Slacker(SLACK_API_TOKEN)
    user_id_name_map = get_user_map(slack)
    user_name_id = {v: k for k, v in user_id_name_map.items()}

    messages = get_direct_messages(slack, user_id_name_map, 'ktisha')
    messages = messages[-messages_count:]

    comix = render_template("base.html", title=messages[0]['text'], messages=messages, user1=user_name_id['stan'],
                                           user2=user_name_id['ktisha'])
    return comix


@app.route("/")
def comics():
    channel_id = request.args["channel_id"]
    user_id = request.args["user_id"]
    payload = get_user(user_id)
    payload["channel"] = channel_id

    attachments = [{"image_url": "http://comics-slack.herokuapp.com/", "fallback": "Oops. Try  again."}]
    payload.update({"attachments": attachments})

    try:
        requests.post(SLACK_COMICS_WEBHOOK_URL, data=json.dumps(payload))
    except Exception as e:
        return e

    return "Success!", 200
