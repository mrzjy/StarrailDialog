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

- [x] Messages: Text communications that the Trailblazer receives from other Characters and NPCs. [\[Ref\]](https://honkai-star-rail.fandom.com/wiki/Messages)
- [ ] Misc
  - [x] Books
  - [x] Submissions
  - [x] Items

Note: 
- Extraction results are stored in the "data" folder. I won't provide full extraction results, please run the code yourself to get full extracted data.
- Bugs or data problems possibly exist, feel free to PR (although the author is not very active...)
- There are string variables (e.g., "{NICKNAME}" stands for trailblazer's name) in the corpus.

#### Messages

The resulting extraction remains structured, waiting for you to be further processed.

- Code

~~~
python get_messages.py --lang=CHS --repo=PATH_TO_STARRAIL_DATA
~~~

- Example

~~~
{
   "ID":1000200,
   "StartMessageItemIDList":[
      100020001
   ],
   "IsPerformMessage":true,
   "contacts":[
      {
         "ID":1013,
         "Name":"Herta",
         "IconPath":"SpriteOutput/AvatarRoundIcon/1013.png",
         "SignatureText":"This account is disabled | Business Contact: Asta",
         "ContactsType":1,
         "ContactsCamp":"Herta Space Station"
      }
   ],
   "messages":[
      {
         "ID":100020001,
         "Sender":"NPC",
         "ItemType":"Text",
         "MainText":"Hey, {NICKNAME}, it's Herta. I need you for something good",
         "OptionText":"N/A",
         "NextItemIDList":[
            100020002
         ],
         "SectionID":1000200
      },
      {
         "ID":100020002,
         "Sender":"NPC",
         "ItemType":"Text",
         "MainText":"Come to my office quickly! I'm waiting!",
         "OptionText":"N/A",
         "NextItemIDList":[
            100020003
         ],
         "SectionID":1000200
      },
      {
         "ID":100020003,
         "Sender":"PlayerAuto",
         "ItemType":"Text",
         "MainText":"?",
         "OptionText":"N/A",
         "NextItemIDList":[
            100020004,
            100020005
         ],
         "SectionID":1000200
      },
      {
         "ID":100020004,
         "Sender":"Player",
         "ItemType":"Text",
         "MainText":"But you're right next to me",
         "OptionText":"But you're right next to me",
         "NextItemIDList":[
            100020006
         ],
         "SectionID":1000200
      },
      {
         "ID":100020005,
         "Sender":"Player",
         "ItemType":"Text",
         "MainText":"Can't you just tell me",
         "OptionText":"Can't you just tell me",
         "NextItemIDList":[
            100020006
         ],
         "SectionID":1000200
      },
      {
         "ID":100020006,
         "Sender":"NPC",
         "ItemType":"Text",
         "MainText":"[Automatic reply] Hi, I'm currently unavailable, and I won't be contacting you later",
         "OptionText":"N/A",
         "NextItemIDList":[
            100020007
         ],
         "SectionID":1000200
      },
      {
         "ID":100020007,
         "Sender":"PlayerAuto",
         "ItemType":"Text",
         "MainText":"???",
         "OptionText":"N/A",
         "NextItemIDList":[
            
         ],
         "SectionID":1000200
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
~~~