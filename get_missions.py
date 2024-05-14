import argparse
import copy
import glob
import json
import os
import re

from util.common import text_normalization, load_text_hash_map


def get_missions(repo: str, map_hash_to_text: dict, lang: str):
    def unhash_info(info: dict):
        for key, item in info.items():
            if isinstance(item, dict) and "Hash" in item:
                if str(item["Hash"]) in map_hash_to_text:
                    info[key] = text_normalization(map_hash_to_text[str(item["Hash"])])
                else:
                    print(f"warning: {item['Hash']} hash key not found")
                    info[key] = "N/A"
        return info

    mission_file = os.path.join(repo, "ExcelOutput/MainMission.json")
    with open(mission_file, "r", encoding="utf-8") as f:
        mission_map = json.load(f)
    mission_map = {mission_id: unhash_info(info) for mission_id, info in mission_map.items()}

    submission_file = os.path.join(repo, "ExcelOutput/SubMission.json")
    with open(submission_file, "r", encoding="utf-8") as f:
        submission_map = json.load(f)
    submission_map = {mission_id: unhash_info(info) for mission_id, info in submission_map.items()}

    # find mission-submission hierarchy
    def get_submission_text_feature(submission: dict):
        return submission["TargetText"] + "|||" + submission["DescrptionText"]

    mission_hierarchy_map = {}
    for mission_dir in glob.iglob(os.path.join(repo, "Config/Level/Mission/*")):
        for file in glob.iglob(os.path.join(mission_dir, "MissionInfo_*.json")):
            with open(file, "r", encoding="utf-8") as f:
                info = json.load(f)
                if str(info["MainMissionID"]) not in mission_map or "N/A" in mission_map[str(info["MainMissionID"])]["Name"]:
                    continue
                # there are repetitive texts (maybe sub tasks sharing the same submission)
                # we merge them with unique texts and a list of ids
                map_text_feature_to_submissions = {}
                for sub in info["SubMissionList"]:
                    if str(sub["ID"]) not in submission_map:
                        continue
                    submission = submission_map[str(sub["ID"])]
                    text_feature = get_submission_text_feature(submission)
                    if text_feature not in map_text_feature_to_submissions:
                        map_text_feature_to_submissions[text_feature] = []
                    map_text_feature_to_submissions[text_feature].append(sub["ID"])

                merged_submissions = []
                for text_feature, submissions in map_text_feature_to_submissions.items():
                    target, desc = text_feature.split("|||")
                    if "N/A" in target:
                        continue
                    merged_submissions.append({"submission_ids": submissions, "target": target, "desc": desc})

                mission = mission_map[str(info["MainMissionID"])]
                mission = {
                    "name": mission["Name"],
                    "next_missions": mission["NextMainMissionList"],
                    "next_track_mission": mission.get("NextTrackMainMission", None),
                    "chapter_id": mission.get("ChapterID", None),
                    "reward_id": mission.get("RewardID", None),
                }
                mission_hierarchy_map[info["MainMissionID"]] = {
                    "mission": mission,
                    "submissions": merged_submissions
                }

    os.makedirs(f"data/missions/{lang}", exist_ok=True)
    with open(f"data/missions/{lang}/missions.json", "w", encoding="utf-8") as f:
        json.dump(mission_hierarchy_map, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
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

    output_dir = "data"
    output_dir = os.path.join(output_dir, "misc", args.lang)
    os.makedirs(output_dir, exist_ok=True)

    map_hash_to_text = load_text_hash_map(args.repo, args.lang)
    map_hash_to_text["371857150"] = "N/A"

    get_missions(
        repo=args.repo,
        map_hash_to_text=map_hash_to_text,
        lang=args.lang,
    )
