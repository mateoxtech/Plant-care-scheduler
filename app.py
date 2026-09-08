from flask import Flask, request, make_response, jsonify, render_template
from pony import orm
from datetime import datetime
from collections import defaultdict
from itertools import groupby

DB = orm.Database()
app = Flask(__name__)


#   Use case model

class Biljka(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv = orm.Required(str)
    vrsta = orm.Required(str)
    opis = orm.Required(str)
    datum_zalijevanja = orm.Required(datetime)
    interval_zalijevanja = orm.Required(int)  # svakih X dana

DB.bind(provider="sqlite", filename="biljke.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


def formatiraj_datum(d):
    return d.strftime('%d-%m-%Y') if d else None


#   CRUD - CREATE

def add_biljka(json_request):
    try:
        naziv = json_request["naziv"]
        vrsta = json_request["vrsta"]
        opis = json_request["opis"]
        interval = int(json_request["interval_zalijevanja"])

        try:
            datum = datetime.fromisoformat(json_request["datum_zalijevanja"])
        except:
            datum = datetime.now()

        with orm.db_session:
            Biljka(
                naziv=naziv,
                vrsta=vrsta,
                opis=opis,
                datum_zalijevanja=datum,
                interval_zalijevanja=interval
            )
        return {"response": "Success"}

    except Exception as e:
        return {"response": "Fail", "error": str(e)}


#   CRUD - READ

def get_biljke():
    try:
        with orm.db_session:
            q = Biljka.select()  # BEZ [:]
            data = []
            for b in q:
                d = b.to_dict()
                d["datum_zalijevanja"] = formatiraj_datum(d["datum_zalijevanja"])
                data.append(d)
        return {"response": "Success", "data": data}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}



#   READ

def get_biljka_by_id(biljka_id):
    try:
        with orm.db_session:
            b = Biljka.get(id=biljka_id)
            if not b:
                return {"response": "Fail", "error": "Biljka ne postoji"}

            d = b.to_dict()
            d["datum_zalijevanja"] = formatiraj_datum(d["datum_zalijevanja"])
        return {"response": "Success", "data": d}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}



#   CRUD - UPDATE

def patch_biljka(biljka_id, json_request):
    try:
        with orm.db_session:
            b = Biljka[biljka_id]

            if "naziv" in json_request:
                b.naziv = json_request["naziv"]
            if "vrsta" in json_request:
                b.vrsta = json_request["vrsta"]
            if "opis" in json_request:
                b.opis = json_request["opis"]
            if "interval_zalijevanja" in json_request:
                b.interval_zalijevanja = int(json_request["interval_zalijevanja"])
            if "datum_zalijevanja" in json_request:
                b.datum_zalijevanja = datetime.strptime(json_request["datum_zalijevanja"], "%d-%m-%Y")

        return {"response": "Success"}

    except Exception as e:
        return {"response": "Fail", "error": str(e)}


#   CRUD - DELETE

def delete_biljka(biljka_id):
    try:
        with orm.db_session:
            Biljka[biljka_id].delete()
        return {"response": "Success"}
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


#   STATISTIKA zalijevanja

def get_biljke_by_month():
    try:
        with orm.db_session:
            q = orm.select(b for b in Biljka)[:]
            stats = defaultdict(int)

            for b in q:
                month = b.datum_zalijevanja.month
                stats[month] += 1

        return {"response": "Success", "data": dict(stats)}

    except Exception as e:
        return {"response": "Fail", "error": str(e)}


#   FILTER po vrsti biljke

@orm.db_session
def get_biljke_by_vrsta():
    try:
        biljke = orm.select(b for b in Biljka).order_by(Biljka.vrsta)
        grouped = groupby(biljke, lambda b: b.vrsta)

        result = [{"vrsta": vrsta, "broj_biljaka": len(list(grupa))} for vrsta, grupa in grouped]

        return {"response": "Success", "data": {"vrste": result}}

    except Exception as e:
        return {"response": "Fail", "error": str(e)}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dodaj/biljku", methods=["GET", "POST"])
def dodaj_biljku():
    if request.method == "POST":
        json_request = {k: (v if v != "" else None) for k, v in request.form.items()}
        response = add_biljka(json_request)
        if response["response"] == "Success":
            return render_template("dodaj.html")
        return jsonify(response), 400
    return render_template("dodaj.html")

@app.route("/vrati/biljke", methods=["GET"])
def vrati_biljke():
    if request.args and "id" in request.args:
        biljka_id = int(request.args.get("id"))
        response = get_biljka_by_id(biljka_id)
        if response["response"] == "Success":
            return render_template("vrati.html", data=[response["data"]])
        return jsonify(response), 400

    response = get_biljke()
    if response["response"] == "Success":
        return render_template("vrati.html", data=response["data"])
    return jsonify(response), 400



@app.route("/uredi/<int:biljka_id>", methods=["GET"])
def uredi_biljku_html(biljka_id):
    response = get_biljka_by_id(biljka_id)
    if response["response"] == "Success":
        return make_response(render_template("uredi.html", data=response["data"]), 200)
    return make_response(jsonify(response), 400)




@app.route("/biljke/vizualizacija")
def vizualizacija():
    chart_data = get_biljke_by_month()

    print("CHART DATA =", chart_data)

    y_axis = list(chart_data.get("data", {}).values())
    x_axis = list(chart_data.get("data", {}).keys())

    print("X AXIS =", x_axis)
    print("Y AXIS =", y_axis)

    return render_template(
        "vizualizacija.html",
        y_axis=y_axis,
        x_axis=x_axis
    )


@app.route("/biljke/vrste")
def biljke_po_vrstama():
    data = get_biljke_by_vrsta()
    vrste = list(data.get("data", {}).values())
    return render_template("vizualizacija_vrste.html", vrste=vrste)

@app.route("/biljka/<int:biljka_id>", methods=["DELETE"])
def obrisi_biljku(biljka_id):
    response = delete_biljka(biljka_id)
    return jsonify(response), (200 if response["response"] == "Success" else 400)

@app.route("/biljka/<int:biljka_id>", methods=["PATCH"])
def izmjeni_biljku(biljka_id):
    json_request = request.json
    response = patch_biljka(biljka_id, json_request)
    return jsonify(response), (200 if response["response"] == "Success" else 400)


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", debug=True)