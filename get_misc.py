import argparse
import json
import os

from util import text_normalization, load_text_hash_map


def get_books(repo, map_hash_to_text):
    with open(os.path.join(repo, "ExcelOutput/BookSeriesConfig.json"), "r", encoding="utf-8") as f:
        books = json.load(f)

    with open(os.path.join("data", "books.jsonl"), "w", encoding="utf-8") as f:
        for book_id, info in books.items():
            try:
                info["BookSeries"] = text_normalization(map_hash_to_text[str(info["BookSeries"]["Hash"])])
                info["BookSeriesComments"] = text_normalization(map_hash_to_text[str(info["BookSeriesComments"]["Hash"])])
                books[book_id] = info
                print(json.dumps(info, ensure_ascii=False), file=f)
            except KeyError:
                print("warning: ", book_id, "text hash not found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="../StarRailData",
        type=str,
        required=True,
        help="data dir",
    )
    parser.add_argument("--lang", default="EN", type=str, help="language type")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)

    map_hash_to_text = load_text_hash_map(args.repo, args.lang)

    get_books(args.repo, map_hash_to_text)


