from flask import Flask, render_template, redirect, request, session
import json
import vector_db

app = Flask(__name__)
app.secret_key = "iCitation"

@app.route("/")
def home():
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
        if sources_to_add:
            sources_to_add = json.loads(sources_to_add)
            vector_db.add_sources(sources_to_add)
            session["sources"] = sources_to_add
    return redirect("/")

@app.route('/sentence/<index>')
def search_sentence(index):
    sentences = session.get("sentences")
    target_sentence = sentences[int(index)]
    session["target_sentence"] = target_sentence
    session["relevant_sources"] = vector_db.search(target_sentence)
    return redirect("/")