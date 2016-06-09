from pprint import pprint
from slacker import Slacker
from settings import SLACK_API_TOKEN

slack = Slacker(SLACK_API_TOKEN)


def get_history(pageable_object, channel_id, page_size=100):
    messages = []
    last_timestamp = None

    while True:
        response = pageable_object.history(
            channel=channel_id,
            latest=last_timestamp,
            oldest=0,
            count=page_size
        ).body

        messages.extend(response['messages'])

        if response['has_more']:
            last_timestamp = messages[-1]['ts']  # -1 means last element in a list
        else:
            break
    messages.reverse()
    return messages


def get_direct_messages(slack, user_id_name_map, user_name):
    dms = slack.im.list().body['ims']
    for dm in dms:
        user = dm['user']
        name = user_id_name_map.get(user, dm['user'] + " (name unknown)")
        if name == user_name:
            messages = get_history(slack.im, dm['id'])
            return messages


def get_user_map(slack):
    users = slack.users.list().body['members']
    user_id_name_map = {}
    for user in users:
        user_id_name_map[user['id']] = user['name']
    return user_id_name_map


def get_user(user_id):
    users = slack.users.list().body['members']
    for user in users:
        if user['id'] == user_id:
            return {"username": user['name'], "icon_url": user['profile']['image_48']}


if __name__ == '__main__':
    slack = Slacker(SLACK_API_TOKEN)
    user_id_name_map = get_user_map(slack)

    messages = get_direct_messages(slack, user_id_name_map, 'franny')
    pprint(messages)
