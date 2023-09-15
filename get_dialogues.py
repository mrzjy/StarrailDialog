import argparse

from util.common import load_text_hash_map, load_sentence_map
from util.message_util import get_message
from util.train_visitor_util import get_train_visitor

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

    map_hash_to_text = load_text_hash_map(args.repo, args.lang)
    map_hash_to_text["371857150"] = "{NICKNAME}"

    map_sent_id_to_hash_info = load_sentence_map(args.repo)

    get_message(args.repo, args.lang, map_hash_to_text, max_count=args.max_count)
    get_train_visitor(
        args.repo,
        args.lang,
        map_hash_to_text,
        map_sent_id_to_hash_info,
        max_count=args.max_count,
    )
