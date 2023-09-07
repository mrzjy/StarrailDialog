import argparse
import glob
import json
import os
import re

from util import text_normalization


def get_speaker_content(sent_id):
    try:
        hash_info = map_sent_id_to_hash_info[str(sent_id)]
        speaker_name_hash_id = hash_info["TextmapTalkSentenceName"]["Hash"]
        sentence_hash_id = hash_info["TalkSentenceText"]["Hash"]
        speaker = text_normalization(map_id_to_text[str(speaker_name_hash_id)])
        sentence = text_normalization(map_id_to_text[str(sentence_hash_id)])
    except KeyError:
        print(f"warning: {sent_id} not found in text hash map")
        return None
    return {"role": speaker, "content": sentence}


# read textmap
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
    parser.add_argument(
        "--ignore_dialogue_branch",
        action="store_true",
        help="whether to ignore branch (only choose a random branch)",
    )
    parser.add_argument(
        "--n_utter",
        default=1000,
        type=int,
        help="max number of utterances for a session",
    )
    args = parser.parse_args()

    with open(
        os.path.join(args.repo, "TextMap", f"TextMap{args.lang}.json"),
        "r",
        encoding="utf-8",
    ) as f:
        map_id_to_text = json.load(f)
        map_id_to_text["371857150"] = "{NICKNAME}"

    with open(
        os.path.join(args.repo, "ExcelOutput/TalkSentenceConfig.json"),
        "r",
        encoding="utf-8",
    ) as f:
        map_sent_id_to_hash_info = json.load(f)

    sessions = []
    for file in glob.iglob(
        os.path.join(args.repo, "Config/Level/Mission/TrainVisitor/Act/*.json"),
        recursive=True,
    ):
        with open(file, "r", encoding="utf-8") as f:
            info = json.load(f)
            for sequence in info["OnStartSequece"]:
                session = []
                for element in sequence["TaskList"]:
                    if element["$type"] == "RPG.GameCore.PlayAndWaitSimpleTalk":
                        sub_session = {"type": element["$type"], "conversations": []}
                        for simple_talk in element["SimpleTalkList"]:
                            speaker_content = get_speaker_content(
                                simple_talk["TalkSentenceID"]
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
                            if speaker_content:
                                speaker_content = get_speaker_content(
                                    option["TalkSentenceID"]
                                )
                                option["next_TalkSentenceID"] = re.search(
                                    r"TalkSentence_(?P<sent_id>\d+)",
                                    option["TriggerCustomString"],
                                )["sent_id"]
                                del option["TriggerCustomString"]
                                del option["OptionIconType"]
                                option["role"] = speaker_content["role"]
                                option["content"] = speaker_content["content"]
                                sub_session["options"].append(option)
                        if sub_session["options"]:
                            session.append(sub_session)
                    elif element["$type"] in {
                        "RPG.GameCore.WaitCustomString",
                        "RPG.GameCore.TriggerCustomString",
                    }:
                        try:
                            sent_id = int(re.search(
                                r"TalkSentence_(?P<sent_id>\d+)",
                                element["CustomString"]["Value"],
                            )["sent_id"])
                        except TypeError:
                            sent_id = element["CustomString"]["Value"]
                        sub_session = {
                            "type": element["$type"],
                            "TalkSentenceID": sent_id,
                        }
                        session.append(sub_session)
                    elif element["$type"] == "RPG.GameCore.EndPerformance":
                        sub_session = {"type": "RPG.GameCore.EndPerformance"}
                        if session:
                            session.append(sub_session)
                if session:
                    sessions.append(session)

    output_dir = os.path.join("data", "dialogues", args.lang)
    os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "train_visitor.jsonl")
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        merged_session = []
        for session in sessions:
            # process
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
                    merged_session[-1]["next_TalkSentenceID"] = sub_session["TalkSentenceID"]
                    continue

                merged_session.append(sub_session)

            if merged_session and merged_session[-1]["type"] == "RPG.GameCore.EndPerformance":
                print(json.dumps(merged_session, ensure_ascii=False), file=f)
                merged_session = []
                count += 1
    print("Total num of dialogues:", count)
