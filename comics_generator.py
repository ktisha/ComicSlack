def parse_comics_message(message : str):
    splitted_message = message.split(" ")
    num_messages = int(splitted_message[0])
    num_scenes = int(splitted_message[1])
    title = " ".join(splitted_message[2:])
    return num_messages, num_scenes, title
