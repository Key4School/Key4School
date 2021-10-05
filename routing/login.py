from flask import Flask, render_template, request, redirect, session, url_for, abort, escape

def signIn():
    if request.method == 'POST':
        request.form['prenom']
        request.form['nom']
        request.form['pseudo']
        request.form['email']
        hash = hashing.hash_value(request.form['mdp'], salt=cle)
        print(hash)
        return render_template('inscription1.html')
    else:
        return render_template('inscription0.html')
