# pip install -U spacy
# python -m spacy download en_core_web_sm
import json
import folium
import spacy
from spacy import displacy
from flask import Flask, jsonify, request, render_template
from waitress import serve
from extraction import extractloc
from pdffile1 import test
from geopy1 import GetGeo

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/", methods=["GET"])
def extraction():
    content = request.get_data().decode("utf-8")
    tableau = {}
    chapter = 1
    chapitre = 1
    #nb de page a analyser
    for page in range(7, 300):
        #recupere le resultat de l'extraction
        content1 = test(page)
        resultpays, resultville, resultlocation, flagChapter = extractloc(content1)
        if flagChapter == 1:
            print("chapitre trouvé", chapter)
            chapter += 1
        tableauville = set(resultville)
        for ville in tableauville:
            if ville not in tableau: tableau[ville] = []
            tableau[ville].append([chapter, +page + 1])
        tableaupays = set(resultpays)
        for pays in tableaupays:
            if pays not in tableau: tableau[pays] = []
            tableau[pays].append([chapter, +page + 1])
        tableaulocation = set(resultlocation)
        for location in tableaulocation:
            if location not in tableau: tableau[location] = []
            tableau[location].append([chapter, +page + 1])

    # Démarrage et initialisation de la maps folium
    start_coords = (48.875334577438565, 2.3378889831721357)
    folium_map = folium.Map(location=start_coords, zoom_start=4)
    tooltip = "Cliquez-ici"

    #Ajout des markers sur la carte depuis tableau
    for item in tableau:
        geo = GetGeo(item)
        if geo is not None:
            coords = (geo[1][0], geo[1][1])
        popup = '<h2>' + item + '</h2>' + "<br><h6>Liste des pages dans lequel apparait cette localisation</h6>"
        for item1 in tableau[item]:
            var1 = str(item1).split(",")
            LeChapitre = "Chapitre:" + var1[0].replace("[", "")
            LaPage = "page=" + var1[1].replace("]", "")
            html = '<A HREF="static/Inferno.pdf#' + LaPage + '" target="_blank"">' + LeChapitre + LaPage
            popup += html + "<br>"

        folium.Marker(
            coords, popup=popup, color='green',
            clustered_marker=True, tooltip=tooltip
        ).add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run()
