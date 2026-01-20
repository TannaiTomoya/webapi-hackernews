import argparse
import time
from typing import Any, Dict, List, Optional

import requests

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

DEFAULT_MAX_ITEMS = 30
SLEEP_SECONDS = 1  # 注意事項：少なくとも1秒空ける


def fetch_json(url: str, timeout: int = 10) -> Any:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_top_story_ids() -> List[int]:
    return fetch_json(TOP_STORIES_URL)


def fetch_story(item_id: int) -> Dict[str, Any]:
    return fetch_json(ITEM_URL.format(item_id))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Hacker News top stories (title + link).")
    parser.add_argument(
        "-n", "--num", type=int, default=DEFAULT_MAX_ITEMS, help="取得する件数（デフォルト30）"
    )
    args = parser.parse_args()

    # 安全策：件数が変でも壊れないように補正（課題は30件想定）
    num = args.num
    if num < 1:
        num = 1
    if num > 30:
        num = 30

    story_ids = fetch_top_story_ids()

    printed = 0
    for story_id in story_ids:
        if printed >= num:
            break

        story = fetch_story(story_id)

        title = story.get("title")
        if not title:
            continue

        link = story.get("url")  # 無い場合は None（注意事項）
        print({"title": title, "link": link})  # 1件=1行で表示

        printed += 1
        time.sleep(SLEEP_SECONDS)  # 注意事項：1秒空ける


if __name__ == "__main__":
    main()
