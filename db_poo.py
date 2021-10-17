from datetime import *
from flask import session, escape, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from functools import wraps
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
from matieresDict import translations, translateProf
from datetime import *
import inspect

Base = declarative_base()

# gestionnaire de session
@contextmanager
def session_scope():
    session = dbSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# decorateur -> creer session et la ferme a la fin
def db_session(func):
    @wraps(func) # permet de garder le nom de la fonction pour Flask
    def return_func(*param, **param2):
        with session_scope() as s:
            func.__globals__.update({'s': s})
            return_value = func(*param, **param2)
        return return_value

    return return_func

def get_context(func):
    @wraps(func)
    def return_func(*param, **param2):
        func.__globals__.update(inspect.currentframe().f_back.f_locals | inspect.currentframe().f_back.f_globals)
        return_value = func(*param, **param2)
        return return_value

    return return_func


class Actions:
    @get_context
    def insert(self):
        s.add(self)
        s.commit()

    @classmethod
    @get_context
    def get(cls, filter=None, limit=None, order_by=None, desc=False):
        query = s.query(cls)
        if filter:
            query = query.filter(eval(filter))
        if query.count() == 0:
            return None
        if limit == 1:
            query = query.one()
        elif limit:
            query = query.limit(limit)
        else:
            query = query.all()
        if order_by:
            if desc:
                query = query.order_by(eval(order_by).desc())
            else:
                query = query.order_by(eval(order_by))
        return query

    @get_context
    def update(self):
        s.commit()

    @get_context
    def delete(self):
        self.delete()
        s.commit()


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


class User(Translate_matiere_spes_options_lv, Actions, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    pseudo = Column(String)
    email = Column(String)
    mdp = Column(String)
    type = Column(String)
    dateInscription = Column(DateTime)
    etapeInscription = Column(Integer)

    birth_date = Column(DateTime)
    classe = Column(String)
    telephone = Column(String)
    lycee = Column(String)
    lyceeId = Column(String)
    langues = Column(JSONB)

    options = Column(JSONB)
    spes = Column(JSONB)
    matiere = Column(String)
    matiere_autre = Column(JSONB)

    nomImg = Column(String)
    imgProfile = Column(String)

    couleur = Column(JSONB)
    theme = Column(String)

    elementPublic = Column(JSONB)
    elementPrive = Column(JSONB)

    interets = Column(String)

    notifs = Column(JSONB)

    sign = Column(JSONB)
    Sanctions = Column(JSONB)
    SanctionEnCour = Column(String)
    SanctionDuree = Column(String)

    xp = Column(Integer)
    xpModeration = Column(Integer)
    motif = Column(JSONB)

    admin = Column(Boolean)

    savedDemands = Column(JSONB)

    def __init__(self, **params):
        self.nom = params['nom']
        self.prenom = params['prenom']
        self.pseudo = params['pseudo']
        self.email = params['email']
        self.mdp = params['mdp']
        self.type = 'ELEVE'
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

    @property
    def niv(self):
        return int(0.473*self.xp**0.615)

    @property
    def xplvl(self):
        return int((0.473*self.xp**0.615-niv)*100)

    @property
    def matieres(self):
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

    @property
    def a_sign(self):
        if ObjectId(session.get('id')) in self.sign:
            return True
        else:
            return False

    def __setitem__(self, key, value):
          setattr(self, key, value)

    def __getitem__(self, key):
        methods = {
            'spes-str': (self.translate_matiere_spes_options_lv, self.spes),
            'langues-str': (self.translate_matiere_spes_options_lv, self.langues),
            'options-str':(self.translate_matiere_spes_options_lv, self.options),
            'matiere-str': (self.translate_matiere_spes_options_lv, self.matiere),
            'matiere_autre-str': (self.translate_matiere_spes_options_lv, self.matiere_autre)
        }
        if key in methods:
            return methods[key][0](methods[key][1])
        else:
            return getattr(self, key)

    def __repr__(self):
        return f'<User id={self.id}, pseudo={self.pseudo}>'


class Request(Translate_matiere_spes_options_lv, Actions, Base):
    __tablename__ = 'help_requests'

    id = Column(Integer, primary_key=True)
    id_utilisateur = Column(Integer)
    titre = Column(String)
    contenu = Column(String)
    date_envoi = Column(DateTime)
    matiere = Column(String)
    reponses_associees = Column(JSONB)
    likes = Column(JSONB)
    sign = Column(JSONB)
    motif = Column(JSONB)
    resolu = Column(Boolean)
    fileType = Column(String)

    def __init__(self, **params):
        self.id_utilisateur = params['id-utilisateur']
        self.titre = params['titre']
        self.contenu = params['contenu']
        self.date_envoi = params.get('date_envoi', datetime.now())
        self.matiere = params['matière']
        self.reponses_associees = params.get('reponses_associees', [])
        self.likes = params.get('likes', [])
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])
        self.resolu = params.get('resolu', False)
        self.fileType = params.get('fileType', 'none')

    def diffTemps(self):
        diff_temps = int((datetime.now() - self.date_envoi).total_seconds())
        return diff_temps

    @property
    def temps(self):
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

    @property
    def aLike(self):
        if session['id'] in self.likes:
            return True
        else:
            return False

    @property
    def aSign(self):
        if session['id'] in self.sign:
            return True
        else:
            return False

    @property
    def aSave(self):
        user = User.get(filter="cls.id == session['id']", limit=1)

        if self.id in user.savedDemands:
            return True
        else:
            return False

    @property
    def contenuLink(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(re.sub('^http(s?)://', '', w), w),
                w)
            contenu += ' '

        return contenu

    @property
    def nb_likes(self):
        return len(self.likes)

    @property
    def nb_comment(self):
        return len(reponses_associees)

    @property
    def user(self):
        return User.get(filter="cls.id == self.id_utilisateur", limit=1)

    # def toDict(self) -> dict:
    #     return {  # on ajoute à la liste ce qui nous interesse
    #         'réponses associées': sorted([r.toDict() for r in self.reponses_associees.values()], key=lambda r: r['nb_likes'], reverse=True),
    #         'reponsesDict': {idRep: rep.toDict() for (idRep, rep) in self.reponses_associees.items()},
    #         'reponsesDict2': {idRep: rep for (idRep, rep) in self.reponses_associees.items()}
    #     }

    def __setitem__(self, key, value):
          setattr(self, key, value)

    def __getitem__(self, key):
        methods = {
            'matière': (self.translate_matiere_spes_options_lv, [self.matiere])
        }
        if key in methods:
            return methods[key][0](methods[key][1])
        else:
            return getattr(self, key)

    def __repr__(self):
        return f'<User id={self.id}, pseudo={self.titre}>'


class Response(Request, Actions, Base):
    __tablename__ = 'help_reponse'

    id = Column(Integer, primary_key=True)
    id_utilisateur = Column(Integer)
    contenu = Column(String)
    date_envoi = Column(DateTime)
    likes = Column(JSONB)
    sign = Column(JSONB)
    motif = Column(JSONB)

    def __init__(self, **params):
        self.id_utilisateur = params['id-utilisateur']
        self.contenu = params['contenu']
        self.date_envoi = params.get('date_envoi', datetime.now())
        self.likes = params.get('likes', [])
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

    def contenuLink(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(re.sub('^http(s?)://', '', w), w),
                w)
            contenu += ' '

        return contenu

    def __setitem__(self, key, value):
          setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return f'<User id={self.id}, pseudo={self.titre}>'


class Message(Actions):
    def __init__(self, params: dict):
        self.id = params['id']
        self.id_groupe = params['id-groupe']
        self.id_utilisateur = params['id-utilisateur']
        self.contenu = params['contenu']
        self.date_envoi = params['date_envoi']
        self.reponse = params['reponse']
        self.audio = params.get('audio', False)
        self.image = params.get('image', '')
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

        self.db_table = DB.db_messages

    def suppr(self) -> None:
        if self.audio == 'True':
            MyAudio = DB.db_files.find_one({'filename': self.contenu})
            DB.db_files.delete_one({'id': MyAudio['id']})
            DB.db_chunks.delete_many({'filesid': MyAudio['id']})
        if self.image != '':
            MyAudio = DB.db_files.find_one({'filename': self.image})
            DB.db_files.delete_one({'id': MyAudio['id']})
            DB.db_chunks.delete_many({'filesid': MyAudio['id']})
        self.delete()
        messages.pop(str(self.id))
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
            'id': self.id,
            'id-groupe': self.id_groupe,
            'id-utilisateur': self.id_utilisateur,
            'utilisateur': User.get(filter="cls.id == self.id_utilisateur", limit=1),
            'contenu': self.convert_links(),
            'original-contenu': self.contenu,
            'date_envoi': self.date_envoi,
            'audio': self.audio,
            'image': self.image
        }

    def toDict(self) -> dict:
        if self.reponse != "None" and str(self.reponse) in messages:
            rep = messages[str(self.reponse)].toDict()
        else:
            rep = None
        return {  # on ajoute à la liste ce qui nous interesse
            'id': self.id,
            'id-groupe': self.id_groupe,
            'groupe': groupes[str(self.id_groupe)].toDict(),
            'id-utilisateur': self.id_utilisateur,
            'utilisateur': User.get(filter="cls.id == self.id_utilisateur", limit=1),
            'contenu': self.convert_links(),
            'original-contenu': self.contenu,
            'date_envoi': self.date_envoi,
            'reponse': self.reponse,
            'rep': rep,
            'audio': self.audio,
            'image': self.image,
            'sign': self.sign,
            'motif': self.motif
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            'id': self.id,
            'id-groupe': self.id_groupe,
            'id-utilisateur': self.id_utilisateur,
            'contenu': self.contenu,
            'date_envoi': self.date_envoi,
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
        self.id = params['id']
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
        grpMsg = [m.toDict() for m in messages.values() if m.id_groupe == self.id]
        for m in grpMsg:
            messages[str(m['id'])].suppr()

        self.delete()
        groupes.pop(str(self.id))
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
        return sorted([message.toDict() for id, message in messages.copy().items() if self.id == message.id_groupe], key=lambda message: message['date_envoi'])

    def getAllMessagesSign(self):
        return sorted([message.toDict() for id, message in messages.copy().items() if self.id == message.id_groupe and message.sign != []], key=lambda message: message['date_envoi'])

    def getLastMessage(self):
        l = sorted([message.toDictLast() for id, message in messages.copy().items()
        if self.id == message.id_groupe], key=lambda message: message['date_envoi'])
        return l[-1] if len(l) > 0 else None

    def getNbNotif(self, uid):
        if uid != None:
            return len([notif for notif in notifications.values() if notif.type == 'msg' and notif.id_groupe == self.id and uid in notif.destinataires])
        else:
            return None

    def toDict(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            'id': self.id,
            'nom': self.nom,
            'is_class': self.is_class,
            'is_DM': self.is_DM,
            'is_mod': self.is_mod,
            'id-utilisateurs': self.id_utilisateurs,
            'utilisateurs': User.get(filter="cls.id.comparator.contains_by(self.id_utilisateurs)"),
            'nbUtilisateurs': len(self.id_utilisateurs),
            'lastMsg': self.getLastMessage(),
            'nbNotif': self.getNbNotif(session['id'] if session != None and 'id' in session else None),
            'moderateurs': self.moderateurs,
            'modos': User.get(filter="cls.id.comparator.contains_by(self.moderateurs)"),
            'sign': self.sign,
            'motif': self.motif
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            'id': self.id,
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
        self.id = params['id']
        self.type = params['type']
        self.id_groupe = params['id_groupe']
        self.id_msg = params['id_msg']
        self.date = params['date']
        self.destinataires = params['destinataires']
        self.db_table = DB.db_notif

    def create(type, id_groupe, id_msg, destinataires):
        if type == 'demande':
            destinataires += User.get(filter="cls.savedDemands.comparator.has(id_groupe)")

        if session['id'] in destinataires:
            destinataires.remove(session['id'])

        destinataires = list(set(destinataires))

        if len(destinataires) > 0:
            id = ObjectId()
            notifications[str(id)] = Notification({"id": id, "type": type, "id_groupe": id_groupe, "id_msg": id_msg,
                                            "date": datetime.now(), "destinataires": destinataires})
            notifications[str(id)].insert()
            notifications[str(id)].send()
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

    @get_context
    def send(self):
        notification = self.toDict()
        html = render_template("notification.html", notif=notification, similar=0)

        for user in notification['userDest']:
            if str(user['id']) in clientsNotif:
                socketio.emit('newNotif', {'html': html, 'sound': str(user['notifs']['sound'])}, to=str(user['id']))
            elif user['email'] != "" or user['emailENT'] != "":
                # si l'user a autorisé les notifs par mail
                if (self.type == 'msg' and user['notifs']['messages']) or (self.type == 'demande' and user['notifs']['demandes']):
                    # si un mail n'a pas déja été envoyé pour ce groupe
                    if (self.type == 'msg' and len([notif for notif in notifications.values() if notif.id_groupe == self.id_groupe and notif.type == 'msg' and user['id'] in notif.destinataires]) == 1) or self.type == 'demande':
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
        return [notification for notification in notifications.values() if notification.id_groupe == self.id_groupe and notification.date >= self.date and notification.id != self.id and uid in notification.destinataires]

    def supprNotif(self):
        self.delete()
        if str(self.id) in notifications:
            notifications.pop(str(self.id))
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
        sender = User.get(filter="cls.id == msg['id-utilisateur']", limit=1)
        return {  # on ajoute à la liste ce qui nous interesse
            'id': self.id,
            'type': self.type,
            'id_groupe': self.id_groupe,
            'groupe': grp,
            'id_msg': self.id_msg,
            'message': msg,
            "sender": sender,
            'date': self.date,
            'temps': self.convertTime(),
            'destinataires': self.destinataires,
            'userDest': User.get(filter="cls.id.comparator.contains_by(self.destinataires)")
        }

    def toDB(self) -> dict:
        return {  # on ajoute à la liste ce qui nous interesse
            'id': self.id,
            'type': self.type,
            'id_groupe': self.id_groupe,
            'id_msg': self.id_msg,
            'date': self.date,
            'destinataires': self.destinataires
        }

    def __str__(self):
        return str(self.toDict())

# configuration de la database
DATABASE_URI = 'postgresql://rxtmhycolmbxky:d66072b10150c9b7dbe86a026cc7e08f670b8fcf6a45ff71160863069c896ec2@ec2-52-210-120-210.eu-west-1.compute.amazonaws.com:5432/d3vkha7h4hsf16'
engine = create_engine(DATABASE_URI)
if __name__ == "__main__":
    # vider la DB
    if input('Voulez vous reset la base de donnée ? (Y/n)') == 'Y':
        Base.metadata.drop_all(engine)
else:
    Base.metadata.create_all(engine)
dbSession = sessionmaker(bind=engine)
