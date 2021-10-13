from datetime import *
from bson.objectid import ObjectId
from flask import session, escape, render_template
from flask_pymongo import PyMongo, ObjectId
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from matieresDict import translations, translateProf
from datetime import *

utilisateurs = {}
demandes_aide = {}
messages = {}
groupes = {}
notifications = {}
DB = None


class DB_Manager:
    def __init__(self, app, cluster_url):
        self.cluster = PyMongo(app, cluster_url, tls=True, tlsAllowInvalidCertificates=True)
        self.db_utilisateurs = self.cluster.db.utilisateurs
        self.db_demande_aide = self.cluster.db.demande_aide
        self.db_messages = self.cluster.db.messages
        self.db_groupes = self.cluster.db.groupes
        self.db_files = self.cluster.db.fs.files
        self.db_chunks = self.cluster.db.fs.chunks
        self.db_notif = self.cluster.db.notifications

    @staticmethod
    def createCluster(app, cluster_url):
        global DB
        global utilisateurs
        global demandes_aide
        global messages
        global groupes
        global notifications

        # create DB
        DB = DB_Manager(app, cluster_url)

        # save DB

        all_utilisateurs = DB.db_utilisateurs.find()
        for u in all_utilisateurs:
            utilisateurs[str(u['_id'])] = Utilisateur(u)

        all_demandes_aide = DB.db_demande_aide.find()
        for d in all_demandes_aide:
            demandes_aide[str(d['_id'])] = Demande(d)

        all_groupes = DB.db_groupes.find()
        for g in all_groupes:
            groupes[str(g['_id'])] = Groupe(g)

        all_messages = DB.db_messages.find()
        for m in all_messages:
            messages[str(m['_id'])] = Message(m)

        all_notifications = DB.db_notif.find()
        for n in all_notifications:
            notifications[str(n['_id'])] = Notification(n)

        # return DB
        return DB

    def update(self, db_table, data):
        db_table.update_one(
            {'_id': data['_id']},
            {'$set': data}
        )

    def insert(self, db_table, data):
        db_table.insert_one(data)

    def delete(self, db_table, _id):
        db_table.delete_one({'_id': _id})


class Actions:
    def insert(self):
        DB.insert(self.db_table, self.toDB())

    def update(self):
        DB.update(self.db_table, self.toDB())

    def delete(self):
        DB.delete(self.db_table, self._id)


class Translate_matiere_spes_options_lv:
    def translate_matiere_spes_options_lv(self, toTranslate):
        translated = ''
        if type(toTranslate) == list:
            for a in toTranslate:
                if translated != '' and a != 'none':
                    translated += ' / '
                translated += translations[a]
        elif toTranslate != '':
            translated = translations[toTranslate]

        return translated


class Utilisateur(Translate_matiere_spes_options_lv, Actions):
    def __init__(self, params: dict):
        self._id = params['_id']
        self.nom = params['nom']
        self.prenom = params['prenom']
        self.pseudo = params['pseudo']
        self.email = params['email']
        self.mdp = params['mdp']
        self.dateInscription = params.get('dateInscription', datetime.now())
        self.etapeInscription = params.get('etapeInscription', 1)

        self.birth_date = params.get('birth_date')
        self.classe = params.get('classe')
        self.telephone = params.get('telephone', '')
        self.lycee = params.get('lycee')
        self.lyceeId = params.get('lyceeId')
        self.langues = params.get('langues', [])

        self.options = params.get('options', [])
        self.spes = params.get('spes', [])
        self.matiere = params.get('matiere', '') # pour les profs
        self.matiere_autre = params.get('matiere_autre', []) # pour les profs

        self.nomImg = params.get('nomImg', '')
        self.imgProfile = params.get('imgProfile', '')

        self.couleur = params.get('couleur', ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'])
        self.theme = params.get('theme', 'system')

        self.elementPublic = params.get('elementPublic', [])
        self.elementPrive = params.get('elementPrive', ['email', 'telephone', 'interets', 'birth_date'])

        self.interets = params.get('interets', '')

        self.notifs = params.get(
            'notifs', {'demandes': True, 'messages': True, 'sound': True})

        self.sign = params.get('sign', [])
        self.Sanctions = params.get('Sanction', [])
        self.SanctionEnCour = params.get('SanctionEnCour', '')
        self.SanctionDuree = params.get('SanctionDuree', '')

        self.xp = max(params.get('xp', 0), 0)
        self.xpModeration = max(params.get('xpModeration', 0), 0)
        self.motif = params.get('motif', [])

        self.admin = params.get('admin', False)

        self.savedDemands = params.get('savedDemands', [])

        self.db_table = DB.db_utilisateurs

    def signIn1(self, phone, birthday, school, classe, langues):
        self.telephone = phone
        self.birth_date = birthday
        self.lycee = school['nomVille']
        self.lyceeId = school['id']
        self.classe = classe
        self.langues = langues

        self.etapeInscription = 2
        self.update()

    def signIn2(self, spes, options):
        self.spes = spes
        self.options = options

        self.etapeInscription = None
        self.update()

    def recupLevel(self):
        niv = int(0.473*self.xp**0.615)
        xplvl = int((0.473*self.xp**0.615-niv)*100)

        return niv, xplvl, self.xp

    def addXP(self, amount: int) -> None:
        """
            +10 pour une demande d’aide
            +15 pour une réponse
            +2 pour chaque like reçu
        """
        self.xp += amount
        self.xp = max(self.xp, 0)
        self.update()
        return

    def addXpModeration(self, amount: int) -> None:
        self.xpModeration += amount
        self.xpModeration = max(self.xpModeration, 0)
        self.update()
        return

    def toDict(self):
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'nom': self.nom,
            'prenom': self.prenom,
            'pseudo': self.pseudo,
            'mdp': self.mdp,
            'nomImg': self.nomImg,
            'imgProfile': self.imgProfile,
            'dateInscription': self.dateInscription,
            'etapeInscription': self.etapeInscription,
            'birth_date': self.birth_date,
            'classe': self.classe,
            'lycee': self.lycee,
            'lyceeId': self.lyceeId,
            'spes': self.spes,
            'spes-str': self.translate_matiere_spes_options_lv(self.spes),
            'langues': self.langues,
            'langues-str': self.translate_matiere_spes_options_lv(self.langues),
            'options': self.options,
            'options-str': self.translate_matiere_spes_options_lv(self.options),
            'matiere': self.matiere, # pour les profs
            'matiere-str': self.translate_matiere_spes_options_lv(self.matiere),
            'matiere_autre': self.matiere_autre, # pour les profs
            'matiere_autre-str': self.translate_matiere_spes_options_lv(self.matiere_autre),
            'matieres': self.getUserSubjects(),
            'couleur': self.couleur,
            'theme': self.theme,
            'elementPublic': self.elementPublic,
            'elementPrive': self.elementPrive,
            'email': self.email,
            'interets': self.interets,
            'telephone': self.telephone,
            'notifs': self.notifs,
            'sign': self.sign,
            'Sanctions': self.Sanctions,
            'SanctionEnCour': self.SanctionEnCour,
            'SanctionDuree': self.SanctionDuree,
            'xp': self.xp,
            'xpModeration': self.xpModeration,
            'motif': self.motif,
            'admin': self.admin,
            'a_sign': self.aSign(),
            'savedDemands': self.savedDemands
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'nom': self.nom,
            'prenom': self.prenom,
            'pseudo': self.pseudo,
            'mdp': self.mdp,
            'nomImg': self.nomImg,
            'imgProfile': self.imgProfile,
            'dateInscription': self.dateInscription,
            'etapeInscription': self.etapeInscription,
            'birth_date': self.birth_date,
            'classe': self.classe,
            'lycee': self.lycee,
            'lyceeId': self.lyceeId,
            'spes': self.spes,
            'langues': self.langues,
            'options': self.options,
            'matiere': self.matiere, # pour les profs
            'matiere_autre': self.matiere_autre, # pour les profs
            'couleur': self.couleur,
            'theme': self.theme,
            'elementPublic': self.elementPublic,
            'elementPrive': self.elementPrive,
            'email': self.email,
            'interets': self.interets,
            'telephone': self.telephone,
            'notifs': self.notifs,
            'sign': self.sign,
            'Sanction': self.Sanctions,
            'SanctionEnCour': self.SanctionEnCour,
            'SanctionDuree': self.SanctionDuree,
            'xp': self.xp,
            'xpModeration': self.xpModeration,
            'motif': self.motif,
            'admin': self.admin,
            'savedDemands': self.savedDemands
        }

    def getUserSubjects(self):
        # A REFAIRE
        if self.etapeInscription:
            return []
        if 'ELEVE' == "ELEVE":
            subjects = ['hg', 'emc', 'eps']
            # Tronc commun
            if self.classe[0] == '2' or self.classe[0] == '1':
                subjects.append('fr')
            if self.classe[0] == '2':
                subjects.append('maths')
                subjects.append('pc')
                subjects.append('svt')
                subjects.append('snt')
                subjects.append('ses')
            if self.classe[0] == 'T':
                subjects.append('philo')
            # Langues
            if 'lv1-ang' in self.langues or 'lv1-ang-euro' in self.langues or 'lv2-ang' in self.langues or 'opt-lv3-ang' in self.options:
                subjects.append('ang')
            if 'lv1-esp' in self.langues or 'lv1-esp-euro' in self.langues or 'lv2-esp' in self.langues or 'opt-lv3-esp' in self.options:
                subjects.append('esp')
            if 'lv1-all' in self.langues or 'lv1-all-euro' in self.langues or 'lv2-all' in self.langues or 'opt-lv3-all' in self.options:
                subjects.append('all')
            if 'lv1-it' in self.langues or 'lv1-it-euro' in self.langues or 'lv2-it' in self.langues or 'opt-lv3-it' in self.options:
                subjects.append('it')
            if 'lv1-chi' in self.langues or 'lv2-chi' in self.langues or 'opt-lv3-chi' in self.options:
                subjects.append('chi')
            if 'lv1-ru' in self.langues or 'lv2-ru' in self.langues or 'opt-lv3-ru' in self.options:
                subjects.append('ru')
            if 'lv1-por' in self.langues or 'lv2-por' in self.langues or 'opt-lv3-por' in self.options:
                subjects.append('por')
            if 'lv1-ara' in self.langues or 'lv2-ara' in self.langues or 'opt-lv3-ara' in self.options:
                subjects.append('ara')
            # AJOUTER LES NOUVELLES LANGUES
            # Spés + options
            subjects += self.spes
            subjects += self.options
        else:
            subjects = []
            if self.matiere != '':
                if self.matiere in translateProf:
                    subjects += translateProf[self.matiere]
                else:
                    subjects += [self.matiere]
                for subject in self.matiere_autre:
                    if subject in translateProf:
                        subjects += translateProf[subject]
                    else:
                        subjects += [subject]
            elif len(self.matiere_autre) > 0:
                for subject in self.matiere_autre:
                    if subject in translateProf:
                        subjects += translateProf[subject]
                    else:
                        subjects += [subject]
            else:
                subjects = ['ang', 'esp', 'all', 'it', 'chi', 'ru', 'por', 'ara']
                subjects += [key for key, value in translations.items() if not 'lv'in key]
        return subjects

    def aSign(self):
        if ObjectId(session.get('id')) in self.sign:
            return True
        else:
            return False

    def __str__(self):
        return str(self.toDict())


class Demande(Translate_matiere_spes_options_lv, Actions):
    def __init__(self, params: dict):
        self._id = params['_id']
        self.id_utilisateur = params['id-utilisateur']
        self.titre = params['titre']
        self.contenu = params['contenu']
        self.date_envoi = params['date-envoi']
        self.matiere = params['matière']
        self.reponses_associees = {}
        for (idRep, rep) in params['réponses associées'].items():
            self.reponses_associees[idRep] = Reponse(rep)
        self.likes = params['likes']
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])
        self.resolu = params['resolu']
        self.fileType = params['fileType']

        self.db_table = DB.db_demande_aide

    def diffTemps(self):
        diff_temps = int((datetime.now() - self.date_envoi).total_seconds())
        return diff_temps

    def convertTime(self):
        tempsStr = ''
        diffTemps = self.diffTemps()
        # puis on se fait chier à trouver le délai entre le poste et aujourd'hui
        if diffTemps // (60 * 60 * 24 * 7):  # semaines
            tempsStr += '{}sem '.format(diffTemps // (60 * 60 * 24 * 7))
            if (diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24):  # jours
                tempsStr += '{}j '.format((diffTemps %
                                           (60 * 60 * 24 * 7)) // (60 * 60 * 24))
        elif diffTemps // (60 * 60 * 24):  # jours
            tempsStr += '{}j '.format(diffTemps // (60 * 60 * 24))
            if (diffTemps % (60 * 60 * 24)) // (60 * 60):  # heures
                tempsStr += '{}h '.format((diffTemps %
                                           (60 * 60 * 24)) // (60 * 60))
        elif diffTemps // (60 * 60):  # heures
            tempsStr += '{}h '.format(diffTemps // (60 * 60))
            if (diffTemps % (60 * 60)) // 60:  # minutes
                tempsStr += '{}min '.format(diffTemps % (60 * 60) // 60)
        else:
            tempsStr = '{}min'.format(diffTemps // 60)

        return tempsStr

    def aLike(self):
        if session['id'] in self.likes:
            return True
        else:
            return False

    def aSign(self):
        if ObjectId(session['id']) in self.sign:
            return True
        else:
            return False

    def aSave(self):
        user = utilisateurs[session['id']]

        if self._id in user.savedDemands:
            return True
        else:
            return False

    def convert_links(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(re.sub('^http(s?)://', '', w), w),
                w)
            contenu += ' '

        return contenu

    def toDict(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'idMsg': self._id,
            'idAuteur': self.id_utilisateur,
            'titre': self.titre,
            'contenu': self.convert_links(),
            'date-envoi': self.date_envoi,
            'temps': self.convertTime(),
            'tag-matière': self.matiere,
            'matière': self.translate_matiere_spes_options_lv([self.matiere]),
            'likes': self.likes,
            'nb-likes': len(self.likes),
            'réponses associées': sorted([r.toDict() for r in self.reponses_associees.values()], key=lambda r: r['nb-likes'], reverse=True),
            'reponsesDict': {idRep: rep.toDict() for (idRep, rep) in self.reponses_associees.items()},
            'reponsesDict2': {idRep: rep for (idRep, rep) in self.reponses_associees.items()},
            'reponsesObjects': self.reponses_associees,
            'a_like': self.aLike(),
            'a_sign': self.aSign(),
            'a_save': self.aSave(),
            'sign': self.sign,
            'motif': self.motif,
            'resolu': self.resolu,
            'fileType': self.fileType,
            # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
            'user': utilisateurs.get(str(self.id_utilisateur)).toDict()
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'id-utilisateur': self.id_utilisateur,
            'titre': self.titre,
            'contenu': self.contenu,
            'date-envoi': self.date_envoi,
            'matière': self.matiere,
            'réponses associées': {idRep: rep.toDB() for (idRep, rep) in self.reponses_associees.items()},
            'likes': self.likes,
            'sign': self.sign,
            'motif': self.motif,
            'resolu': self.resolu,
            'fileType': self.fileType
        }

    def __str__(self):
        return str(self.toDict())


class Reponse(Demande):
    def __init__(self, params: dict):
        self._id = params['_id']
        self.id_utilisateur = params['id-utilisateur']
        self.contenu = params['contenu']
        self.date_envoi = params['date-envoi']
        self.likes = params['likes']
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

    def convert_links(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(re.sub('^http(s?)://', '', w), w),
                w)
            contenu += ' '

        return contenu

    def toDict(self) -> dict:
        return {
            '_id': self._id,
            'idRep': self._id,
            'id-utilisateur': self.id_utilisateur,
            'original-contenu': self.contenu,
            'contenu': self.convert_links(),
            'date-envoi': self.date_envoi,
            'likes': self.likes,
            'nb-likes': len(self.likes),
            'a_like': self.aLike(),
            'a_sign': self.aSign(),
            'temps': self.convertTime(),
            'sign': self.sign,
            'motif': self.motif,
            # on récupère en plus l'utilisateur pour prochainement afficher son nom/prenom/pseudo
            'user': utilisateurs.get(str(self.id_utilisateur)).toDict()
        }

    def toDB(self) -> dict:
        return {
            '_id': self._id,
            'id-utilisateur': self.id_utilisateur,
            'contenu': self.contenu,
            'date-envoi': self.date_envoi,
            'likes': self.likes,
            'sign': self.sign,
            'motif': self.motif
        }

    def __str__(self):
        return str(self.toDict())


class Message(Actions):
    def __init__(self, params: dict):
        self._id = params['_id']
        self.id_groupe = params['id-groupe']
        self.id_utilisateur = params['id-utilisateur']
        self.contenu = params['contenu']
        self.date_envoi = params['date-envoi']
        self.reponse = params['reponse']
        self.audio = params.get('audio', False)
        self.image = params.get('image', '')
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

        self.db_table = DB.db_messages

    def suppr(self) -> None:
        if self.audio == 'True':
            MyAudio = DB.db_files.find_one({'filename': self.contenu})
            DB.db_files.delete_one({'_id': MyAudio['_id']})
            DB.db_chunks.delete_many({'files_id': MyAudio['_id']})
        if self.image != '':
            MyAudio = DB.db_files.find_one({'filename': self.image})
            DB.db_files.delete_one({'_id': MyAudio['_id']})
            DB.db_chunks.delete_many({'files_id': MyAudio['_id']})
        self.delete()
        messages.pop(str(self._id))
        return

    def convert_links(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(re.sub('^http(s?)://', '', w), w),
                w)
            contenu += ' '

        return contenu

    def toDictLast(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'id-groupe': self.id_groupe,
            'id-utilisateur': self.id_utilisateur,
            'utilisateur': utilisateurs[str(self.id_utilisateur)].toDict(),
            'contenu': self.convert_links(),
            'original-contenu': self.contenu,
            'date-envoi': self.date_envoi,
            'audio': self.audio,
            'image': self.image
        }

    def toDict(self) -> dict:
        if self.reponse != "None" and str(self.reponse) in messages:
            rep = messages[str(self.reponse)].toDict()
        else:
            rep = None
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'id-groupe': self.id_groupe,
            'groupe': groupes[str(self.id_groupe)].toDict(),
            'id-utilisateur': self.id_utilisateur,
            'utilisateur': utilisateurs[str(self.id_utilisateur)].toDict(),
            'contenu': self.convert_links(),
            'original-contenu': self.contenu,
            'date-envoi': self.date_envoi,
            'reponse': self.reponse,
            'rep': rep,
            'audio': self.audio,
            'image': self.image,
            'sign': self.sign,
            'motif': self.motif
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'id-groupe': self.id_groupe,
            'id-utilisateur': self.id_utilisateur,
            'contenu': self.contenu,
            'date-envoi': self.date_envoi,
            'reponse': self.reponse,
            'audio': self.audio,
            'image': self.image,
            'sign': self.sign,
            'motif': self.motif
        }

    def __str__(self):
        return str(self.toDict())


class Groupe(Actions):
    def __init__(self, params: dict):
        self._id = params['_id']
        self.nom = params['nom']
        self.is_class = params.get('is_class', False)
        self.is_DM = params.get('is_DM', False)
        self.is_mod = params.get('is_mod', False)
        self.id_utilisateurs = params['id-utilisateurs']
        self.moderateurs = params.get('moderateurs', [])
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

        self.db_table = DB.db_groupes

    def supprGroupe(self):
        grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == self._id]
        for m in grpMsg:
            messages[str(m['_id'])].suppr()

        self.delete()
        groupes.pop(str(self._id))
        return

    def supprUser(self, uid):
        self.id_utilisateurs.remove(uid)
        if uid in self.moderateurs:
            self.moderateurs.remove(uid)
        if len(self.id_utilisateurs) == 0:
            self.supprGroupe()
            return
        elif len(self.moderateurs) == 0 and self.is_class == False:
            self.moderateurs.append(self.id_utilisateurs[0])
        self.update()

    def getAllMessages(self):
        return sorted([message.toDict() for id, message in messages.copy().items() if self._id == message.id_groupe], key=lambda message: message['date-envoi'])

    def getAllMessagesSign(self):
        return sorted([message.toDict() for id, message in messages.copy().items() if self._id == message.id_groupe and message.sign != []], key=lambda message: message['date-envoi'])

    def getLastMessage(self):
        l = sorted([message.toDictLast() for id, message in messages.copy().items()
        if self._id == message.id_groupe], key=lambda message: message['date-envoi'])
        return l[-1] if len(l) > 0 else None

    def getNbNotif(self, uid):
        if uid != None:
            return len([notif for notif in notifications.values() if notif.type == 'msg' and notif.id_groupe == self._id and uid in notif.destinataires])
        else:
            return None

    def toDict(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'nom': self.nom,
            'is_class': self.is_class,
            'is_DM': self.is_DM,
            'is_mod': self.is_mod,
            'id-utilisateurs': self.id_utilisateurs,
            'utilisateurs': [user.toDict() for id, user in utilisateurs.items() if ObjectId(id) in self.id_utilisateurs],
            'nbUtilisateurs': len(self.id_utilisateurs),
            'lastMsg': self.getLastMessage(),
            'nbNotif': self.getNbNotif(ObjectId(session['id']) if session != None and 'id' in session else None),
            'moderateurs': self.moderateurs,
            'modos': [user.toDict() for id, user in utilisateurs.items() if ObjectId(id) in self.moderateurs],
            'sign': self.sign,
            'motif': self.motif
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'nom': self.nom,
            'is_class': self.is_class,
            'is_DM': self.is_DM,
            'is_mod': self.is_mod,
            'id-utilisateurs': self.id_utilisateurs,
            'moderateurs': self.moderateurs,
            'sign': self.sign,
            'motif': self.motif
        }

    def __str__(self):
        return str(self.toDict())

clientsNotif = {}

class Notification(Actions):
    def __init__(self, params: dict):
        self._id = params['_id']
        self.type = params['type']
        self.id_groupe = params['id_groupe']
        self.id_msg = params['id_msg']
        self.date = params['date']
        self.destinataires = params['destinataires']
        self.db_table = DB.db_notif

    def create(type, id_groupe, id_msg, destinataires):
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
            notifications[str(_id)].send()
        return

    def diffTemps(self):
        diff_temps = int((datetime.now() - self.date).total_seconds())
        return diff_temps

    def convertTime(self):
        tempsStr = ''
        diffTemps = self.diffTemps()
        # puis on se fait chier à trouver le délai entre le poste et aujourd'hui
        if diffTemps // (60 * 60 * 24 * 7):  # semaines
            tempsStr += '{}sem '.format(diffTemps // (60 * 60 * 24 * 7))
            if (diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24):  # jours
                tempsStr += '{}j '.format((diffTemps %
                                           (60 * 60 * 24 * 7)) // (60 * 60 * 24))
        elif diffTemps // (60 * 60 * 24):  # jours
            tempsStr += '{}j '.format(diffTemps // (60 * 60 * 24))
            if (diffTemps % (60 * 60 * 24)) // (60 * 60):  # heures
                tempsStr += '{}h '.format((diffTemps %
                                           (60 * 60 * 24)) // (60 * 60))
        elif diffTemps // (60 * 60):  # heures
            tempsStr += '{}h '.format(diffTemps // (60 * 60))
            if (diffTemps % (60 * 60)) // 60:  # minutes
                tempsStr += '{}min '.format(diffTemps % (60 * 60) // 60)
        else:
            tempsStr = '{}min'.format(diffTemps // 60)

        return tempsStr

    def send(self):
        from main import socketio
        notification = self.toDict()
        html = render_template("notification.html", notif=notification, similar=0)

        for user in notification['userDest']:
            if str(user['_id']) in clientsNotif:
                socketio.emit('newNotif', {'html': html, 'sound': str(user['notifs']['sound'])}, to=str(user['_id']))
            elif user['email'] != "" or user['emailENT'] != "":
                # si l'user a autorisé les notifs par mail
                if (self.type == 'msg' and user['notifs']['messages']) or (self.type == 'demande' and user['notifs']['demandes']):
                    # si un mail n'a pas déja été envoyé pour ce groupe
                    if (self.type == 'msg' and len([notif for notif in notifications.values() if notif.id_groupe == self.id_groupe and notif.type == 'msg' and user['_id'] in notif.destinataires]) == 1) or self.type == 'demande':
                        if user['email'] != "":
                            To = user['email']
                        elif user['emailENT'] != "":
                            To = user['emailENT']
                        else:
                            pass
                        htmlMail = render_template('mail.html', notif=notification, user=user)
                        envoi = Thread(target=self.sendMail, args=(To, htmlMail, notification['sender']['pseudo']))
                        envoi.start()
        return



    def sendMail(self, To, htmlMail, pseudo):
        serveur = 'key4school.com'
        port = '465'
        From = 'no-reply@key4school.com'
        password = os.environ['SMTP_password']
        codage = 'utf-8'
        with smtplib.SMTP_SSL(serveur, port) as mailserver:
            mailserver.login(From, password)

            msg = MIMEMultipart()
            msg['From'] = From
            msg['To'] = To
            msg['Subject'] = f'Key4School - Nouvelle notification de {pseudo}'
            msg['Charset'] = codage

            # attache message HTML
            msg.attach(MIMEText(htmlMail.encode(codage),
                                'html', _charset=codage))

            mailserver.sendmail(From, To, msg.as_string())
        return

    def getSimilar(self, uid):
        '''récupère les notifs du même groupe plus récentes'''
        return [notification for notification in notifications.values() if notification.id_groupe == self.id_groupe and notification.date >= self.date and notification._id != self._id and uid in notification.destinataires]

    def supprNotif(self):
        self.delete()
        if str(self._id) in notifications:
            notifications.pop(str(self._id))
        return

    def supprUser(self, uid):
        if uid in self.destinataires:
            self.destinataires.remove(uid)
        if len(self.destinataires) > 0:
            self.update()
        else:
            self.supprNotif()
        return

    def toDict(self) -> dict:
        if self.type == 'msg':
            if str(self.id_groupe) in groupes and str(self.id_msg) in messages:
                grp = groupes[str(self.id_groupe)].toDict()
                msg = messages[str(self.id_msg)].toDict()
            else:
                self.supprNotif()
                return
        elif self.type == 'demande':
            if str(self.id_groupe) in demandes_aide:
                grp = demandes_aide[str(self.id_groupe)].toDict()
                if str(self.id_msg) in grp['reponsesDict']:
                    msg = grp['reponsesDict'][str(self.id_msg)]
                else:
                    self.supprNotif()
                    return
            else:
                self.supprNotif()
                return
        sender = utilisateurs[str(msg['id-utilisateur'])].toDict()
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'type': self.type,
            'id_groupe': self.id_groupe,
            'groupe': grp,
            'id_msg': self.id_msg,
            'message': msg,
            "sender": sender,
            'date': self.date,
            'temps': self.convertTime(),
            'destinataires': self.destinataires,
            'userDest': [utilisateurs.get(str(destinataire)).toDict() for destinataire in self.destinataires if utilisateurs.get(str(destinataire)) != None]
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            '_id': self._id,
            'type': self.type,
            'id_groupe': self.id_groupe,
            'id_msg': self.id_msg,
            'date': self.date,
            'destinataires': self.destinataires
        }

    def __str__(self):
        return str(self.toDict())
