import json
import pandas as pd
import glob

uri_prefix = "https://app.cultural.jp/iiif-collection"

collections = []

path = "/Users/nakamura/git/d_cj/cj_pro2/docs/collections/*.json"
path = "../docs/collections/*.json"

files = glob.glob(path, recursive=True)

for file in files:
    with open(file) as f:
        df = json.load(f)
        # df.pop("manifests")

        collections.append(df)



files = glob.glob("../docs/collections/automatic/*.json", recursive=True)

for file in files:
    with open(file) as f:
        df = json.load(f)
        # df.pop("manifests")

        collections.append(df)



####### Collection

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": uri_prefix+"/collection.json",
    "@type": "sc:Collection",
    "label": "Cultural Japan IIIF Collections",
    "attribution": "Cultural Japan",
    "collections": collections,
    "vhint": "use-thumb"
}

f2 = open("../docs/collection.json", 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))
