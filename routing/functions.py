from flask import Flask, current_app as app, render_template, request, redirect, session, url_for, abort, escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from datetime import *
from flask.json import jsonify
from threading import Timer
from functools import partial
from db_poo import *

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

@db_session
def afficheNotif(userId, notifId):
    if not is_valid_uuid(userId) or not is_valid_uuid(notifId):
        return redirect(url_for('login'))

    user = User.get(filter="cls.id == userId", limit=1)
    notif = Notification.get(filter="cls.id == notifId", limit=1)
    if user and notif:
        return render_template("mail.html", user=user, notif=notif)
    else:
        return redirect(url_for('login'))
