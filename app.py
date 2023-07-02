from flask import Flask, render_template, redirect
import vector_db

app = Flask(__name__)

with open("data/input.txt") as file:
    input_text = file.read()

sentences = input_text.split(".")
print(sentences)
sentences = [i + ". " for i in sentences]

target_sentence = ""
sources = {}

@app.route("/")
def hello_world():
    print("hi", sources)
    return render_template("base.html", content=sentences, sources=sources, target_sentence=target_sentence)

@app.route('/sentence/<index>')
def user_profile(index):
    global sources, target_sentence
    target_sentence = sentences[int(index)]
    sources = vector_db.search(target_sentence)
    return redirect("/")