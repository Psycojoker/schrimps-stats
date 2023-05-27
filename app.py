import os
import json
import string
import random

from flask import Flask, render_template, request, flash
from wtforms import Form, FloatField, IntegerField, SelectField
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

if not os.path.exists(".secret_key"):
    secret_key = "".join(
        random.SystemRandom().choice(
            string.printable.strip()
            .replace("'", "")
            .replace('"', "")
            .replace("\\", "")
            .replace("?", "")
            .replace("!", "")
        )
        for n in range(80)
    )
    with open(".secret_key", "w") as f:
        f.write(secret_key)
else:
    app.secret_key = open(".secret_key", "r").read().strip()


@app.route("/")
def hello_world():
    return render_template("index.html")


class StatsForm(Form):
    ph = FloatField("pH")
    ph_band = FloatField("pH band")

    gh = IntegerField("gh")
    gh_band = IntegerField("gh band")

    kh = IntegerField("kh")

    no2 = IntegerField("no2")
    no3 = IntegerField("no3")

    cl = FloatField("cL")

    co2 = SelectField(
        "CO²", choices=[("blue", "Bleu"), ("green", "Green"), ("yellow", "Yellow")]
    )


@app.route("/add", methods=["GET", "POST"])
def register():
    form = StatsForm(request.form)
    if request.method == "POST" and form.validate():
        json.dump(form.data, open("data.json", "w"), indent=True, sort_keys=True)
        flash("Measurements successfully added")
        return render_template("add.html", form=StatsForm())

    return render_template("add.html", form=form)


@app.route("/edit", methods=["GET"])
def edit_get():
    form = StatsForm()
    if os.path.exists("data.json"):
        for key, value in json.load(open("data.json", "r")).items():
            getattr(form, key).data = value

    return render_template("add.html", form=form)


@app.route("/edit", methods=["POST"])
def edit_post():
    form = StatsForm(request.form)

    if form.validate():
        print(form)
        json.dump(form.data, open("data.json", "w"), indent=True, sort_keys=True)
        flash("Measurements successfully edited")
        return render_template("add.html", form=form)

    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
