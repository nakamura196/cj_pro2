import json
import pandas as pd

file = "/Users/nakamura/git/json/cj/iiif/collection.json"

with open(file) as f:
    df = json.load(f)

    collections = df["collections"]

    for collection in collections:

        filename = collection["@id"].split("/")[-1]

        f2 = open("../docs/collections/"+filename, 'w')
        json.dump(collection, f2, 
        ensure_ascii=False, 
        # indent=4,
            sort_keys=True, separators=(',', ': '))