from flask import Flask, render_template, redirect, request, session
import vector_db

app = Flask(__name__)
app.secret_key = "iCitation"

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/input_text/", methods=['GET', 'POST'])
def process_text():
    if request.method == 'POST':
        text = request.form.get('input_text')
        text = text.strip()
        if text[-1] == '.':
            text = text[:-1]
        sentences = text.split(".")
        sentences = [i + ". " for i in sentences]
        session["sentences"] = sentences
    return redirect("/")

@app.route('/sentence/<index>')
def user_profile(index):
    sentences = session.get("sentences")
    session["target_sentence"] = sentences[int(index)]
    # session["sources"] = vector_db.search(target_sentence)
    return redirect("/")