from datetime import *
from flask import session, escape, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB, UUID
from uuid import uuid1
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
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
    @wraps(func)  # permet de garder le nom de la fonction pour Flask
    def return_func(*param, **param2):
        with session_scope() as s:
            func.__globals__.update({'s': s})
            return_value = func(*param, **param2)
        return return_value

    return return_func


def get_context(func):
    @wraps(func)
    def return_func(*param, **param2):
        func.__globals__.update(inspect.currentframe(
        ).f_back.f_locals | inspect.currentframe().f_back.f_globals)
        return_value = func(*param, **param2)
        return return_value

    return return_func


def generate_uuid():
    return str(uuid1())


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

        if order_by:
            if desc:
                query = query.order_by(eval(order_by).desc())
            else:
                query = query.order_by(eval(order_by))

        try:
            del globals()['temp']
            del locals()['temp']
        except Exception:
            pass

        if limit == 1:
            if query.count() == 0:
                return None
            query = query.first()
        elif limit:
            if query.count() == 0:
                return []
            query = query.limit(limit).all()
        else:
            if query.count() == 0:
                return []
            query = query.all()

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

    id = Column(UUID(as_uuid=False), primary_key=True,
                default=generate_uuid, unique=True)
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
        self.matiere = params.get('matiere', '')  # pour les profs
        self.matiere_autre = params.get('matiere_autre', [])  # pour les profs

        self.nomImg = params.get('nomImg', '')
        self.imgProfile = params.get('imgProfile', '')

        self.couleur = params.get(
            'couleur', ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'])
        self.theme = params.get('theme', 'system')

        self.elementPublic = params.get('elementPublic', [])
        self.elementPrive = params.get(
            'elementPrive', ['email', 'telephone', 'interets', 'birth_date'])

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
        return int((0.473*self.xp**0.615-self.niv)*100)

    @property
    def xplvlMax(self):
        return int((100*self.xp)/self.xplvl)

    @property
    def matieres(self):
        '''A REFAIRE'''
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
            '''AJOUTER LES NOUVELLES LANGUES'''
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
                subjects = ['ang', 'esp', 'all',
                            'it', 'chi', 'ru', 'por', 'ara']
                subjects += [key for key,
                             value in translations.items() if not 'lv' in key]
        return subjects

    @property
    def a_sign(self):
        if session.get('id') in self.sign:
            return True
        else:
            return False

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, key):
        methods = {
            'spes-str': (self.translate_matiere_spes_options_lv, self.spes),
            'langues-str': (self.translate_matiere_spes_options_lv, self.langues),
            'options-str': (self.translate_matiere_spes_options_lv, self.options),
            'matiere-str': (self.translate_matiere_spes_options_lv, self.matiere),
            'matiere_autre-str': (self.translate_matiere_spes_options_lv, self.matiere_autre)
        }
        if key in methods:
            return methods[key][0](methods[key][1])
        else:
            return getattr(self, key)

    def __contains__(self, key):
        methods = {
            'spes-str': (self.translate_matiere_spes_options_lv, self.spes),
            'langues-str': (self.translate_matiere_spes_options_lv, self.langues),
            'options-str': (self.translate_matiere_spes_options_lv, self.options),
            'matiere-str': (self.translate_matiere_spes_options_lv, self.matiere),
            'matiere_autre-str': (self.translate_matiere_spes_options_lv, self.matiere_autre)
        }
        if key in methods:
            return True
        else:
            return hasattr(self, key)

    def __repr__(self):
        return f'<User id={self.id}, pseudo={self.pseudo}>'


class Request(Translate_matiere_spes_options_lv, Actions, Base):
    __tablename__ = 'help_requests'

    id = Column(UUID(as_uuid=False), primary_key=True,
                default=generate_uuid, unique=True)
    id_utilisateur = Column(UUID(as_uuid=False))
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
        self.id_utilisateur = params['id_utilisateur']
        self.titre = params['titre']
        self.contenu = params['contenu']
        self.date_envoi = params.get('date_envoi', datetime.now())
        self.matiere = params['matière']
        self.reponses_associees = params.get('reponses_associees', [])
        self.likes = params.get('likes', [])
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])
        self.resolu = params.get('resolu', False)
        self.fileType = params.get('fileType', None)

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
                              '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(
                                  re.sub('^http(s?)://', '', w), w),
                              w)
            contenu += ' '

        return contenu

    @property
    def rep(self):
        temp = self.reponses_associees
        print(type(temp))
        return Response.get(filter="cls.id in temp")

    @property
    def nb_likes(self):
        return len(self.likes)

    @property
    def nb_comment(self):
        return len(self.reponses_associees)

    @property
    def user(self):
        temp = self.id_utilisateur
        return User.get(filter="cls.id == temp", limit=1)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, key):
        methods = {
            'matière': (self.translate_matiere_spes_options_lv, [self.matiere])
        }
        if key in methods:
            return methods[key][0](methods[key][1])
        else:
            return getattr(self, key)

    def __contains__(self, key):
        methods = {
            'matière': (self.translate_matiere_spes_options_lv, [self.matiere])
        }
        if key in methods:
            return True
        else:
            return hasattr(self, key)

    def __repr__(self):
        return f'<Request id={self.id}, title={self.titre}>'


class Response(Actions, Base):
    __tablename__ = 'help_responses'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=generate_uuid, unique=True)
    id_utilisateur = Column(UUID(as_uuid=True))
    contenu = Column(String)
    date_envoi = Column(DateTime)
    likes = Column(JSONB)
    sign = Column(JSONB)
    motif = Column(JSONB)

    def __init__(self, **params):
        self.id_utilisateur = params['id_utilisateur']
        self.contenu = params['contenu']
        self.date_envoi = params.get('date_envoi', datetime.now())
        self.likes = params.get('likes', [])
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

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
    def contenuLink(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                              '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(
                                  re.sub('^http(s?)://', '', w), w),
                              w)
            contenu += ' '

        return contenu

    @property
    def nb_likes(self):
        return len(self.likes)

    @property
    def user(self):
        temp = self.id_utilisateur
        return User.get(filter="cls.id == temp", limit=1)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __repr__(self):
        return f'<Response id={self.id}, content={self.contenu[0:15]}>'


class Message(Actions, Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=generate_uuid, unique=True)
    id_groupe = Column(UUID(as_uuid=False))
    id_utilisateur = Column(UUID(as_uuid=False))
    contenu = Column(String)
    date_envoi = Column(DateTime)
    reponse = Column(UUID(as_uuid=False))
    audio = Column(Boolean)
    image = Column(String)
    sign = Column(JSONB)
    motif = Column(JSONB)

    def __init__(self, **params):
        self.id_groupe = params['id_groupe']
        self.id_utilisateur = params['id_utilisateur']
        self.contenu = params['contenu']
        self.date_envoi = params.get('date_envoi', datetime.now())
        self.reponse = params['reponse']
        self.audio = params.get('audio', False)
        self.image = params.get('image', '')
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

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
        return

    @property
    def contentLink(self) -> str:
        safe = escape(self.contenu)
        contenu = ''
        for w in safe.split():
            contenu += re.sub("^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$",
                              '<a href="//{}" target="_blank" style="overflow-wrap: break-word;">{}</a>'.format(
                                  re.sub('^http(s?)://', '', w), w),
                              w)
            contenu += ' '

        return contenu

    @property
    def utilisateur(self):
        temp = self.id_utilisateur
        return User.get(filter="cls.id == temp", limit=1)

    @property
    def groupe(self):
        temp = self.id_groupe
        return Group.get(filter="cls.id == temp", limit=1)

    @property
    def rep(self):
        if self.reponse:
            temp = self.reponse
            rep = Message.get(filter="cls.id == temp", limit=1)
        else:
            rep = None
        return rep

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __repr__(self):
        return f'<Message id={self.id}, content={self.contenu[0:15]}>'


class Group(Actions, Base):
    __tablename__ = 'groups'

    id = Column(UUID(as_uuid=False), primary_key=True,
                default=generate_uuid, unique=True)
    nom = Column(String)
    is_class = Column(Boolean)
    is_DM = Column(Boolean)
    is_mod = Column(Boolean)
    id_utilisateurs = Column(JSONB)
    moderateurs = Column(JSONB)
    sign = Column(JSONB)
    motif = Column(JSONB)

    def __init__(self, **params):
        self.nom = params['nom']
        self.is_class = params.get('is_class', False)
        self.is_DM = params.get('is_DM', False)
        self.is_mod = params.get('is_mod', False)
        self.id_utilisateurs = params['id_utilisateurs']
        self.moderateurs = params.get('moderateurs', [])
        self.sign = params.get('sign', [])
        self.motif = params.get('motif', [])

    def supprGroupe(self):
        grpMsg = Message.get(filter="cls.id_groupe == self.id")
        for m in grpMsg:
            m.suppr()

        self.delete()
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

    @property
    def getAllMessages(self):
        temp = self.id
        return Message.get(filter="cls.id_groupe == temp", order_by="cls.date_envoi")

    @property
    def getAllMessagesSign(self):
        temp = self.id
        return Message.get(filter="cls.id_groupe == temp and cls.sign != '[]'", order_by="cls.date_envoi")

    @property
    def lastMsg(self):
        temp = self.id
        return Message.get(filter="cls.id_groupe == temp", order_by="cls.date_envoi", desc=True, limit=1)

    @property
    def nbNotif(self, uid=None):
        if uid == None:
            uid = session['id'] if session != None and 'id' in session else None
        if uid != None:
            id = self.id
            return len(Notification.get(filter="cls.type == 'msg' and cls.id_groupe == id and cls.destinataires.comparator.has(uid)"))
        else:
            return None

    @property
    def nbUtilisateurs(self):
        return len(self.id_utilisateurs)

    @property
    def utilisateurs(self):
        temp = self.id_utilisateurs
        return User.get(filter="cls.id in temp")

    @property
    def modos(self):
        temp = self.moderateurs
        return User.get(filter="cls.id in temp")

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __repr__(self):
        return f'<Group id={self.id}, nom={self.nom}>'


clientsNotif = {}


class Notification(Actions, Base):
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=False), primary_key=True,
                default=generate_uuid, unique=True)
    type = Column(String)
    id_groupe = Column(UUID(as_uuid=False))
    id_msg = Column(UUID(as_uuid=False))
    date = Column(DateTime)
    destinataires = Column(JSONB)

    def __init__(self, **params):
        self.id = params['id']
        self.type = params['type']
        self.id_groupe = params['id_groupe']
        self.id_msg = params['id_msg']
        self.date = params.get('date', datetime.now())
        self.destinataires = params['destinataires']

    @classmethod
    def create(cls, type, id_groupe, id_msg, destinataires):
        if type == 'demande':
            for user in User.get(filter="cls.savedDemands.comparator.has_key(str(id_groupe))"):
                destinataires.append(user['id'])

        if session['id'] in destinataires:
            destinataires.remove(session['id'])

        destinataires = list(set(destinataires))

        if len(destinataires) > 0:
            notification = Notification(
                type=type, id_groupe=id_groupe, id_msg=id_msg, destinataires=destinataires)
            notification.insert()
            notification.send()
        else:
            notification = None
        return notification

    def diffTemps(self):
        diff_temps = int((datetime.now() - self.date).total_seconds())
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

    @get_context
    def send(self):
        notification = self
        html = render_template("notification.html",
                               notif=notification, similar=0)

        for user in notification['userDest']:
            if user['id'] in clientsNotif:
                socketio.emit(
                    'newNotif', {'html': html, 'sound': user['notifs']['sound']}, to=user['id'])
            elif user['email'] != "":
                # si l'user a autorisé les notifs par mail
                if (self.type == 'msg' and user['notifs']['messages']) or (self.type == 'demande' and user['notifs']['demandes']):
                    # si un mail n'a pas déja été envoyé pour ce groupe
                    if (self.type == 'msg' and len(Notification.get(filter="cls.type == 'msg' and cls.id_groupe == self.id and cls.destinataires.comparator.has_key(str(user['id']))")) == 1) or self.type == 'demande':
                        if user['email'] != "":
                            To = user['email']
                        else:
                            pass
                        htmlMail = render_template(
                            'mail.html', notif=notification, user=user)
                        envoi = Thread(target=self.sendMail, args=(
                            To, htmlMail, notification['sender']['pseudo']))
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
        return Notification.get(filter="cls.id_groupe == self.id_groupe and cls.date >= self.date and cls.id != self.id and cls.destinataires.comparator.has(uid)")

    def supprNotif(self):
        self.delete()
        return

    def supprUser(self, uid):
        if uid in self.destinataires:
            self.destinataires.remove(uid)
        if len(self.destinataires) > 0:
            self.update()
        else:
            self.supprNotif()
        return

    def verifNotif(self):
        if self.type == 'msg':
            if not Group.get(filter="cls.id == self.id_groupe", limit=1) and not Message.get(filter="cls.id == self.id_msg", limit=1):
                self.supprNotif()
                return True
        elif self.type == 'demande':
            if Request.get(filter="cls.id == self.id_groupe", limit=1):
                if not Response.get(filter="cls.id == self.id_msg", limit=1):
                    self.supprNotif()
                    return True
            else:
                self.supprNotif()
                return True

    @property
    def groupe(self):
        if self.type == 'msg':
            return Group.get(filter="cls.id == self.id_groupe", limit=1)
        elif self.type == 'demande':
            return Request.get(filter="cls.id == self.id_groupe", limit=1)

    @property
    def message(self):
        if self.type == 'msg':
            return Message.get(filter="cls.id == self.id_msg", limit=1)
        elif self.type == 'demande':
            return Response.get(filter="cls.id == self.id_msg", limit=1)

    @property
    def sender(self):
        '''A REVOIR PEUT ETRE ERREUR'''
        return User.get(filter="cls.id == msg['id_utilisateur']", limit=1)

    @property
    def userDest(self):
        temp = self.destinataires
        return User.get(filter="cls.id in temp")

    def __setitem__(self, key, value):
        if self.verifNotif():
            return
        return setattr(self, key, value)

    def __getitem__(self, key):
        if self.verifNotif():
            return
        return getattr(self, key)

    def __contains__(self, key):
        return hasattr(self, key)

    def __repr__(self):
        return f'<Notification id={self.id}, type={self.type}>'


# configuration de la database
DATABASE_URI = 'postgresql://rxtmhycolmbxky:d66072b10150c9b7dbe86a026cc7e08f670b8fcf6a45ff71160863069c896ec2@ec2-52-210-120-210.eu-west-1.compute.amazonaws.com:5432/d3vkha7h4hsf16'
engine = create_engine(DATABASE_URI)
if __name__ == "__main__":
    # vider la DB
    if input('Voulez vous reset la base de donnée ? (Y/n)') == 'Y':
        Base.metadata.drop_all(engine)
else:
    Base.metadata.create_all(engine)
dbSession = sessionmaker(bind=engine, expire_on_commit=False)
