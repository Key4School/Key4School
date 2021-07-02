from flask import Flask, render_template, request, redirect, session, url_for, abort, escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from flask.json import jsonify
from bson.objectid import ObjectId
from threading import Timer
from functools import partial
from db_poo import *

clientsNotif = {}

listeModeration = []
with open("list_ban_words.txt", "r", encoding='cp1252') as fichierBanWords:
    listeModeration = fichierBanWords.read().splitlines()

def automoderation(stringModerer: str) -> str:
    nbMaj = sum(1 for c in stringModerer if c.isupper())
    lenStr = len(stringModerer)
    if lenStr != 0 and nbMaj/lenStr >= 60/100 :
        stringModerer=stringModerer.lower()
    stringModerer2 =stringModerer
    for key in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']:
            stringModerer2 = stringModerer2.replace(key," ")
            # print (stringModerer2)
    for content in listeModeration:
        strReplace = ""
        for i in range(len(content)):
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

def sendNotif(type, id_groupe, id_msg, destinataires):
    global notifications
    global utilisateurs

    if type == 'demande':
        destinataires += [user._id for user in utilisateurs.values() if id_groupe in user.savedDemands]

    if ObjectId(session['id']) in destinataires:
        destinataires.remove(ObjectId(session['id']))

    destinataires = list(set(destinataires))

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
                emit('newNotif', {'html': html, 'sound': str(user['notifs']['sound'])}, to=str(user['_id']))
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



class Interval(object):

    def __init__(self, interval, function, args=[], kwargs={}):
        """
        Runs the function at a specified interval with given arguments.
        """
        self.interval = interval
        self.function = partial(function, *args, **kwargs)
        self.running  = False
        self._timer   = None

    def __call__(self):
        """
        Handler function for calling the partial and continuting.
        """
        self.running = False  # mark not running
        self.start()          # reset the timer for the next go
        self.function()       # call the partial function

    def start(self):
        """
        Starts the interval and lets it run.
        """
        if self.running:
            # Don't start if we're running!
            return

        # Create the timer object, start and set state.
        self._timer = Timer(self.interval, self)
        self._timer.start()
        self.running = True

    def stop(self):
        """
        Cancel the interval (no more function calls).
        """
        if self._timer:
            self._timer.cancel()
        self.running = False
        self._timer  = None
