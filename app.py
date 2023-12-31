from flask import Flask, render_template, redirect, request, session
import json, os
import vector_db

app = Flask(__name__)
app.secret_key = "iCitation"

CURRENT_SOURCES_FILE = "data/current_sources.json"


@app.route("/")
def home():
    session["collection_exists"] = vector_db.collection_exists()
    if "sources" not in session:
        if os.path.exists(CURRENT_SOURCES_FILE):
            with open(CURRENT_SOURCES_FILE) as file:
                session["sources"] = json.load(file)
        else:
            session["sources"] = {}
    return render_template("base.html")

@app.route("/input_text/", methods=['GET', 'POST'])
def process_text():
    if request.method == 'POST':
        text = request.form.get('input-text')
        text = text.strip()
        if text[-1] == '.':
            text = text[:-1]
        sentences = text.split(".")
        sentences = [i + ". " for i in sentences]
        session["sentences"] = sentences
    return redirect("/")

@app.route('/add_sources', methods=['GET', 'POST'])
def add_sources():
    if request.method == 'POST':

        sources_to_add = request.form.get('sources-to-add')
        citations = request.form.get('sources-citations')

        if sources_to_add:
            sources_to_add = json.loads(sources_to_add)
            citations = json.loads(citations)
            vector_db.add_sources(sources_to_add)

            current_sources: dict = session["sources"]
            current_sources.update(dict([i for i in zip(sources_to_add, citations)]))

            session["sources"] = current_sources

            with open(CURRENT_SOURCES_FILE, 'w') as file:
                json.dump(session["sources"], file)

    return redirect("/")

@app.route('/sentence/<index>')
def search_sentence(index):
    sentences = session.get("sentences")
    target_sentence = sentences[int(index)]
    session["target_sentence"] = target_sentence
    session["relevant_sources"] = vector_db.search(target_sentence)
    return redirect("/")

@app.route('/create_collection')
def create_collection():
    if not vector_db.collection_exists():
        vector_db.create_collection()
    return redirect("/")

@app.route("/delete_collection")
def delete_collection():
    vector_db.delete_collection()

    for i in ['sources', 'target_sentence', 'relevant_sources']:
        if i in session:
            session.pop(i)

    if os.path.exists(CURRENT_SOURCES_FILE):
        os.remove(CURRENT_SOURCES_FILE)
    
    return redirect("/")