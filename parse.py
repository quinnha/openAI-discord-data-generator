import json
import re
import os
from collections import defaultdict

DIR_PATH = 'logs/'

# Change to your discord username and discriminator (after the #)
USER_NAME = "bagel"
DISCRIMINATOR = "4824"

reply_counter = 0
word_counter = 0

# regex compile emojis
emoj = re.compile("["
                  u"\U0001F600-\U0001F64F"  # emoticons
                  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                  u"\U0001F680-\U0001F6FF"  # transport & map symbols
                  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                  u"\U00002500-\U00002BEF"  # chinese char
                  u"\U00002702-\U000027B0"
                  u"\U00002702-\U000027B0"
                  u"\U000024C2-\U0001F251"
                  u"\U0001f926-\U0001f937"
                  u"\U00010000-\U0010ffff"
                  u"\u2640-\u2642"
                  u"\u2600-\u2B55"
                  u"\u200d"
                  u"\u23cf"
                  u"\u23e9"
                  u"\u231a"
                  u"\ufe0f"  # dingbats
                  u"\u3030"
                  "]+", re.UNICODE)


def clean_text(text):
    text = re.sub(r'@\w+', '', text)  # discord mentions
    text = re.sub(r":(\w+):", "", text)  # discord emojis
    text = re.sub(r'http\S+', "", text)  # links
    text = re.sub(r'\|+|[\*_]+|\`+|\~\~+|\>+|\>+>+|\n',
                  "", text)  # discord markdown
    text = re.sub(emoj, '', text)  # emojis
    text += " "
    return text


# clear output file
with open('output.jsonl', 'w') as outfile:
    pass

file_list = os.listdir(DIR_PATH)

# get every file in DIR_PATH subdirectory
for file in file_list:
    with open('{}{}'.format(DIR_PATH, file), 'r', encoding="utf8") as f:
        data = json.load(f)

    messages = data["messages"]
    message_dict = defaultdict(list)
    for msg in messages:
        message_dict[msg["id"]].append(msg["content"])

    user_replies = [msg for msg in messages if (
        msg["author"]["name"] == USER_NAME and msg["author"]["discriminator"] == DISCRIMINATOR and msg["type"] == "Reply")]

    # get id of msg that the user replied to
    prompt_completion = {}
    for reply in user_replies:
        prompt_id = reply["reference"]["messageId"]

        prompt_msg = message_dict[prompt_id]
        content_msg = reply["content"]

        # if the msg exists (not deleted)
        if prompt_msg:
            prompt_msg = prompt_msg[0]
            prompt_msg = clean_text(prompt_msg)
            content_msg = clean_text(content_msg)

            # if the msg is more than 4 words
            if len(prompt_msg.split(" ")) > 4 and len(content_msg.split(" ")) > 4:
                reply_counter += 1
                word_counter += len(prompt_msg.split(" ")) + \
                    len(content_msg.split(" "))
                prompt_completion[prompt_msg.strip()] = content_msg.strip()

    with open('output.jsonl', 'a') as outfile:
        for key in prompt_completion.keys():
            json.dump({"prompt": "{}\n\n".format(key),
                       "completion": " {}\n".format(prompt_completion[key])}, outfile)
            outfile.write('\n')

print("Operation complete, find the log in output.jsonl")
print("Replies Parsed:", reply_counter)
print("Words Parsed", word_counter)
print("Approximate Tokens", word_counter * 1000/750)
