from replit import db
import pandas as pd
import json

class EventContainer:
  counter = 0
  entries = ["id", "name", "category", "time", "duration", "location"]
  dir = ""

  def __init__(self, dir):
    self.dir = dir

  def get_from_csv(self, file_dir, opt="append"):
    df = pd.read_csv(self.dir + file_dir)
    cols = list(df.columns.values)
    for i in range(0, len(cols)):
      if not cols[i] == self.entries[i]:
        return False
    if opt == "overwrite":
      self.purge_db()
    if opt == "overwrite" or opt == "append":
      df = df.values.tolist()
      for row in df:
        new_item = json.dumps([{
          "id": row[0],
          "name": row[1],
          "category": row[2],
          "time": row[3],
          "duration": row[4],
          "location": row[5]
        }])
        self.counter += 1
        self.add_item(new_item)
      return True
    else:
      return False

  def export_to_csv(self, file_dir):
    df = pd.DataFrame(columns=self.entries)
    for key in db.keys():
      df.loc[len(df.index)] = json.loads(db[key])
    print(df)
    df.to_csv(file_dir, index=False)

  def add_item(self, item):
    print(item)
    data = json.loads(item)
    for key in db.keys():
      if data[0]['id'] == json.loads(db[key])[0]:
        return False
    new_row = []
    for col in self.entries:
      new_row.append(data[0][col])
    self.counter += 1
    db[data[0]['id']] = json.dumps(new_row)
    return True

  def delete_by_id(self, id):
    for key in db.keys():
      if json.loads(db[key])[0] == int(id):
        del db[str(id)]
        self.counter -= 1
        return True
    return False

  def contains(self, id):
    for key in db.keys():
      if json.loads(db[key])[0] == int(id):
        return True
    return False

  def get_id_by_name(self, event_name):
    valid_ids = []
    for key in db.keys():
      if event_name in json.loads(db[key])[1].lower():
        valid_ids.append(key)
    return valid_ids

  def print_db(self):
    for key in db.keys():
      print(json.loads(db[key]))

  def get_ids(self):
    valid_ids = []
    for key in db.keys():
      valid_ids.append(json.loads(db[key])[0])
    return valid_ids

  def get_size(self):
    return self.counter

  def get_events(self):
    events = []
    for key in db.keys():
      row = json.loads(db[key])
      new_item = json.dumps({
        "id": row[0],
        "name": row[1],
        "category": row[2],
        "time": row[3],
        "duration": row[4],
        "location": row[5]
      })
      events.append(new_item)
    return json.dumps(events)

  def purge_db(self):
    keys = db.keys()
    for key in keys:
      del db[key]
    self.counter = 0

"""
eventContainer = EventContainer('')
eventContainer.purge_db()
eventContainer.add_item(
  json.dumps([{
    "id": 0,
    "name": "test_event1",
    "category": "community engagement",
    "time": 1668034685,
    "duration": 3600,
    "location": "111 ddd st, dallas tx 75023"
  }],
             separators=(',', ':')))
eventContainer.add_item(
  json.dumps([{
    "id": 1,
    "name": "test_event2",
    "category": "community engagement",
    "time": 1668034685,
    "duration": 3600,
    "location": "111 ddd st, dallas tx 75023"
  }],
             separators=(',', ':')))
eventContainer.get_from_csv('events.csv')
print(eventContainer.get_ids())
eventContainer.print_db()
print(eventContainer.get_id_by_name('ddin'))
print(eventContainer.get_events())
eventContainer.export_to_csv('new-events.csv')
"""
"""
eventContainer.purge_db()
eventContainer.add_item(
  json.dumps([{
    "id": 0,
    "name": "test_event1",
    "category": "community engagement",
    "time": 1668034685,
    "duration": 3600,
    "location": "111 ddd st, dallas tx 75023"
  }],
             separators=(',', ':')))
eventContainer.add_item(
  json.dumps([{
    "id": 0,
    "name": "test_event1",
    "category": "community engagement",
    "time": 1668034685,
    "duration": 3600,
    "location": "111 ddd st, dallas tx 75023"
  }],
             separators=(',', ':')))
eventContainer.print_db()
"""
