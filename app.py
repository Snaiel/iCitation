from flask import Flask, render_template

app = Flask(__name__)

with open("input.txt") as file:
    input_text = file.read()

sentences = input_text.split(".")
sentences = [i.strip().replace("\n", " ") + ". " for i in sentences]

print(sentences)

@app.route("/")
def hello_world():
    return render_template("base.html", content=sentences)