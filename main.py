from flask import Flask, render_template, request, redirect
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/report")
def report():
    word = request.args.get("word")
    if word:  #word==None 일때 lower안한다는 처리
        word = word.lower()
        existing_jobs = db.get(word)
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")  #입력없을시 못벗어남
    return render_template("report.html",
                           searching_by=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs, word)
    return f"Generate CSV for {word}"
  except:
    return redirect("/")

app.run(host="0.0.0.0")
