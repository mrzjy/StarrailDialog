import json
import os
import re

import pandas as pd

df = pd.read_excel("data/html_entities.xlsx")
map_html_codes_to_symbol = {
    row["Entity Name"]: row["Symbol"] if not pd.isna(row["Symbol"]) else "" for _, row in df.iterrows()
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


def load_text_hash_map(repo: str, lang: str):
    # get text map
    with open(
            os.path.join(repo, "TextMap", f"TextMap{lang}.json"),
            "r",
            encoding="utf-8",
    ) as f:
        map_hash_to_text = json.load(f)
    return map_hash_to_text
