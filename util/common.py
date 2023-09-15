import json
import os
import re

import pandas as pd

df = pd.read_excel("data/html_entities.xlsx")
map_html_codes_to_symbol = {
    row["Entity Name"]: row["Symbol"] if not pd.isna(row["Symbol"]) else ""
    for _, row in df.iterrows()
}


def text_normalization(content: str) -> str:
    # replace all html entities
    for entity in re.findall("&[a-zA-Z0-9]+;", content):
        if entity in map_html_codes_to_symbol:
            content = content.replace(entity, map_html_codes_to_symbol[entity])
    # remove html tags
    content = re.sub(r"\s*<br />\s*", " ", content)
    content = re.sub(r" ", " ", content)
    content = re.sub(r"<[^>]+>", "", content)
    return content


def load_text_hash_map(repo: str, lang: str) -> dict[str, str]:
    # get text map
    with open(
        os.path.join(repo, "TextMap", f"TextMap{lang}.json"),
        "r",
        encoding="utf-8",
    ) as f:
        map_hash_to_text = json.load(f)
    return map_hash_to_text


def load_sentence_map(repo: str) -> dict[str, dict]:
    with open(
        os.path.join(repo, "ExcelOutput/TalkSentenceConfig.json"),
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_speaker_content(
    sent_id, map_hash_to_text: dict[str, str], map_sent_id_to_hash_info: dict[str, dict]
) -> dict[str, str]:
    try:
        hash_info = map_sent_id_to_hash_info[str(sent_id)]
        speaker_name_hash_id = hash_info["TextmapTalkSentenceName"]["Hash"]
        sentence_hash_id = hash_info["TalkSentenceText"]["Hash"]
        speaker = text_normalization(map_hash_to_text[str(speaker_name_hash_id)])
        sentence = text_normalization(map_hash_to_text[str(sentence_hash_id)])
    except KeyError:
        print(f"warning: {sent_id} not found in text hash map")
        return None
    return {"role": speaker, "content": sentence}
