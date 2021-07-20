import psycopg2
from psycopg2 import OperationalError
import psycopg2.extras
from db_poo import *
from datetime import *
from bson.objectid import ObjectId
from flask import session, escape, render_template, Flask
from flask_pymongo import PyMongo, ObjectId
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from matieresDict import translations, translateProf
from uuid import uuid4

def create_connection(db_name, db_user, db_password):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection("nomdeladb", "nomdel'utilisateur","motdepassedeladb")
app = Flask(__name__)

try :
    DB = DB_Manager.createCluster(app, "mongodb+srv://CTLadmin:ctlADMIN@ctlbdd.etzx9.mongodb.net/CTLBDD?retryWrites=true&w=majority")
    print("Connection to PyMongo BD successful")
except :
    print("An error occurred")




with app.test_request_context(
        '/make_report/2017', data={'format': 'short'}):
    for a in utilisateurs:
        e = utilisateurs[a].toDict()
        _id = uuid4()
        nom = e['nom']
        prenom = e['prenom']
        pseudo = e['pseudo']
        nomImg = e.get('nomImg')
        imgProfile = e.get('imgProfile', '')
        dateInscription = e['dateInscription']
        birth_date = e.get('birth_date', None)
        classe = e.get('classe', '')
        lycee = e['lycee']
        spes = e.get('spes', [])
        langues = e.get('langues', [])
        options = e.get('options', [])
        matiere = e.get('matiere', '') # pour les profs
        matiere_autre = e.get('matiere_autre', []) # pour les profs
        couleur = e['couleur']
        typeEleve = e['type']
        elementPublic = e['elementPublic']
        elementPrive = e['elementPrive']
        caractere = e.get('caractere')
        email = e.get('email', '')
        interets = e.get('interets', '')
        telephone = e.get('telephone', '')
        notifs = e.get('notifs')
        sign = e.get('sign', [])
        Sanctions = e.get('Sanction', [])
        SanctionEnCour = e['SanctionEnCour']
        SanctionDuree = e.get('SanctionDuree', '')
        xp = max(e['xp'], 0)
        xpModeration = max(e.get('xpModeration', 0), 0)
        motif = e.get('motif', [])
        admin = e.get('admin', False)
        savedDemands = e.get('savedDemands', [ObjectId('60d8b3a48a701d9f2cbebf3c')])

        connection.autocommit = True
        cursor = connection.cursor()
        psycopg2.extras.register_uuid()

        try:
            print(_id,nom,prenom,pseudo,nomImg,dateInscription,birth_date,classe,lycee,spes,langues,options,matiere,matiere_autre,couleur,typeEleve,elementPublic,elementPrive,caractere,email,interets,telephone,notifs,Sanctions,SanctionEnCour,SanctionDuree,xp,xpModeration,admin)
            cursor.execute("INSERT INTO users (id, name, firstname, pseudo, image_name, inscription_date, birth_date, grade, school, spes, languages, options, matter, other_matter, color, type, public, private, mood, email, interest, phone, sanction, current_sanction, sanction_duration, xp, xp_moderation, admin) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)", (_id,nom,prenom,pseudo,nomImg,dateInscription,birth_date,classe,lycee,spes,langues,options,matiere,matiere_autre,couleur,typeEleve,elementPublic,elementPrive,caractere,email,interets,telephone,Sanctions,SanctionEnCour,SanctionDuree,xp,xpModeration,admin))
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")


if connection:
    connection.close()
    print("PostgreSQL connection is closed")
