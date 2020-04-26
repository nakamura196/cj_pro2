import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import time
import sys
import argparse

types = [
    "cj", 
    # "js"
]

manifests = []

for type in types:

    print(type)

    rows = []
    rows.append(["title", "label", "label_en", "manifest", "thumbnail", "license", "id"])

    flg = True

    page = 0

    unit = 10000

    while (flg):

        print(page)

        endpoint = "https://ld.cultural.jp/sparql" if type == "cj" else "https://jpsearch.go.jp/rdf/sparql"

        sparql = SPARQLWrapper(endpoint=endpoint, returnFormat='json')

        # time.sleep(1)

        # ?o schema:url ?manifest . MINUS { ?manifest a <http://iiif.io/api/presentation/2#Manifest> . }
        # optional { ?p schema:name ?name . filter(lang(?name) = "en") }
        # optional { ?o schema:license ?license . }
        # optional { ?s schema:image ?thumbnail }
        # ?name ?license 

        q = ("""
            PREFIX jps: <https://jpsearch.go.jp/term/property#>
            PREFIX schema: <http://schema.org/>
            PREFIX type: <https://jpsearch.go.jp/term/type/>
            PREFIX chname: <https://jpsearch.go.jp/entity/chname/>
            PREFIX place: <https://jpsearch.go.jp/entity/place/>
            PREFIX time: <https://jpsearch.go.jp/entity/time/>
            PREFIX work: <https://jpsearch.go.jp/entity/work/>
            PREFIX role: <https://jpsearch.go.jp/term/role/>
            PREFIX keyword: <https://jpsearch.go.jp/term/keyword/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX gvname: <https://jpsearch.go.jp/entity/gvname/>
            PREFIX ncname: <https://jpsearch.go.jp/entity/ncname/>
            PREFIX ncplace: <https://jpsearch.go.jp/entity/ncplace/>
            PREFIX series: <https://jpsearch.go.jp/entity/series/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            select distinct ?title ?label ?thumbnail ?s where {
                ?s rdfs:label ?title . 
                ?s schema:image ?thumbnail . 
                ?s jps:accessInfo ?o.
                ?o schema:associatedMedia ?am . 
                minus { ?o schema:url ?manifest . ?manifest a <http://iiif.io/api/presentation/2#Manifest> } . 
                ?s jps:sourceInfo ?so.
                ?so schema:provider ?p.
                ?p rdfs:label ?label . 
            } limit """+str(unit)+""" offset """ + str(unit * page) + """
        """)
        sparql.setQuery(q)

        url = endpoint+"?query="+urllib.parse.quote(q)+"&format=json&output=json&results=json"

        r = requests.get(url)

        # 結果はJSON形式なのでデコードする
        results = json.loads(r.text)

        if len(results["results"]["bindings"]) == 0:
            flg = False

        page += 1

        for obj in results["results"]["bindings"]:

            id = obj["s"]["value"].split("/")[-1]
            manifest = "https://api.cultural.jp/iiif/"+id+"/manifest"  # obj["manifest"]["value"]

            if manifest in manifests:
                continue
            manifests.append(manifest)

            collection_id = id.split("-")[0]
            
            title = obj["title"]["value"]
            label = obj["label"]["value"]
            
            en = obj["name"]["value"] if "name" in obj else label
            thumbnail = obj["thumbnail"]["value"] if "thumbnail" in obj else ""
            license = obj["license"]["value"] if "license" in obj else ""
            

            rows.append([title, label, en, manifest, thumbnail, license, collection_id])

    import csv
    f = open("data/list_"+type+".csv", 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)

    f.close()
