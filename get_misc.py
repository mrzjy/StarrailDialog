import argparse
import json
import os
import re

from util.common import text_normalization, load_text_hash_map


def get_misc(
    input_path: str, map_hash_to_text: dict, output_path: str = None, max_count=-1
):
    with open(input_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    unique_set = set()
    count = 0
    outputs = []
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
            outputs.append(info)
            count += 1
            if 0 < max_count <= count:
                return
        except KeyError:
            print("warning: ", idx, "text hash not found")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            for info in outputs:
                print(json.dumps(info, ensure_ascii=False), file=f)
    return outputs


def get_avatar(repo: str, map_hash_to_text: dict, output_path: str, max_count=-1):
    repo = os.path.join(repo, "ExcelOutput")
    with open(os.path.join(repo, "VoiceAtlas.json"), "r", encoding="utf-8") as f:
        map_avatar_to_voiceline = {}
        for avatar_id, info in json.load(f).items():
            if avatar_id not in map_avatar_to_voiceline:
                map_avatar_to_voiceline[avatar_id] = []
            for sub_info in info.values():
                voice_line = {
                    "title": text_normalization(
                        map_hash_to_text[str(sub_info["VoiceTitle"]["Hash"])]
                    ),
                    "Voice_M": text_normalization(
                        map_hash_to_text[str(sub_info["Voice_M"]["Hash"])]
                    ),
                    "Voice_F": text_normalization(
                        map_hash_to_text[str(sub_info["Voice_F"]["Hash"])]
                    ),
                    "UnlockDesc": text_normalization(
                        map_hash_to_text[str(sub_info["UnlockDesc"]["Hash"])]
                    ),
                }
                for key in list(voice_line.keys()):
                    if "N/A" in voice_line[key]:
                        del voice_line[key]
                map_avatar_to_voiceline[avatar_id].append(voice_line)

    with open(os.path.join(repo, "StoryAtlas.json"), "r", encoding="utf-8") as f:
        map_avatar_to_story = {}
        for avatar_id, info in json.load(f).items():
            if avatar_id not in map_avatar_to_story:
                map_avatar_to_story[avatar_id] = {}
            for story_id, sub_info in info.items():
                map_avatar_to_story[avatar_id][story_id] = text_normalization(
                    map_hash_to_text[str(sub_info["Story"]["Hash"])]
                )

    with open(os.path.join(repo, "AvatarCamp.json"), "r", encoding="utf-8") as f:
        map_camp_to_name = json.load(f)
        for camp_id, info in map_camp_to_name.items():
            map_camp_to_name[camp_id] = text_normalization(
                map_hash_to_text[str(info["Name"]["Hash"])]
            )
    with open(os.path.join(repo, "AvatarAtlas.json"), "r", encoding="utf-8") as f:
        map_avatar_to_atlas = json.load(f)
        for avatar_id, info in map_avatar_to_atlas.items():
            map_avatar_to_atlas[avatar_id] = {
                "camp": map_camp_to_name[str(info["CampID"])],
                "CV_CN": map_hash_to_text[str(info["CV_CN"]["Hash"])],
                "CV_JP": map_hash_to_text[str(info["CV_JP"]["Hash"])],
                "CV_KR": map_hash_to_text[str(info["CV_KR"]["Hash"])],
                "CV_EN": map_hash_to_text[str(info["CV_EN"]["Hash"])],
            }

    with open(os.path.join(repo, "AvatarSkillConfig.json"), "r", encoding="utf-8") as f:
        map_skill_to_info = json.load(f)
        for skill_id, info in map_skill_to_info.items():
            level_info_list = []
            for level_id, sub_info in info.items():
                param_list = [p["Value"] for p in sub_info["ParamList"]]
                simple_param_list = [p["Value"] for p in sub_info["SimpleParamList"]]
                level_info = {
                    level_id: {
                        key: text_normalization(
                            map_hash_to_text.get(str(sub_info[key]["Hash"]), "N/A")
                        )
                        for key in [
                            "SkillDesc",
                            "SimpleSkillDesc",
                        ]
                    }
                }
                for i, (param, simple_param) in enumerate(
                    zip(param_list, simple_param_list)
                ):
                    if isinstance(param, float):
                        param = f"{100 * param:0.0f}"
                        simple_param = f"{100 * simple_param:0.0f}"
                    else:
                        param = f"{param}"
                        simple_param = f"{simple_param}"
                    level_info[level_id]["SkillDesc"] = re.sub(
                        f"#{i+1}\[[^]]+]", param, level_info[level_id]["SkillDesc"]
                    )
                    level_info[level_id]["SimpleSkillDesc"] = re.sub(
                        f"#{i+1}\[[^]]+]",
                        simple_param,
                        level_info[level_id]["SimpleSkillDesc"],
                    )
                assert "#" not in level_info[level_id]["SkillDesc"]
                level_info_list.append(level_info)

            map_skill_to_info[skill_id] = {
                "SkillName": map_hash_to_text.get(str(sub_info["SkillName"]["Hash"])),
                "SkillTag": map_hash_to_text.get(str(sub_info["SkillTag"]["Hash"])),
                "SkillTypeDesc": map_hash_to_text.get(
                    str(sub_info["SkillTypeDesc"]["Hash"])
                ),
                "levels": level_info_list,
            }

    with open(os.path.join(repo, "AvatarConfig.json"), "r", encoding="utf-8") as f:
        basic_info = json.load(f)
        map_avatar_to_info = {}
        for avatar_id, info in basic_info.items():
            if avatar_id not in map_avatar_to_story:
                continue
            map_avatar_to_info[avatar_id] = {
                # todo: AvatarCutinIntroText, AvatarDesc, AvatarFullName is none
                "basic": {
                    "Name": text_normalization(
                        map_hash_to_text[str(info["AvatarName"]["Hash"])]
                    ),
                    "Camp": map_avatar_to_atlas[avatar_id]["camp"],
                    "AvatarVOTag": info["AvatarVOTag"],
                    "DamageType": info["DamageType"],
                    "AvatarBaseType": info["AvatarBaseType"],
                    "CV": {
                        k: v
                        for k, v in map_avatar_to_atlas[avatar_id].items()
                        if "CV" in k
                    },
                },
                "dialogue_lines": map_avatar_to_voiceline[avatar_id],
                "story": map_avatar_to_story[avatar_id],
                "skill": [map_skill_to_info[str(s)] for s in info["SkillList"]],
            }

    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        # json.dump(map_avatar_to_info, f, ensure_ascii=False, indent=4)
        for i, (_, info) in enumerate(map_avatar_to_info.items()):
            avatar_name = info["basic"]["Name"]
            print(json.dumps({avatar_name: info}, ensure_ascii=False), file=f)
            count += 1
            if 0 < max_count <= count:
                break


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

    # simple tasks
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

    # complex tasks
    get_avatar(
        args.repo,
        map_hash_to_text,
        output_path=os.path.join(output_dir, "avatar.jsonl"),
        max_count=args.max_count,
    )
