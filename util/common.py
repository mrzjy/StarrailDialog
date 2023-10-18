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


def parse_on_sequence(info: dict, map_hash_to_text: dict, map_sent_id_to_hash_info: dict) -> list:
    sessions = []
    for sequence in info.get("OnStartSequece", []):
        session = []
        for element in sequence.get("TaskList", []):
            if element["$type"] == "RPG.GameCore.PlayAndWaitSimpleTalk":
                sub_session = {"type": element["$type"], "conversations": []}
                for simple_talk in element["SimpleTalkList"]:
                    speaker_content = get_speaker_content(
                        simple_talk["TalkSentenceID"],
                        map_hash_to_text,
                        map_sent_id_to_hash_info,
                    )
                    if speaker_content:
                        simple_talk["role"] = speaker_content["role"]
                        simple_talk["content"] = speaker_content["content"]
                        simple_talk["type"] = "PlayAndWaitSimpleTalk"
                        sub_session["conversations"].append(simple_talk)
                if sub_session["conversations"]:
                    session.append(sub_session)
            elif element["$type"] == "RPG.GameCore.PlayOptionTalk":
                sub_session = {"type": element["$type"], "options": []}
                for option in element["OptionList"]:
                    try:
                        speaker_content = get_speaker_content(
                            option["TalkSentenceID"],
                            map_hash_to_text,
                            map_sent_id_to_hash_info,
                        )
                        option["next_TalkSentenceID"] = re.search(
                            r"(TalkSentence_)*(?P<sent_id>\d+)",
                            option["TriggerCustomString"],
                        )["sent_id"]
                        del option["TriggerCustomString"]
                        del option["OptionIconType"]
                        option["role"] = speaker_content["role"]
                        option["content"] = speaker_content["content"]
                        sub_session["options"].append(option)
                    except:
                        pass
                if sub_session["options"]:
                    session.append(sub_session)
            elif element["$type"] in {
                "RPG.GameCore.WaitCustomString",
                "RPG.GameCore.TriggerCustomString",
            }:
                speaker_content = None
                try:
                    sent_id = int(
                        re.search(
                            r"(TalkSentence_)*(?P<sent_id>\d+)",
                            element["CustomString"]["Value"],
                        )["sent_id"]
                    )
                    speaker_content = get_speaker_content(
                        sent_id,
                        map_hash_to_text,
                        map_sent_id_to_hash_info,
                    )
                except TypeError:
                    sent_id = element["CustomString"]["Value"]
                except KeyError:
                    continue
                sub_session = {
                    "type": element["$type"],
                    "TalkSentenceID": sent_id,
                }
                if speaker_content:
                    sub_session["role"] = speaker_content["role"]
                    sub_session["content"] = speaker_content["content"]

                session.append(sub_session)
            elif element["$type"] == "RPG.GameCore.EndPerformance":
                sub_session = {"type": "RPG.GameCore.EndPerformance"}
                if session:
                    session.append(sub_session)
        if session:
            sessions.append(session)

    return sessions


def merge_on_sequence_sessions(sessions: list):
    merged_sessions = []
    merged_session = []
    for session in sessions:
        for i, sub_session in enumerate(session):
            if (
                    merged_session
                    and merged_session[-1]["type"] == "RPG.GameCore.WaitCustomString"
            ):
                if (
                        sub_session["type"] == "RPG.GameCore.PlayAndWaitSimpleTalk"
                        and sub_session["conversations"][0]["TalkSentenceID"]
                        == merged_session[-1]["TalkSentenceID"]
                ):
                    del merged_session[-1]

            if (
                    merged_session
                    and sub_session["type"] == "RPG.GameCore.TriggerCustomString"
            ):
                merged_session[-1]["next_TalkSentenceID"] = sub_session[
                    "TalkSentenceID"
                ]
                continue

            merged_session.append(sub_session)

        if (
                merged_session
                and merged_session[-1]["type"] == "RPG.GameCore.EndPerformance"
        ):
            merged_sessions.append(merged_session)
            merged_session = []
    return merged_sessions
