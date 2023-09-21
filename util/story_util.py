import glob
import json
import os

from util.common import parse_on_sequence, merge_on_sequence_sessions


def get_story(
    repo: str,
    lang: str,
    map_hash_to_text: dict[str, str],
    map_sent_id_to_hash_info: dict[str, dict],
    max_count=-1,
):
    sessions = []
    for file in glob.iglob(
        os.path.join(repo, "Story/Mission/*/*.json"),
        recursive=True,
    ):
        with open(file, "r", encoding="utf-8") as f:
            info = json.load(f)
            sessions.extend(
                parse_on_sequence(info, map_hash_to_text, map_sent_id_to_hash_info)
            )

    output_dir = os.path.join("data", "dialogues", lang)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "story.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        merged_sessions = merge_on_sequence_sessions(sessions)
        for count, merged_session in enumerate(merged_sessions):
            print(json.dumps(merged_session, ensure_ascii=False), file=f)
            if count + 1 >= max_count > 0:
                break
    print("Story: Total num of dialogues:", count)
