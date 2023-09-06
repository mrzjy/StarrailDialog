import argparse
import json
import os
import traceback

from util import text_normalization, load_text_hash_map


def get_misc(input_path: str, output_path: str, map_hash_to_text: dict, max_count=-1):
    with open(input_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    unique_set = set()
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, info in items.items():
            feature_str = ""
            try:
                for key, item in info.items():
                    if isinstance(item, dict):
                        if "Hash" in item:
                            info[key] = text_normalization(
                                map_hash_to_text[str(item["Hash"])]
                            )
                            feature_str += info[key]
                        else:
                            # there may be nested dict
                            for subkey, subitem in item.items():
                                if isinstance(subitem, dict) and "Hash" in subitem:
                                    item[subkey] = text_normalization(
                                        map_hash_to_text[str(subitem["Hash"])]
                                    )
                                    feature_str += item[subkey]
                if feature_str in unique_set:
                    continue
                unique_set.add(feature_str)
                print(json.dumps(info, ensure_ascii=False), file=f)
                count += 1
                if 0 < max_count <= count:
                    return
            except KeyError:
                print("warning: ", idx, "text hash not found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="../StarRailData",
        type=str,
        required=True,
        help="data dir",
    )
    parser.add_argument("--lang", default="CHS", type=str, help="language type")
    parser.add_argument("--max_count", default=-1, type=str, help="max_count")
    args = parser.parse_args()

    output_dir = "data"
    output_dir = os.path.join(output_dir, "misc", args.lang)
    os.makedirs(output_dir, exist_ok=True)

    map_hash_to_text = load_text_hash_map(args.repo, args.lang)
    map_hash_to_text["371857150"] = "N/A"

    for input_name, output_name in [
        ("BookSeriesConfig.json", "books.jsonl"),
        ("SubMission.json", "submissions.jsonl"),
        ("ItemConfig.json", "items.jsonl"),
        ("MazeBuff.json", "maze_buff.jsonl"),
    ]:
        get_misc(
            input_path=os.path.join(args.repo, "ExcelOutput", input_name),
            output_path=os.path.join(output_dir, output_name),
            map_hash_to_text=map_hash_to_text,
            max_count=args.max_count,
        )
