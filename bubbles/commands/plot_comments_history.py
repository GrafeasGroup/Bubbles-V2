import datetime
from typing import Dict

import matplotlib.pyplot as plt
from numpy import flip

from bubbles.config import (
    client,
    PluginManager,
    rooms_list,
)


def plot_comments_history(message_data: Dict) -> None:
    # Syntax: !history [number of posts]

    count_days = {}
    args = message_data.get("text").split()
    print(args)
    number_posts = 100
    if len(args) == 2:
        if args[1] in ["-h", "--help", "-H", "help"]:
            response = client.chat_postMessage(
                channel=message_data.get("channel"),
                text="`!history [number of posts]` shows the number of new comments in #new-volunteers in function of their day. `number of posts` must be an integer between 1 and 1000 inclusive.",
                as_user=True,
            )
            return
        else:
            number_posts = max(1, min(int(args[1]), 1000))
    elif len(args) > 3:
        response = client.chat_postMessage(
            channel=message_data.get("channel"),
            text="ERROR! Too many arguments given as inputs! Syntax: `!history [number of posts]`",
            as_user=True,
        )
        return

    response = client.conversations_history(
        channel=rooms_list["new_volunteers"], limit=number_posts
    )

    for message in response["messages"]:

        # userWhoSentMessage = "[ERROR]" # Happens if a bot posts a message
        # if "user" in message.keys():
        #     userWhoSentMessage = usersList[message["user"]]
        #
        # textMessage = message["text"]
        time_send = datetime.datetime.fromtimestamp(float(message["ts"]))
        difference_days = datetime.datetime.now() - time_send
        difference_days_num = difference_days.days
        if difference_days_num not in count_days.keys():
            count_days[difference_days_num] = 0
        count_days[difference_days_num] = count_days[difference_days_num] + 1
        # print(str(timeSend)+"| "+userWhoSentMessage+" sent: "+textMessage)
        last_datetime = time_send
    client.chat_postMessage(
        channel=message_data.get("channel"),
        text=f"{str(len(response['messages']))} messages retrieved since {str(last_datetime)}",
        as_user=True,
    )
    number_posts = []
    dates = []
    for i in range(0, max(count_days.keys())):
        if i not in count_days.keys():
            number_posts.append(0)
        else:
            number_posts.append(count_days[i])
        dates.append(datetime.datetime.now() - datetime.timedelta(days=i))
    plt.plot(flip(dates), flip(number_posts))
    plt.xlabel("Data")
    plt.ylabel("Number of messages")
    plt.grid(True, which="both")
    plt.savefig("plotHour.png")
    client.files_upload(
        channels=message_data.get("channel"),
        file="plotHour.png",
        title="Just vibing.",
        as_user=True,
    )
    plt.close()


PluginManager.register_plugin(
    plot_comments_history,
    r"(?!.*who)history([0-9 ]+)?",
    help=(
        "!history [number of posts] - shows the number of new comments in"
        " #new-volunteers in function of their day. `number of posts` must"
        " be an integer between 1 and 1000 inclusive."
    ),
)
