# pip install -U spacy
# python -m spacy download en_core_web_sm
import json

import spacy
from spacy import displacy
from flask import Flask, jsonify, request
from waitress import serve
from extraction import extractloc

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/extraction", methods=["POST"])
def extraction():
    content = request.data.decode("utf-8")
    result = extractloc(content)
    return jsonify(result)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=1992, threads=1)
