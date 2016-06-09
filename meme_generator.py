import os
from random import randint
from urllib.parse import unquote

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


def build_url(template, top, bottom):
    return MEME_BASE_URL + "/{0}/{1}/{2}.jpg".format(template, top or '_', bottom or '_')


def parse_message(message):
    message = unquote(message.strip())
    message = message[:-1] if message[-1] == "&" else message

    meme_text = message.split("&")

    meme_text = [x.strip() for x in meme_text]

    available_memes = [x[0] for x in get_memes()]

    if meme_text[0] not in available_memes:
        meme_text.insert(0, available_memes[randint(len(available_memes))])

    if len(meme_text) < 3:
        meme_text += [None] * (2 - len(meme_text))

    return meme_text[0], meme_text[1], meme_text[2]
