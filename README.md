# StarrailDialogue

This is a small personal project that extracts Honkai: Star Rail text corpus (including dialogue and miscellaneous items).

### Disclaimer

While this project is based on the legendary [Dim's StarRailData](https://github.com/Dimbreath/StarRailData) project, there are other more plausible data sources to achieve the same thing:

- For example, go to the relevant fandom statistics page: https://honkai-star-rail.fandom.com/wiki/Special:Statistics, and download directly the wiki data dump.

![fandom.png](img%2Ffandom.png)

### Steps

The logic is simple:
1. Git clone [Dim's StarRailData](https://github.com/Dimbreath/StarRailData)
2. Git clone and cd to this repo
3. Run the extraction codes by specifying Dim's starrail data path 


### Feature Support

What data can be extracted:

- [ ] Dialogue
  - [x] Messages: Text communications that the Trailblazer receives from other Characters and NPCs. [\[Ref\]](https://honkai-star-rail.fandom.com/wiki/Messages)
  - [ ] Train visitor
  - [ ] NPC talking
  - [ ] Mission
  - [ ] etc
- [ ] Misc
  - [x] Books
  - [x] Submissions
  - [x] Items
  - [x] Maze buffs
  - [ ] etc

Note: 
- Extraction results are stored in the "data" folder. I won't provide full extraction results, please run the code yourself to get full extracted data.
- Bugs or data problems possibly exist, feel free to PR (although the author is not very active...)
- There are string variables (e.g., "{NICKNAME}" stands for trailblazer's name) in the corpus.
- **Known Issues**:
  - There is incorrect / non-existent text hash, hence some texts would be shown as "N/A" 

#### Messages

The resulting extraction remains structured, waiting for you to be further processed.

- Code

~~~
python get_messages.py --lang=CHS --repo=PATH_TO_STARRAIL_DATA
~~~

- Example (a group chat)

~~~
{
  "ID": 1216001,
  "StartMessageItemIDList": [
    121600101
  ],
  "IsPerformMessage": true,
  "contacts": [
    {
      "ID": 78,
      "Name": "金人巷复兴小组",
      "IconPath": "SpriteOutput/AvatarRoundIcon/UI_Message_Group_Default.png",
      "SignatureText": "N/A",
      "ContactsType": 3,
      "ContactsCamp": "其他"
    }
  ],
  "messages": [
    {
      "ID": 121600101,
      "ContactsID": 80,
      "Sender": "霄翰",
      "ItemType": "Text",
      "MainText": "我很珍惜与各位相处的时光，为了避嫌，我会暂时离开这个群聊",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600102
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600102,
      "ContactsID": 80,
      "Sender": "霄翰",
      "ItemType": "Text",
      "MainText": "那么，暂时再见了！",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600103
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600103,
      "Sender": "System",
      "ItemType": "Text",
      "MainText": "霄翰已退出金人巷复兴小组",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600104
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600104,
      "ContactsID": 1207,
      "Sender": "驭空",
      "ItemType": "Sticker",
      "MainText": "N/A",
      "ItemContentID": 103007,
      "OptionText": "N/A",
      "NextItemIDList": [
        121600105
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600105,
      "ContactsID": 1207,
      "Sender": "驭空",
      "ItemType": "Text",
      "MainText": "虽然你们在谈判席上立场不同，但是想做的事情是一样的",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600106
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600106,
      "ContactsID": 1207,
      "Sender": "驭空",
      "ItemType": "Text",
      "MainText": "所以你们更应该好好辩论一番，才有机会从对方观点中补足自己",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600107
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600107,
      "ContactsID": 1207,
      "Sender": "驭空",
      "ItemType": "Text",
      "MainText": "开放的视野比任何单一的观点更有价值",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600108
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600108,
      "ContactsID": 79,
      "Sender": "明曦",
      "ItemType": "Text",
      "MainText": "谢谢驭空大人",
      "OptionText": "N/A",
      "NextItemIDList": [
        121600109,
        121600110,
        121600111
      ],
      "SectionID": 1216001
    },
    {
      "ID": 121600109,
      "Sender": "Player",
      "ItemType": "Sticker",
      "MainText": "N/A",
      "ItemContentID": 20002,
      "OptionText": "N/A",
      "NextItemIDList": [],
      "SectionID": 1216001
    },
    {
      "ID": 121600110,
      "Sender": "Player",
      "ItemType": "Sticker",
      "MainText": "N/A",
      "ItemContentID": 20004,
      "OptionText": "N/A",
      "NextItemIDList": [],
      "SectionID": 1216001
    },
    {
      "ID": 121600111,
      "Sender": "Player",
      "ItemType": "Sticker",
      "MainText": "N/A",
      "ItemContentID": 20006,
      "OptionText": "N/A",
      "NextItemIDList": [],
      "SectionID": 1216001
    }
  ]
}
~~~

#### Misc

The resulting extraction contains miscellaneous items

- Code

~~~
python get_misc.py --lang=CHS --repo=PATH_TO_STARRAIL_DATA
~~~

- Example

~~~
# books.jsonl
{"BookSeriesID": 1, "BookSeries": "Floriography Manual Attached to a Bouquet", "BookSeriesComments": "Contains commonly used floriography in Belobog. The ways of the world are condensed into this manual.", "BookSeriesNum": 1, "BookSeriesWorld": 2, "IsShowInBookshelf": true}

# submissions.jsonl
{"SubMissionID": 100010100, "TargetText": "Use a fake identity to get past security check", "DescrptionText": "The woman sauntering elegantly across the invasion site is a mystery. She mocks the victims, while also ruthlessly eliminating their oppressors.\\n Over their comms, the mysterious helper revealed that the two seem to have some sort of agenda.\\nIs their presence a sign of more chaos to come? Or is it the start of a new story?"}

# items.jsonl
{"ID": 2, "ItemMainType": "Virtual", "ItemSubType": "Virtual", "InventoryDisplayTag": 1, "Rarity": "Rare", "PurposeType": 11, "ItemName": "Credit", "ItemDesc": "This currency, used by the Interastral Peace Corporation to settle accounts with its customers, is now widely accepted as the hard currency for space travel.", "ItemBGDesc": "\"People run around fighting and trading for numbers in a terminal, but the truly precious cannot be bought.\"", "ItemIconPath": "SpriteOutput/ItemIcon/2.png", "ItemFigureIconPath": "SpriteOutput/ItemFigures/2.png", "ItemCurrencyIconPath": "SpriteOutput/ItemCurrency/2.png", "ItemAvatarIconPath": "", "PileLimit": 999999999, "CustomDataList": [], "ReturnItemIDList": []}

# maze_buff.jsonl
{"1": {"ID": 100201, "BuffSeries": 1, "BuffRarity": 1, "Lv": 1, "LvMax": 1, "ModifierName": "ADV_StageAbility_Maze_DanHeng", "InBattleBindingType": "CharacterSkill", "InBattleBindingKey": "SkillMaze", "ParamList": [], "BuffDescParamByAvatarSkillID": 100207, "BuffIcon": "SpriteOutput/BuffIcon/Inlevel/Icon1002Maze.png", "BuffName": "Splitting Spearhead", "BuffDesc": "At the start of the next battle, Dan Heng's ATK increases by #1[i]% for #2[i] turn(s).", "BuffSimpleDesc": "N/A", "BuffDescBattle": "At the start of the next battle, Dan Heng's ATK increases by #1[i]% for #2[i] turn(s).", "BuffEffect": "MazeBuffEffect_100201", "MazeBuffType": "Character", "MazeBuffIconType": "Other", "MazeBuffPool": 3, "IsDisplay": true}}
~~~