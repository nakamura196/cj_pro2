import json
import pandas as pd

file = "/Users/nakamura/git/json/cj/iiif/collection.json"

with open(file) as f:
    df = json.load(f)

    collections = df["collections"]

    for collection in collections:

        print(collection["@id"])

        filename = collection["@id"].split("/")[-1]

        f2 = open("../docs/collections/"+filename, 'w')

        collection["@id"] = collection["@id"].replace("/automatic/", "/").replace("https://raw.githubusercontent.com/nakamura196/cj_pro2/master/docs/", "https://app.cultural.jp/iiif-collection/")

        json.dump(collection, f2, ensure_ascii=False, sort_keys=True, separators=(',', ': '))