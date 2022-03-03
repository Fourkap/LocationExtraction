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
    tableau = []
    tableau2 = {}
    chapter = 1
    chapitre = 1
    for page in range(7, 45):
        content1 = test(page)
        resultpays, resultville, resultlocation, flagChapter = extractloc(content1)
        if flagChapter == 1:
            print("chapitre trouvé", chapter)
            chapter += 1
        tableauville = set(resultville)
        for ville in tableauville:
            if ville not in tableau2: tableau2[ville] = []
            tableau2[ville].append([chapter, +page + 1])
            # tableau2[ville].append(GetGeo(ville))
            # print(tableau2[ville], ville)

    # print('tableau 2 *************************************************')
    # print(tableau2)
    # for ville, data in tableau2.items():
    #     print("*********************marker*************************")
    #     print(ville)
    #     print(data)
    #     print(GetGeo(ville))
    #     print("*************fin du marqueur*******************")
    # for i in range(7, 15):
    #     content1 = test(i)
    #     resultpays, resultville, resultlocation, flagChapter = extractloc(content1)
    #     #print("flag chapter:", flagChapter)
    #     if flagChapter == 1: chapitre += 1
    #     #print(f"chapitre {chapitre}: page {i}")
    #     tableau.append(f"chapitre {chapitre}: page {i}")
    #     tableauville = []
    #     for ville in set(resultville):
    #         #print(ville)
    #         geo = GetGeo(ville)
    #         #print(geo.latitude, geo.longitude)
    #         tableauville.append(
    #             {"nomville": ville, "latitude": geo.latitude, "longitude": geo.longitude, "addresse": geo.address})
    #         # tableau.append(geo.latitude, geo.longitude)
    #     tableaupays = []
    #     for pays in set(resultpays):
    #         geo = GetGeo(pays)
    #         tableaupays.append(
    #             {"nompays": pays, "latitude": geo.latitude, "longitude": geo.longitude, "addresse": geo.address})
    #     tableauloc = []
    #     for loc in set(resultlocation):
    #         geo = GetGeo(loc)
    #         tableauloc.append(
    #             {"nomlocations": loc, "latitude": geo.latitude, "longitude": geo.longitude, "addresse": geo.address})
    #     tableau.append({"villes": tableauville})
    #     tableau.append({"pays": tableaupays})
    #     tableau.append({"autres locations": tableauloc})
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    tooltip = "Cliquez-ici"
    print("_____________------------------________________")

    for item in tableau2:
        geo = GetGeo(item)
        coords = (geo[1][0], geo[1][1])
        # print(item)
        test34 = item
        for item1 in tableau2[item]:
            var1 = str(item1).split(",")
            LeChapitre = "Chapitre:" + var1[0].replace("[", "")
            LaPage = "page=" + var1[1].replace("]", "")
            html = '<A HREF="static/Inferno.pdf#' + LaPage + '" target="_blank"">'
            # html = "<a href='#' onclick='window.open('Inferno.pdf', '_blank', 'fullscreen=yes'); return " \
            #        "false;'>MyPDF</a> "
            test34 += LeChapitre + LaPage + html + "<br>"

        folium.Marker(
            coords, popup=test34, tooltip=tooltip
        ).add_to(folium_map)
    return folium_map._repr_html_()
    # return jsonify(tableau)


if __name__ == '__main__':
    app.run()
