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
    gene = list(set(df[~df["Genres"].str.contains("\|")]["Genres"]))  #~: sta per not
    gene.sort()
    return render_template("genere.html", elenco = gene)

@app.route("/genereTendina")
def tendina():
    gene = list(set(df[~df["Genres"].str.contains("\|")]["Genres"]))
    gene.sort()
    return render_template("tendina.html", elenco = gene)

@app.route("/genereRadio")
def radio():
    gene = list(set(df[~df["Genres"].str.contains("\|")]["Genres"]))
    gene.sort()
    return render_template("radio.html", elenco = gene)

@app.route("/genereCheck")
def check():
    gene = list(set(df[~df["Genres"].str.contains("\|")]["Genres"]))
    gene.sort()
    return render_template("check.html", elenco = gene)

@app.route("/budget")
def budget():
    nulla = df[df["Budget"].isnull()]
    n = nulla.to_html()
    return render_template("budget.html", tabella = n)

@app.route("/grafico")
def grafico():
    dfConteggio = df.groupby("Language").count()[["Title"]].sort_values(by="Title", ascending = False).reset_index()
    import matplotlib.pyplot as plt
    import plotly.graph_objs as go
    import os
    x = dfConteggio["Title"]
    y = dfConteggio["Language"]
    plt.bar(y, x, label = "NumeroFilm")  #prima stringhe, poi dati
    plt.xticks(rotation = (80))
    plt.title('Film per lingua')
    plt.xlabel('Lingue')
    plt.ylabel('Nfilm')
    plt.subplots_adjust(bottom=0.25)  #non taglia i nomi sull'asse x
    plt.legend()
    dir = "static/images"
    file_name = "graf.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)   #trasforma un grafico in un'immagine; dpi serve per cambiare le dimensione dell'immagine
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
    dfGenereTendina = df[df["Genres"].str.contains(genT)]
    hhh = dfGenereTendina.to_html()
    return render_template("datiGenereTendina.html", tabella = hhh)

@app.route("/datiGenereRadio", methods = ["GET"])
def datiGenereRadio():
    genR = request.args.get("genereRadio")
    dfGenereRadio = df[df["Genres"].str.contains(genR)]
    hhhh = dfGenereRadio.to_html()
    return render_template("datiGenereRadio.html", tabella = hhhh)

@app.route("/datiGenereCheck", methods = ["GET"])
def datiGenereCheck():
    genC = request.args.getlist("gener")
    dfGenereCheck = pd.DataFrame()
    for elemento in genC:
        ris = df[df["Genres"].str.contains(elemento)]
        dfGenereCheck = pd.concat([dfGenereCheck, ris])
    hhhhh = dfGenereCheck.to_html()
    return render_template("datiGenereCheck.html", tabella = hhhhh)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)