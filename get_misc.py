import argparse
import json
import os

from util import text_normalization, load_text_hash_map


def get_books(repo, map_hash_to_text, output_dir):
    with open(os.path.join(repo, "ExcelOutput/BookSeriesConfig.json"), "r", encoding="utf-8") as f:
        books = json.load(f)

    unique_set = set()
    with open(os.path.join(output_dir, "books.jsonl"), "w", encoding="utf-8") as f:
        for book_id, info in books.items():
            try:
                info["BookSeries"] = text_normalization(map_hash_to_text[str(info["BookSeries"]["Hash"])])
                info["BookSeriesComments"] = text_normalization(map_hash_to_text[str(info["BookSeriesComments"]["Hash"])])
                feature_str = info["BookSeries"] + info["BookSeriesComments"]
                if feature_str in unique_set:
                    continue
                unique_set.add(feature_str)
                print(json.dumps(info, ensure_ascii=False), file=f)
            except KeyError:
                print("warning: ", book_id, "text hash not found")


def get_submissions(repo, map_hash_to_text, output_dir):
    with open(os.path.join(repo, "ExcelOutput/SubMission.json"), "r", encoding="utf-8") as f:
        submissions = json.load(f)

    unique_set = set()
    with open(os.path.join(output_dir, "submissions.jsonl"), "w", encoding="utf-8") as f:
        for mission_id, info in submissions.items():
            try:
                info["TargetText"] = text_normalization(map_hash_to_text[str(info["TargetText"]["Hash"])])
                info["DescrptionText"] = text_normalization(map_hash_to_text[str(info["DescrptionText"]["Hash"])])
                feature_str = info["TargetText"] + info["DescrptionText"]
                if feature_str in unique_set:
                    continue
                unique_set.add(feature_str)
                print(json.dumps(info, ensure_ascii=False), file=f)
            except KeyError:
                print("warning: ", mission_id, "text hash not found")


def get_items(repo, map_hash_to_text, output_dir):
    with open(os.path.join(repo, "ExcelOutput/ItemConfig.json"), "r", encoding="utf-8") as f:
        items = json.load(f)

    unique_set = set()
    with open(os.path.join(output_dir, "items.jsonl"), "w", encoding="utf-8") as f:
        for idx, info in items.items():
            try:
                info["ItemName"] = text_normalization(map_hash_to_text[str(info["ItemName"]["Hash"])])
                info["ItemDesc"] = text_normalization(map_hash_to_text[str(info["ItemDesc"]["Hash"])])
                info["ItemBGDesc"] = text_normalization(map_hash_to_text[str(info["ItemBGDesc"]["Hash"])])
                feature_str = info["ItemName"] + info["ItemDesc"] + info["ItemBGDesc"]
                if feature_str in unique_set:
                    continue
                unique_set.add(feature_str)
                print(json.dumps(info, ensure_ascii=False), file=f)
                break
            except KeyError:
                print("warning: ", idx, "text hash not found")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="../StarRailData",
        type=str,
        required=True,
        help="data dir",
    )
    parser.add_argument("--lang", default="CHS", type=str, help="language type")
    args = parser.parse_args()

    output_dir = "data"
    output_dir = os.path.join(output_dir, "misc", args.lang)
    os.makedirs(output_dir, exist_ok=True)

    map_hash_to_text = load_text_hash_map(args.repo, args.lang)

    get_books(args.repo, map_hash_to_text, output_dir)
    get_submissions(args.repo, map_hash_to_text, output_dir)
    get_items(args.repo, map_hash_to_text, output_dir)

