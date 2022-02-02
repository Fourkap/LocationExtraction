# pip install -U spacy
# python -m spacy download en_core_web_sm
import json

import spacy
from spacy import displacy
from flask import Flask, jsonify, request
from waitress import serve
from extraction import extractloc
from pdffile1 import test
from geopy1 import GetGeo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/extraction", methods=["POST"])
def extraction():
    content = request.get_data().decode("utf-8")
    tableau=[]
    chapitre = 0
    for i in range(7, 30):
        content1 = test(i)
        resultpays, resultville, resultlocation ,flagChapter = extractloc(content1)
        print("flag chapter:" ,flagChapter)
        if flagChapter == 1: chapitre += 1
        print(f"chapitre {chapitre}: page {i}")
        tableau.append(f"chapitre {chapitre}: page {i}")
        tableauville = []
        for ville in set(resultville):
            print(ville)
            geo = GetGeo(ville)
            print(geo.latitude, geo.longitude)
            tableauville.append({"nomville":ville, "latitude":geo.latitude, "longitude":geo.longitude, "addresse": geo.address})
            #tableau.append(geo.latitude, geo.longitude)
        tableaupays = []
        for pays in set(resultpays):
            geo = GetGeo(pays)
            tableaupays.append({"nompays": pays, "latitude": geo.latitude, "longitude": geo.longitude, "addresse": geo.address})
        tableauloc = []
        for loc in set(resultlocation):
            geo = GetGeo(loc)
            tableauloc.append({"nomlocations": loc, "latitude": geo.latitude, "longitude": geo.longitude, "addresse": geo.address})
        tableau.append({"villes":tableauville})
        tableau.append({"pays":tableaupays})
        tableau.append({"autres locations":tableauloc})

    return jsonify(tableau)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=1992, threads=1)
