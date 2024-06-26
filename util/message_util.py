import json
import os
import traceback

from util.common import text_normalization


_UNKNOWN_SECTION_ID = -99999999999999


def get_message(repo: str, lang: str, map_hash_to_text: dict[str, str], max_count=-1):
    # get contacts camp
    with open(
            os.path.join(repo, "ExcelOutput/MessageContactsCamp.json"),
            "r",
            encoding="utf-8",
    ) as f:
        contact_camp_info = json.load(f)

    # get contacts name and signature
    with open(
            os.path.join(repo, "ExcelOutput/MessageContactsConfig.json"),
            "r",
            encoding="utf-8",
    ) as f:
        map_contact_to_info = json.load(f)
        for contact_id, info in map_contact_to_info.items():
            try:
                info["Name"] = text_normalization(
                    map_hash_to_text[str(info["Name"]["Hash"])]
                )
                info["SignatureText"] = text_normalization(
                    map_hash_to_text[str(info["SignatureText"]["Hash"])]
                )
                if "ContactsCamp" in info:
                    info["ContactsCamp"] = text_normalization(
                        map_hash_to_text[
                            str(
                                contact_camp_info[str(info["ContactsCamp"])]["Name"]["Hash"]
                            )
                        ]
                    )
                map_contact_to_info[contact_id] = info
            except:
                print(traceback.format_exc())

    # get messages
    with open(
            os.path.join(repo, "ExcelOutput/MessageItemConfig.json"),
            "r",
            encoding="utf-8",
    ) as f:
        message_info = json.load(f)
        map_section_to_messages = {}
        for message_id, item in message_info.items():
            try:
                section_id = int(item["SectionID"])
            except KeyError:
                section_id = _UNKNOWN_SECTION_ID
            if section_id not in map_section_to_messages:
                map_section_to_messages[section_id] = []
            try:
                item["MainText"] = text_normalization(
                    map_hash_to_text[str(item["MainText"]["Hash"])]
                )
                item["OptionText"] = text_normalization(
                    map_hash_to_text[str(item["OptionText"]["Hash"])]
                )
            except KeyError:
                continue
            map_section_to_messages[section_id].append(item)

    # get message group
    with open(
            os.path.join(repo, "ExcelOutput/MessageGroupConfig.json"),
            "r",
            encoding="utf-8",
    ) as f:
        map_session_id_to_contacts = {}
        for key, info in json.load(f).items():
            for section_id in info["MessageSectionIDList"]:
                if section_id not in map_session_id_to_contacts:
                    map_session_id_to_contacts[section_id] = []
                contact_id = info["MessageContactsID"]
                map_session_id_to_contacts[section_id].append(contact_id)

    with open(
            os.path.join(repo, "ExcelOutput/MessageSectionConfig.json"),
            "r",
            encoding="utf-8",
    ) as f:
        section_info = json.load(f)

    output_dir = os.path.join("data", "dialogues", lang)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "messages.jsonl")
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        # normal sections
        for section_id, info in section_info.items():
            # add contacts information
            contact_ids = map_session_id_to_contacts[int(section_id)]
            info["contacts"] = [map_contact_to_info[str(c_id)] for c_id in contact_ids]
            try:
                info["messages"] = map_section_to_messages[int(section_id)]
                info["messages"] = list(
                    filter(
                        lambda m: not (
                                m["Sender"] == "System" and m["MainText"] == "N/A"
                        ),
                        info["messages"],
                    )
                )

                for message in info["messages"]:
                    if "ContactsID" in message:
                        message["Sender"] = map_contact_to_info[
                            str(message["ContactsID"])
                        ]["Name"]
                    elif message["Sender"] == "NPC":
                        message["Sender"] = info["contacts"][0]["Name"]

            except KeyError:
                print("warning: ", section_id, "No messages found")
                continue
            print(json.dumps(info, ensure_ascii=False), file=f)
            count += 1
            if count >= max_count > 0:
                break

        for message in map_section_to_messages[_UNKNOWN_SECTION_ID]:
            print(
                json.dumps(
                    {"ID": _UNKNOWN_SECTION_ID, "messages": [message]},
                    ensure_ascii=False,
                ),
                file=f,
            )

        print("Messages: Total num of dialogues:", count)
