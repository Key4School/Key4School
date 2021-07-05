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


def afficheNotif(userId, notifId):
    global utilisateurs
    global notifications
    if userId in utilisateurs and notifId in notifications:
        return render_template("mail.html", user=utilisateurs[userId].toDict(), notif=notifications[notifId].toDict())
    else:
        return redirect(url_for('login'))


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
        self.start()          # reset the timer for the next go
        self.function()       # call the partial function
        self.running = False  # mark not running

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
