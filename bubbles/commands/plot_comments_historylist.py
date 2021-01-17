import datetime
from typing import Dict

import matplotlib.pyplot as plt
from numpy import flip

from bubbles.config import app, PluginManager, rooms_list, users_list
import warnings

from bubbles.commands.helper_functions_history.extract_author import extract_author

# get rid of matplotlib's complaining
warnings.filterwarnings("ignore")


def plot_comments_historylist(message_data: Dict) -> None:
    # Syntax: !historylist [number of posts]
    args = message_data.get("text").split()
    print(args)
    number_posts = 100
    if len(args) == 2:
        if args[1] in ["-h", "--help", "-H", "help"]:
            response = app.client.chat_postMessage(
                channel=message_data.get("channel"),
                text="`!historylist [number of posts]` shows the number of new comments in #new-volunteers in function of the mod having welcomed them. `number of posts` must be an integer between 1 and 1000 inclusive.",
                as_user=True,
            )
            return
        else:
            number_posts = max(1, min(int(args[1]), 1000))
    elif len(args) > 3:
        response = app.client.chat_postMessage(
            channel=message_data.get("channel"),
            text="ERROR! Too many arguments given as inputs! Syntax: `!historylist [number of posts]`",
            as_user=True,
        )
        return

    response = app.client.conversations_history(
        channel=rooms_list["new_volunteers"], limit=number_posts
    )
    count_reactions_people = {}
    list_volunteers_per_person = {}
    GOOD_REACTIONS = ["watch", "heavy_check_mark", "email", "exclamation_point"]
    for message in response["messages"]:

        # userWhoSentMessage = "[ERROR]" # Happens if a bot posts a message
        # if "user" in message.keys():
        #     userWhoSentMessage = usersList[message["user"]]
        #
        welcomed_username = message["text"].split(">")[0]
        welcomed_username = welcomed_username.split("|")[-1]
        author = extract_author(message, GOOD_REACTIONS)
        count_reactions_people[author] = count_reactions_people.get(author, 0) + 1
        list_volunteers_per_person[author] = list_volunteers_per_person.get(
            author, []
        ) + [welcomed_username]
    count_reactions_people = dict(sorted(count_reactions_people.items()))
    app.client.chat_postMessage(
        channel=message_data.get("channel"),
        text=f"{str(len(response['messages']))} messages retrieved. Numerical data: {count_reactions_people}",
        as_user=True,
    )
    keys_dict = list(sorted(list_volunteers_per_person.keys()))
    for key in keys_dict:
        app.client.chat_postMessage(
            channel=message_data.get("channel"),
            text=f"Volunteers welcomed by {key}: {list_volunteers_per_person[key]}",
            as_user=True,
        )


PluginManager.register_plugin(
    plot_comments_historylist,
    r"(?!.*who)listmodsTEST ([0-9 ]+)?",
    help=(
        "!historylist [number of posts] - shows the number of new comments in"
        " #new-volunteers in function of the mod having welcomed them. `number"
        "of posts` must be an integer between 1 and 1000 inclusive."
    ),
)
