"""
Global Process 1
"""
import json
import math
import time
KEY = "global_process_1"
with open("global_1.json", "r+") as f:
    data = json.load(f)
    data[KEY] = 0.0
    while True:

        data[KEY] += 1.1
        print(data[KEY])
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        time.sleep(1)