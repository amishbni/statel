import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from collections import defaultdict
from datetime import datetime


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
    user_name: str = ""
    with open(arguments.chat, "r") as file:
        data = json.loads(file.read())
        user_name = data["name"]
        for message in data["messages"]:
            date: str = datetime.strptime(message["date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
            message_count[date] += 1

    dates, counts = zip(*message_count.items())
    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker="o", linestyle="-")
    plt.title("Message frequency per day")
    plt.xlabel("Date")
    plt.ylabel("Message Count")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.tight_layout()
    plt.savefig(f"{user_name}.png", dpi=300, bbox_inches="tight")


def main():
    arguments: argparse.Namespace = parse_arguments()
    statel(arguments=arguments)


if __name__ == '__main__':
    main()
