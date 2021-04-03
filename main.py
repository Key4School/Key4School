from flask import Flask, render_template

# Création de l'application
app = Flask(__name__)


# Quand on arrive sur le site, on affiche la page "ma_page.html"
@app.route('/')
def accueil():
    return render_template("ma_page.html")


@app.route('/accueil')
def accueil2():
    return render_template("ma_page.html")


#testtesttest





# Lancement de l'application, à l'adresse 127.0.0.0 et sur le port 3000
app.run(host="127.0.0.1", port=3000)
