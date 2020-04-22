import json
import pandas as pd

types = ["js", "cj"]

uri_prefix = "https://nakamura196.github.io/cj-pro2"

mapByCollection = {}

for type in types:


    df = pd.read_csv('data/list_'+type+'.csv')

    

    for i in range(len(df.index)):
        manifest = df.iloc[i, 3]

        label = df.iloc[i, 1]

        id = df.iloc[i, 6].split("/")[-1].split("-")[0]

        if id not in mapByCollection:
            mapByCollection[id] = {
                "label" : label,
                "label_en" : df.iloc[i, 2],
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

        mapByCollection[id]["manifests"].append(manifest_data)

for collection_id in mapByCollection:

    collectionObj = mapByCollection[collection_id]

    collection_data = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "https://raw.githubusercontent.com/nakamura196/cj_pro2/master/docs/collections/automatic/"+collection_id+".json", # uri_prefix + "/collections/" + collection_id + ".json",
        "@type": "sc:Collection",
        "label": collectionObj["label"] + " ("+str(len(collectionObj["manifests"]))+") 【動的生成】",
        "manifests": collectionObj["manifests"],
        "vhint": "use-thumb"
    }

    f2 = open("../docs/collections/automatic/"+collection_id+".json", 'w')
    json.dump(collection_data, f2, 
    ensure_ascii=False, 
    # indent=4,
        sort_keys=True, separators=(',', ': '))