import json
import pandas as pd
import os
import glob

path = "/Users/nakamura/git/json/cj/iiif/collections/**/*.json"

files = glob.glob(path)

for file in files:

    print(file)

    with open(file) as f:
        df = json.load(f)

        dirname = file.split("/")[-2]
        filename = file.split("/")[-1]

        dir = "../docs/collections/"+dirname
        os.makedirs(dir, exist_ok=True)

        f2 = open(dir+"/"+filename, 'w')
        json.dump(df, f2, ensure_ascii=False, sort_keys=True, separators=(',', ': '))


path = "/Users/nakamura/git/json/cj/iiif/collections/*.json"

files = glob.glob(path)

for file in files:

    print(file)

    with open(file) as f:
        df = json.load(f)

        filename = file.split("/")[-1]

        dir = "../docs/collections/"

        f2 = open(dir+"/"+filename, 'w')
        json.dump(df, f2, ensure_ascii=False, sort_keys=True, separators=(',', ': '))