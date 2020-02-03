import json
import os

"""
Script to analyze facebook message data in json format. Expects file structure:
facebook-<username>\
  messages\
    inbox\
      <chatname>\
        message_<n>.json
        photos\
        ...
      <chatname>\
      ...
"""

DIR = "C:\\ferndev\\facebook_analyzer\\facebook-beelthefern"  # location of facebook data
NAME = "Fernando Sanchez"  # facebook name

MESSAGES_PATH = "messages\\inbox"

class Analyzer(object):
    """
    Analyzer object initializes json data in readable dictionaries in member properties. Member functions perform
    actual analysis and output results. Call member functions as desired
    """
    def __init__(self, top_level_folder, name):
        self.folder_path = top_level_folder
        self.name = name

        self.people = set()  # all people in messages
        self.chats = {}
        """
        chat_id: {
          messages: [
            {
              "sender_name": "Karen Fan",
              "timestamp_ms": 1529993628785,
              "content": "Tyty guys :D",
              "type": "Generic",
              "sticker": {
                "uri": "messages/stickers_used/18678382_114314782496463_3407427246472822784_n_114314779163130.png"
              },
              "reactions": [
                {
                  "reaction": "\u00f0\u009f\u0098\u0086",
                  "actor": "Karen Fan"
                }
              ],
            },
          ]
          people: set(),
        }
        """

    def init(self):
        # traverse root directory, and list directories as dirs and files as files
        traversal = os.path.join(self.folder_path, MESSAGES_PATH)
        all_files = []
        #i=0
        for root, dirs, files in os.walk(traversal):
            #if i>10:
            #    break
            for file in files:
                if file[-4:] == 'json':
                    all_files.append(os.path.join(root,  file))
            #i+=1
        for file in all_files:
            chat_id = file.split('\\')[-2]  # last on is file.json
            temp = self._parse_json(file)
            if chat_id not in self.chats:
                self.chats[chat_id] = temp
            else:
                self.chats[chat_id]["people"] |= temp["people"]
                self.chats[chat_id]["messages"].extend(temp["messages"])
            self.people |= temp["people"]

    def _parse_json(self, file):
        temp = {}
        with open(file, 'r') as f:
            data = json.load(f)
            # get participants
            people = set()
            for name in data["participants"]:
                people.add(name["name"])
            # get messages
            messages = data["messages"]
            temp["people"] = self._fix_people(messages)
            temp["messages"] = messages
        return temp

    def _fix_people(self, messages):
        ret = set()
        for message in messages:
            person = message["sender_name"]
            if person == "":
                ret.add("PLACEHOLDER")
            else:
                ret.add(person)
        return ret

    def get_counts(self):
        solo_counts = {}
        group_counts = {}
        for chat_id in self.chats:
            chat = self.chats[chat_id]
            dic = group_counts
            if len(chat["people"]) <= 2:
                dic = solo_counts
            recipients = chat["people"].copy()
            try:
                recipients.remove(self.name)
            except Exception as e:
                pass
            for message in chat["messages"]:
                sender = message["sender_name"]
                if sender == self.name:
                    for recipient in recipients:
                            if recipient not in dic:
                                dic[recipient] = 1
                            else:
                                dic[recipient] += 1
        return solo_counts, group_counts



x = Analyzer(DIR, NAME)
x.init()
solo, group = x.get_counts()
t = sorted(solo.items(), key=lambda item: item[1], reverse=True)
u = sorted(group.items(), key=lambda item: item[1], reverse=True)
print("SOLO")
total = 0
for i in range(len(t)):
    if i < 50:
        print(t[i])
    total += t[i][1]
print("TOTAL: {}".format(str(total)))
print("GROUP")
total2 = 0
for i in range(len(u)):
    if i< 50:
        print(u[i])
    total2 += u[i][1]
print("TOTAL: {}".format(str(total2)))