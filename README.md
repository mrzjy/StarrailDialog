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
  - [x] Train visitor
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

#### Dialogues

The resulting extraction remains structured, waiting for you to be further processed.

- Code

~~~
python get_dialogues_messages.py --lang=CHS --repo=PATH_TO_STARRAIL_DATA
python get_dialogues_train_visitor.py --lang=CHS --repo=PATH_TO_STARRAIL_DATA
~~~

- Example

~~~
# messages.jsonl
{"ID": 1150300, "StartMessageItemIDList": [115030004], "IsPerformMessage": true, "contacts": [{"ID": 1004, "Name": "瓦尔特", "IconPath": "SpriteOutput/AvatarRoundIcon/1004.png", "SignatureText": "列车组各位，随时保持联系", "ContactsType": 1, "ContactsCamp": "星穹列车"}], "messages": [{"ID": 115030004, "Sender": "瓦尔特", "ItemType": "Text", "MainText": "初步的研究结果出来了。这种空间扭曲现象催生的实体被称作「拟造花萼」", "OptionText": "N/A", "NextItemIDList": [115030005], "SectionID": 1150300}, {"ID": 115030005, "Sender": "瓦尔特", "ItemType": "Text", "MainText": "这种实体中可能存有具备实用价值的现实资料。你们与其接触时要倍加小心，空间扭曲现象的本质就是无法解释的混沌，很难判断其中是否还蕴藏着某些危险要素", "OptionText": "N/A", "NextItemIDList": [], "SectionID": 1150300}]}

# train_visitor.jsonl
[{"type": "RPG.GameCore.PlayAndWaitSimpleTalk", "conversations": [{"TalkSentenceID": 500100102, "ProtectTime": 0.3, "role": "艾丝妲", "content": "如果在列车的这个位置布设空间望远镜，应该能观测到更短的波长……", "type": "PlayAndWaitSimpleTalk"}, {"TalkSentenceID": 500100103, "ProtectTime": 0.3, "role": "艾丝妲", "content": "嗯，方向感觉还不错。", "type": "PlayAndWaitSimpleTalk"}]}, {"type": "RPG.GameCore.PlayOptionTalk", "options": [{"TalkSentenceID": 500100104, "next_TalkSentenceID": "500100105", "role": "{NICKNAME}", "content": "有新论文选题？"}, {"TalkSentenceID": 500100107, "next_TalkSentenceID": "500100108", "role": "{NICKNAME}", "content": "刚刚在工作吗？"}]}, {"type": "RPG.GameCore.PlayAndWaitSimpleTalk", "conversations": [{"TalkSentenceID": 500100105, "ProtectTime": 0.3, "role": "艾丝妲", "content": "是呀。之前苦思冥想不得其法，一登上列车，想法就接二连三地冒出来，灵感真是折磨人的小妖怪。", "type": "PlayAndWaitSimpleTalk"}, {"TalkSentenceID": 500100106, "ProtectTime": 0.3, "role": "艾丝妲", "content": "这篇论文或许和列车有关…到时候还要请你们接受我的采访，多多提供一手资料。", "type": "PlayAndWaitSimpleTalk"}], "next_TalkSentenceID": 500100110}, {"type": "RPG.GameCore.PlayAndWaitSimpleTalk", "conversations": [{"TalkSentenceID": 500100108, "ProtectTime": 0.3, "role": "艾丝妲", "content": "当然不是啦。我又不是以工作名义来参观的，而是受到了{NICKNAME}的邀请，对吧？", "type": "PlayAndWaitSimpleTalk"}, {"TalkSentenceID": 500100109, "ProtectTime": 0.3, "role": "艾丝妲", "content": "所以在登上列车的那一刻，我就迫不及待调整至休假模式，全力睁大眼睛，寻找下一个论文选题。", "type": "PlayAndWaitSimpleTalk"}], "next_TalkSentenceID": 500100110}, {"type": "RPG.GameCore.PlayAndWaitSimpleTalk", "conversations": [{"TalkSentenceID": 500100110, "ProtectTime": 0.3, "role": "艾丝妲", "content": "——这些都不是重点啦。", "type": "PlayAndWaitSimpleTalk"}]}, {"type": "RPG.GameCore.PlayOptionTalk", "options": [{"TalkSentenceID": 500100111, "next_TalkSentenceID": "500100112", "role": "{NICKNAME}", "content": "今天就好好享受列车时光吧。"}]}, {"type": "RPG.GameCore.PlayAndWaitSimpleTalk", "conversations": [{"TalkSentenceID": 500100112, "ProtectTime": 0.3, "role": "艾丝妲", "content": "说得没错。", "type": "PlayAndWaitSimpleTalk"}]}, {"type": "RPG.GameCore.PlayAndWaitSimpleTalk", "conversations": [{"TalkSentenceID": 500100113, "ProtectTime": 0.3, "role": "艾丝妲", "content": "虽然之前也来过列车，不过有{NICKNAME}在的列车，我还是第一次来呢。", "type": "PlayAndWaitSimpleTalk"}, {"TalkSentenceID": 500100114, "ProtectTime": 0.3, "role": "艾丝妲", "content": "我很期待哦。", "type": "PlayAndWaitSimpleTalk"}]}, {"type": "RPG.GameCore.EndPerformance"}]
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