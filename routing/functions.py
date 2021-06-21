from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from db_poo import *

clientsNotif = {}

def recupLevel():
    global utilisateurs

    user = utilisateurs[session['id']].toDict()
    xpgens = user['xp']
    niv = int(0.473*xpgens**0.615)
    xplvl = int((0.473*xpgens**0.615-niv)*100)

    return niv, xplvl, xpgens

def addXP(userID: str, amount: int) -> None:
    """
        +10 pour une demande d’aide
        +15 pour une réponse
        +2 pour chaque like reçu
    """

    user = utilisateurs[userID]
    user.xp += amount

    utilisateurs[userID].update()

    return

def addXpModeration(userID: str, amount: int) -> None:
    global utilisateurs

    user = utilisateurs[userID]
    user.xpModeration += amount

    utilisateurs[userID].update()

    return

listeModeration = []
with open("list_ban_words.txt", "r", encoding='cp1252') as fichierBanWords:
    listeModeration = fichierBanWords.read().splitlines()

def automoderation(stringModerer: str) -> str:
    stringModerer2 =stringModerer
    for key in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']:
            stringModerer2 = stringModerer2.replace(key," ")
            print (stringModerer2)
    for content in listeModeration:
        strReplace = ""
        for i in range (len(content)):
            strReplace += "*"
        if len(content) < 6:
            if stringModerer2[0:len(content)+1] == content+" ":
                stringModerer= stringModerer.replace(content, " "+strReplace+" ")
            if stringModerer2[-len(content)+1:] == " "+content:
                stringModerer= stringModerer.replace(content, " "+strReplace+" ")
            if stringModerer2 == content:
                stringModerer= stringModerer.replace(content, " "+strReplace+" ")
            content= " "+content+" "
        if  content in stringModerer2:
            stringModerer= stringModerer.replace(content, " "+strReplace+" ")

    return stringModerer

# clientsNotif = {}

def sendNotif(type, id_groupe, id_msg, destinataires):
    global notifications

    if ObjectId(session['id']) in destinataires:
        destinataires.remove(ObjectId(session['id']))

    if len(destinataires) > 0:
        _id = ObjectId()
        notifications[str(_id)] = Notification({"_id": _id, "type": type, "id_groupe": id_groupe, "id_msg": id_msg,
                                        "date": datetime.now(), "destinataires": destinataires})
        notifications[str(_id)].insert()
        notification = notifications[str(_id)].toDict()

        serveur = 'smtp.gmail.com'
        port = '465'
        From = 'key4school@gmail.com'
        password = 'CtlLemeilleurGroupe'
        codage = 'utf-8'

        html = render_template("notification.html", notif=notification, similar=0)

        for user in notification['userDest']:
            if str(user['_id']) in clientsNotif:
                emit('newNotif', html, to=str(user['_id']))
            # elif user['email'] != "":
            #     # si l'user a autorisé les notifs par mail
            #     if (type == 'msg' and user['notifs']['messages']) or (type == 'demande' and user['notifs']['demandes']):
            #         # si un mail n'a pas déja été envoyé pour ce groupe
            #         if (type == 'msg' and len([notif for notif in notifications.values() if notif.id_groupe == id_groupe and notif.type == 'msg' and user in notif.destinataires]) == 0 ) or type == 'demande':
            #             To = user['email']
            #             msg = MIMEMultipart()
            #             msg['From'] = From
            #             msg['To'] = To
            #             msg['Subject'] = sujet
            #             msg['Charset'] = codage
            #
            #             # attache message texte
            #             msg.attach(MIMEText('message'.encode(codage),
            #                                 'plain', _charset=codage))
            #             # attache message HTML
            #             msg.attach(MIMEText('html'.encode(codage),
            #                                 'html', _charset=codage))
            #
            #             mailserver = smtplib.SMTP_SSL(serveur, port)
            #             mailserver.login(From, password)
            #             mailserver.sendmail(From, To, msg.as_string())
            #             mailserver.quit