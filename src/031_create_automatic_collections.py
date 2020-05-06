import json
import pandas as pd
import os

types = [
    "js", 
    "cj"
]

uri_prefix = "https://app.cultural.jp/iiif-collection"

mapByCollection = {}

manifests = []

for type in types:

    df = pd.read_csv('data/list_'+type+'.csv')

    for i in range(len(df.index)):
        manifest = df.iloc[i, 3]

        if i % 1000 == 0:
            print(i+1, len(df.index), manifest)

        if manifest in manifests:
            continue
    
        manifests.append(manifest)

        label = df.iloc[i, 1]

        id = df.iloc[i, 6].split("/")[-1].split("-")[0]

        if id not in mapByCollection:
            mapByCollection[id] = {
                "label" : label,
                "label_en" : df.iloc[i, 2],
                "collections" : {},
                "vhint": "use-thumb"
            }

        tmp = mapByCollection[id]["collections"]
        id2 = df.iloc[i, 7]

        if id2 not in tmp:
            tmp[id2] = {
                "label" : id2,
                "label_en" : id2,
                "manifests" : [],
                "vhint": "use-thumb"
            }

        manifest_data = {
            "@id": manifest,
            "@type": "sc:Manifest",
            "label": df.iloc[i, 0]
        }

        if not pd.isnull(df.iloc[i, 4]):
            manifest_data["thumbnail"] = df.iloc[i, 4]

        if not pd.isnull(df.iloc[i, 5]):
            manifest_data["license"] = df.iloc[i, 5]

        # mapByCollection[id]["manifests"].append(manifest_data)
        tmp[id2]["manifests"].append(manifest_data)

for collection_id in mapByCollection:

    collectionObj_1 = mapByCollection[collection_id]

    tmp = collectionObj_1["collections"]

    collections = []

    count = 0

    for id2 in tmp:
        print("id2", id2)

        collectionObj = tmp[id2]

        collection_uri = uri_prefix + "/collections/automatic/" + collection_id + "/" + id2 + ".json"
        collection_label = collectionObj["label"] + " ("+str(len(collectionObj["manifests"]))+") 【動的生成】"

        collection_data = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": collection_uri,
            "@type": "sc:Collection",
            "label": collection_label,
            "manifests": collectionObj["manifests"],
            "vhint": "use-thumb"
        }

        count += len(collectionObj["manifests"])

        # collection_data["@id"] = collection_data["@id"].replace("https://raw.githubusercontent.com/nakamura196/cj_pro2/master/docs/", "https://app.cultural.jp/iiif-collection/")

        dir = "../docs/collections/automatic/" + collection_id
        os.makedirs(dir, exist_ok=True)

        f2 = open(dir + "/"+id2+".json", 'w')
        json.dump(collection_data, f2, 
        ensure_ascii=False, 
        # indent=4,
            sort_keys=True, separators=(',', ': '))

        collections.append({
            "@id": collection_uri,
            "@type": "sc:Collection",
            "label": collection_label
        })

    collection_data = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": uri_prefix + "/collections/" + collection_id + ".json",
        "@type": "sc:Collection",
        "label": collectionObj_1["label"] + " ("+str(count)+") 【動的生成】",
        "collections": collections,
        "vhint": "use-thumb"
    }

    f2 = open(dir + ".json", 'w')
    json.dump(collection_data, f2, 
    ensure_ascii=False, 
    indent=4,
        sort_keys=True, separators=(',', ': '))