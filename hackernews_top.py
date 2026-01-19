import argparse
import json
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
    """トップニュースのID一覧を取得する"""
    return fetch_json(TOP_STORIES_URL)


def fetch_story(item_id: int) -> Dict[str, Any]:
    """ニュース1件の詳細を取得する"""
    return fetch_json(ITEM_URL.format(item_id))


def collect_top_stories(
    max_items: int, sleep_seconds: float = SLEEP_SECONDS
) -> List[Dict[str, Optional[str]]]:
    """
    取得結果を list にまとめて返す。
    title がないものはスキップ。
    url がない場合は None を入れる。
    """
    story_ids = fetch_top_story_ids()

    results: List[Dict[str, Optional[str]]] = []
    for story_id in story_ids:
        if len(results) >= max_items:
            break

        story = fetch_story(story_id)

        title = story.get("title")
        if not title:
            continue

        link = story.get("url")  # 無い場合は None
        results.append({"title": title, "link": link})

        time.sleep(sleep_seconds)  # 注意事項：1秒空ける

    return results


def save_as_json(path: str, data: List[Dict[str, Optional[str]]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Hacker News top stories (title + link).")
    parser.add_argument(
        "-n", "--num", type=int, default=DEFAULT_MAX_ITEMS, help="取得する件数（デフォルト30）"
    )
    parser.add_argument("-o", "--output", type=str, default="top_stories.json", help="保存するJSONファイル名")
    args = parser.parse_args()

    num = args.num
    if num < 1:
        num = 1
    if num > 30:

        num = 30

    stories = collect_top_stories(max_items=num)

    save_as_json(args.output, stories)


if __name__ == "__main__":
    main()
