import os
from random import randint
from urllib.parse import unquote, quote

import requests

MEME_BASE_URL = os.environ.get("MEME_BASE_URL")


def get_memes():
    response = requests.get(MEME_BASE_URL + "/templates").json()

    result = []

    for key, value in response.items():
        name = value.replace(MEME_BASE_URL + "/templates/", "")
        description = key
        result.append((name, description))

    return result


def list_memes():
    templates = get_memes()

    help_text = ""

    for template in templates:
        help_text += "`{0}` {1}\n".format(template[0], template[1])

    return help_text


def build_url(meme, top, bottom):
    if meme is "johnshow":
        path = "/{0}/{1}/{2}.jpg".format(meme, top or '_', bottom or '_')
        path += "?alt=http://images-cdn.moviepilot.com/images/c_fill,h_720,w_1280/t_mp_quality/qgqpal5akpm621tdsmlt/if-this-theory-s-true-then-jon-snow-is-definitely-dead-607536.jpg"
        return MEME_BASE_URL + path

    return MEME_BASE_URL + "/{0}/{1}/{2}.jpg".format(meme, top or '_', bottom or '_')


def parse_message(message):
    message = unquote(message.strip())
    message = message[:-1] if message[-1] == "&" else message

    meme_text = message.split("&")

    meme_text = [x.strip() for x in meme_text]
    meme_text = [x.replace(" ", "_") for x in meme_text]
    available_memes = [x[0] for x in get_memes()]

    text = [quote(x.encode("utf8")) for x in meme_text[1:]]
    meme_text = [meme_text[0]]
    meme_text.extend(text)

    if meme_text[0] not in available_memes:
        meme_text.insert(0, available_memes[randint(0, len(available_memes))])

    if len(meme_text) < 3:
        meme_text += [None] * (3 - len(meme_text))

    return meme_text[0], meme_text[1], meme_text[2]
