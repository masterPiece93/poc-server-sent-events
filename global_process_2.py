import json
import time
KEY = "global_process_2"
with open("global_2.json", "r+") as f:
    data = json.load(f)
    data[KEY] = 0
    while True:

        data[KEY] += 1
        print(data[KEY])
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        time.sleep(1)