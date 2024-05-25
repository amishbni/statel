import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

from collections import defaultdict
from datetime import datetime


FONT_NAME = "JetBrainsMono Nerd Font Mono"


def parse_arguments():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Statistics for Telegram")
    parser.add_argument(
        "chat",
        type=str,
        help="Exported JSON file for the chat",
    )
    return parser.parse_args()


def statel(arguments: argparse.Namespace):
    message_count: dict = defaultdict(int)
    user_name: str
    with open(arguments.chat, "r") as file:
        data = json.loads(file.read())
        user_name = data["name"]
        for message in data["messages"]:
            date = datetime.strptime(message["date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m")
            message_count[date] += 1

    dates, counts = zip(*message_count.items())
    df: pd.DataFrame = pd.DataFrame({
        "dates": dates,
        "counts": counts,
    })
    df["dates"] = pd.to_datetime(df["dates"])
    plt.figure(figsize=(10, 6))
    plt.plot(df["dates"], df["counts"], marker="o", linestyle="-")

    plt.title(f"Message Frequency with {user_name}", fontname=FONT_NAME)
    plt.xlabel("Date", fontname=FONT_NAME)
    plt.xticks(fontname=FONT_NAME)
    plt.ylabel("Message Count", fontname=FONT_NAME)
    plt.yticks(fontname=FONT_NAME)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))

    plt.tight_layout()
    plt.savefig(f"{user_name}.png", dpi=300, bbox_inches="tight")


def main():
    arguments: argparse.Namespace = parse_arguments()
    statel(arguments=arguments)


if __name__ == '__main__':
    main()
