# pip install -U spacy
# python -m spacy download en_core_web_sm
import re

import spacy

# Bibliothèque utiliser pour avoir une liste de ville et de pays
import geonamescache

nlp = spacy.load("en_core_web_lg")

gc = geonamescache.GeonamesCache()


def extractloc(text):
    # Chargement de la bibliothèque française de spacy

    # text = (
    # "Bonjour je m'appelle Alexandre Kaprielian, et j'habite en FRANCE du coté des Alpes.")
    flagChapter = 0
    doc = nlp(text)
    for mot in doc:
        if str(mot) == 'CHAPTER':
            # print("trouver")
            flagChapter = 1

    # Analyze de la syntaxe
    # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    # Dictionnaire de pays
    countries = gc.get_countries()

    # Dictionnaire des villes
    cities = gc.get_cities()

    cities = [*gen_dict_extract(cities, 'name')]
    countries = [*gen_dict_extract(countries, 'name')]

    entite = dict()
    # Find named entities, phrases and concepts
    tableau = [chunk.text for chunk in doc.noun_chunks]
    # print(tableau)

    # for item in tableau:
    #     #print(item)
    #     if item == "CHAPTER":
    #         print("trouver")
    #         flagChapter = 1

    entite["pays"] = []
    entite["ville"] = []
    entite["autre_localisation"] = []

    for entity in doc.ents:
        # print(entity.text, entity.label_)
        # entite.append(entity.text)
        # if entity.text == "Chapter": print("toto")
        #Recupération des entités nommées de type Localisation.
        if entity.label_ == 'GPE':
            if entity.text in countries:
                entite["pays"].append(entity.text)
            elif entity.text in cities:
                entite["ville"].append(entity.text)
                # print(entity.text)
        if entity.label_ == 'LOC':
            entite["autre_localisation"].append(entity.text)
    return entite["pays"], entite["ville"], entite["autre_localisation"], flagChapter


def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)
