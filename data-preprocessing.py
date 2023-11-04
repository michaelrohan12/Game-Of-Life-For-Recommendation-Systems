import json
import os
import sys
from pathlib import Path

start = 1001
def data_transformer(json_file):
    data = json.load(json_file)
    dict = {}

    global start 

    lst = list(range(start, 20000))
    ids = [format(x, '02d') for x in lst]

    for i in range(len(data)):
        del data[i]["id"]
        dict[ids[i]] = data[i]

    start = int(ids[i+1])
    
    
    json_object = json.dumps(dict, indent=4)

    result = Path(json_file.name)

    path = sys.path[0] + '\\data_with_ids\\' + result.name
    
    
    with open(path, "w") as outfile:
        outfile.write(json_object)
        
    return result.name


def main():
    print("Starting to intialize the ids...\n")
    path = sys.path[0] + '\\data'
    json_files = [pos_json for pos_json in os.listdir(
        path) if pos_json.endswith('.json')]
    for index, js in enumerate(json_files):
        with open(os.path.join(path, js)) as json_file:
            name = data_transformer(json_file)
            print(name + " has been successfully initialized with item ID's")
    print("\nAll the files were successfully transformed.")

if __name__ == "__main__":
    main()