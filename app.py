from flask import Flask, render_template, redirect

app = Flask(__name__)

with open("data/input.txt") as file:
    input_text = file.read()

sentences = input_text.split(".")
print(sentences)
sentences = [i + ". " for i in sentences]

@app.route("/")
def hello_world():
    return render_template("base.html", content=sentences)

@app.route('/sentence/<index>')
def user_profile(index):
    print(sentences[int(index)])
    return redirect("/")