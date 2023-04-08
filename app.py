#1. visualizzare le infomrazioni riguardanti un film. L'utente inserisce il titolo del film e il server risponde con tutte le informazioni presenti nel file csv. Se il film non è presente, visualizzare un opportuno messaggio di errore
#2. visualizzare i film di un certo genere inserito dall'utente
#3. visualizzare i film di un certo genere scelto dall'utente tra quelli presenti in un menù a tendina
#4. visualizzare i film di un certo genere scelto dall'utente tra quelli presenti in una lista di radiobutton
#5. visualizzare i film di tutti i generi  scelti dall'utente tra quelli presenti in una lista di checkbox
#6. visualizzare i titoli dei film di cui non si conosce il budget
#7. visualizzare un grafico con il numero di film per ogni genere. Ordinare in ordine decrescente a partire dal genere con più film

from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/wtitze/3E/main/2010.csv", delimiter = ";")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/film")
def film():
    return render_template("film.html", elenco = list(df["Title"]))

@app.route("/genere")
def genere():
    return render_template("genere.html", elenco = list(df["Genres"]))

@app.route("/genereTendina")
def tendina():
    return render_template("tendina.html", elenco = list(df["Genres"]))

@app.route("/genereRadio")
def radio():
    return render_template("radio.html", elenco = list(df["Genres"]))

@app.route("/genereCheck")
def check():
    return render_template("check.html", elenco = list(df["Genres"]))

@app.route("/budget")
def budget():
    nulla = df[df["Budget"].isnull()]
    n = nulla.to_html()
    return render_template("budget.html", tabella = n)

@app.route("/grafico")
def grafico():
    dfConteggio = df.groupby("Genres").count()[["Title"]].sort_values(by="Title", ascending = False).reset_index()
    import matplotlib.pyplot as plt
    import plotly.graph_objs as go
    import os
    x = dfConteggio["Title"]
    y = dfConteggio["Genres"]
    plt.bar(y, x)
    plt.xticks(rotation = (80))
    plt.title('Film per genere')
    plt.xlabel('Generi')
    plt.ylabel('Nfilm')
    dir = "static/images"
    file_name = "graf.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path)   #trasforma un grafico in un'immagine
    return render_template("grafico.html")


@app.route("/datiFilm", methods = ["GET"])
def datiFilm():
    nome = request.args.get("film")
    dfFilm = df[df["Title"].str.contains(nome)]
    h = dfFilm.to_html()
    return render_template("datiFilm.html", tabella = h)

@app.route("/datiGenere", methods = ["GET"])
def datiGenere():
    gen = request.args.get("genere")
    dfGenere = df[df["Genres"].str.contains(gen)]
    hh = dfGenere.to_html()
    return render_template("datiGenere.html", tabella = hh)

@app.route("/datiGenereTendina", methods = ["GET"])
def datiGenereTendina():
    genT = request.args.get("genereTendina")
    dfGenereTendina = df[df["Genres"] == genT]
    hhh = dfGenereTendina.to_html()
    return render_template("datiGenereTendina.html", tabella = hhh)

@app.route("/datiGenereRadio", methods = ["GET"])
def datiGenereRadio():
    genR = request.args.get("genereRadio")
    dfGenereRadio = df[df["Genres"] == genR]
    hhhh = dfGenereRadio.to_html()
    return render_template("datiGenereRadio.html", tabella = hhhh)

@app.route("/datiGenereCheck", methods = ["GET"])
def datiGenereCheck():
    genC = request.args.getlist("gener")
    dfGenereCheck = df[df["Genres"].isin(genC)]
    hhhhh = dfGenereCheck.to_html()
    return render_template("datiGenereCheck.html", tabella = hhhhh)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)