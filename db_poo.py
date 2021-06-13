from datetime import *
from bson.objectid import ObjectId
from flask import session
from flask_pymongo import PyMongo

utilisateurs = {}
demandes_aide = {}
messages = {}
groupes = {}
notifications = {}
DB = None

class DB_Manager:
	def __init__(self, app, cluster_url):
		self.cluster = PyMongo(app, cluster_url)
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
		DB = DB_Manager(app, cluster_url)
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
		translations = {
	        # Matières tronc commun
	        'fr': 'Français',
	        'maths': 'Mathématiques',
	        'hg': 'Histoire-Géographie',
	        'snt': 'SNT',
	        'pc': 'Physique-Chimie',
	        'svt': 'SVT',
	        'emc': 'EMC',
	        'ses': 'SES',
	        'philo': 'Philosophie',
	        'eps': 'EPS',
	        # Langues
	        'ang': 'Anglais',
	        'esp': 'Espagnol',
	        'all': 'Allemand',
	        'por': 'Portugais',
	        'it': 'Italien',
	        'chi': 'Chinois',
	        'ru': 'Russe',
	        'ara': 'Arabe',
	        # LV1
	        'lv1-ang': 'LV1 Anglais',
	        'lv1-ang-euro': 'LV1 Anglais Euro',
	        'lv1-esp': 'LV1 Espagnol',
	        'lv1-esp-euro': 'LV1 Espagnol Euro',
	        'lv1-all': 'LV1 Allemand',
	        'lv1-all-euro': 'LV1 Allemand Euro',
	        'lv1-por': 'LV1 Portugais',
	        'lv1-por-euro': 'LV1 Portugais Euro',
	        'lv1-it': 'LV1 Itlien',
	        'lv1-it-euro': 'LV1 Itlien Euro',
	        'lv1-chi': 'LV1 Chinois',
	        'lv1-ru': 'LV1 Russe',
	        'lv1-ara': 'LV1 Arabe',
	        # LV2
	        'lv2-ang': 'LV2 Anglais',
	        'lv2-esp': 'LV2 Espagnol',
	        'lv2-all': 'LV2 Allemand',
	        'lv2-por': 'LV2 Portugais',
	        'lv2-it': 'LV2 Italien',
	        'lv2-chi': 'LV2 Chinois',
	        'lv2-ru': 'LV2 Russe',
	        'lv2-ara': 'LV2 Arabe',
	        # Spés
	        'spe-art': 'Spé Arts',
	        'spe-hggsp': 'Spé HGGSP',
	        'spe-hlp': 'Spé HLP',
	        'spe-ses': 'Spé SES',
	        'spe-maths': 'Spé Mathématiques',
	        'spe-pc': 'Spé Physique-Chimie',
	        'spe-svt': 'Spé SVT',
	        'spe-nsi': 'Spé NSI',
	        'spe-si': 'Spé Sciences de l\'Ingénieur',
	        'spe-lca': 'Spé LCA',
	        'spe-llcer-ang': 'Spé LLCER Anglais',
	        'spe-llcer-esp': 'Spé LLCER Espagnol',
	        'spe-llcer-all': 'Spé LLCER Allemand',
	        'spe-llcer-it': 'Spé LLCER Italien',
	        'spe-bio-eco': 'Spé Biologie-écologie',
	        # Options
	        'opt-lca-latin': 'LCA Latin',
	        'opt-lca-grec': 'LCA Grec',
	        'opt-lv3-ang': 'LV3 Anglais',
	        'opt-lv3-esp': 'LV3 Espagnol',
	        'opt-lv3-all': 'LV3 Allemand',
	        'opt-lv3-por': 'LV3 Portugais',
	        'opt-lv3-it': 'LV3 Italien',
	        'opt-lv3-ru': 'LV3 Russe',
	        'opt-lv3-ara': 'LV3 Arabe',
	        'opt-lv3-chi': 'LV3 Chinois',
	        'opt-eps': 'Option EPS',
	        'opt-arts': 'Option Arts',
	        'opt-musique': 'Option Musique',
	        'opt-mg': 'Option Management et Gestion',
	        'opt-ss': 'Option Santé et Social',
	        'opt-biotech': 'Option Biotechnologies',
	        'opt-sl': 'Option Sciences et laboratoire',
	        'opt-si': 'Option Sciences de l\'Ingénieur',
	        'opt-cit': 'Option Création et culture technologiques',
	        'opt-ccd': 'Option Création et culture - design',
	        'opt-equit': 'Option Hippologie et équitation',
	        'opt-aet': 'Option Agranomie-économie-territoires',
	        'opt-psc': 'Option Pratiques sociales et culturelles',
	        'opt-maths-comp': 'Option Maths Complémentaires',
	        'opt-maths-exp': 'Option Maths Expertes',
	        'opt-dgemc': 'Option Droits et grands enjeux du monde contemporain',
	        #
	        'none': ''
		}

		for a in toTranslate:
			if translated != '' and a != 'none':
				translated += ' / '
			translated += translations[a]

		return translated

class Utilisateur(Translate_matiere_spes_options_lv, Actions):
	def __init__(self, params: dict):
		self._id = params['_id']
		self.idENT = params['idENT']
		self.nom = params['nom']
		self.prenom = params['prenom']
		self.pseudo = params['pseudo']
		self.nomImg = params.get('nomImg')
		self.imgProfile = params.get('imgProfile', '')
		self.dateInscription = params['dateInscription']
		self.birth_date = params.get('birth_date')
		self.classe = params.get('classe', '')
		self.lycee = params['lycee']
		self.spes = params.get('spes', [])
		self.langues = params.get('langues', [])
		self.options = params.get('options', [])
		self.couleur = params['couleur']
		self.type = params['type']
		self.elementPublic = params['elementPublic']
		self.elementPrive = params['elementPrive']
		self.caractere = params.get('caractere')
		self.email = params.get('email', '')
		self.interets = params.get('interets', '')
		self.telephone = params.get('telephone', '')
		self.sign = params.get('sign', [])
		self.Sanctions = params.get('Sanction', [])
		self.SanctionEnCour = params['SanctionEnCour']
		self.SanctionDuree = params.get('SanctionDuree', '')
		self.xp = params['xp']
		self.xpModeration = params.get('xpModeration', 0)
		self.motif = params.get('motif', [])
		self.admin = params.get('admin', False)

		self.db_table = DB.db_utilisateurs

	def toDict(self):
		return {  # on ajoute à la liste ce qui nous interesse
	        '_id': self._id,
	        'idENT': self.idENT,
	        'nom': self.nom,
	        'prenom': self.prenom,
	        'pseudo': self.pseudo,
	        'nomImg': self.nomImg,
	        'imgProfile': self.imgProfile,
	        'dateInscription': self.dateInscription,
	        'birth_date': self.birth_date,
	        'classe': self.classe,
	        'lycee': self.lycee,
	        'spes': self.spes,
	        'spes-str': self.translate_matiere_spes_options_lv(self.spes),
	        'langues': self.langues,
	        'langues-str': self.translate_matiere_spes_options_lv(self.langues),
	        'options': self.options,
	        'options-str': self.translate_matiere_spes_options_lv(self.options),
	        'matieres': self.getUserSubjects(),
	        'couleur': self.couleur,
	        'type': self.type,
	        'elementPublic': self.elementPublic,
	        'elementPrive': self.elementPrive,
	        'caractere': self.caractere,
	        'email': self.email,
	        'interets': self.interets,
	        'telephone': self.telephone,
	        'sign': self.sign,
	        'Sanctions': self.Sanctions,
	        'SanctionEnCour': self.SanctionEnCour,
	        'SanctionDuree': self.SanctionDuree,
	        'xp': self.xp,
	        'xpModeration': self.xpModeration,
	        'motif': self.motif,
	        'admin': self.admin,
	        'a_sign': self.aSign()
	    }

	def toDB(self) -> dict:
		return {  # on ajoute à la liste ce qui nous interesse
	        '_id': self._id,
	        'idENT': self.idENT,
	        'nom': self.nom,
	        'prenom': self.prenom,
	        'pseudo': self.pseudo,
	        'nomImg': self.nomImg,
	        'imgProfile': self.imgProfile,
	        'dateInscription': self.dateInscription,
	        'birth_date': self.birth_date,
	        'classe': self.classe,
	        'lycee': self.lycee,
	        'spes': self.spes,
	        'langues': self.langues,
	        'options': self.options,
	        'couleur': self.couleur,
	        'type': self.type,
	        'elementPublic': self.elementPublic,
	        'elementPrive': self.elementPrive,
	        'caractere': self.caractere,
	        'email': self.email,
	        'interets': self.interets,
	        'telephone': self.telephone,
	        'sign': self.sign,
	        'Sanction': self.Sanctions,
	        'SanctionEnCour': self.SanctionEnCour,
	        'SanctionDuree': self.SanctionDuree,
	        'xp': self.xp,
	        'xpModeration': self.xpModeration,
	        'motif': self.motif,
	        'admin': self.admin
	    }

	def recupLevel(self):
		niv = int(0.473*self.xp**0.615)
		xplvl = int((0.473*self.xp**0.615-niv)*100)

		return niv, xplvl, self.xp

	def getUserSubjects(self):
	    subjects = ['hg', 'emc', 'eps']

	    # Tronc commun
	    if self.classe == '2GT' or self.classe == '1G':
	        subjects.append('fr')
	    if self.classe == '2GT':
	        subjects.append('maths')
	        subjects.append('pc')
	        subjects.append('ses')
	    if self.classe == 'TG':
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
	    # Spés + options
	    subjects += self.spes
	    subjects += self.options

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
		if diffTemps // (60 * 60 * 24 * 7): # semaines
			tempsStr += '{}sem '.format(diffTemps // (60 * 60 * 24 * 7))
			if (diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24): # jours
				tempsStr += '{}j '.format((diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24))
		elif diffTemps // (60 * 60 * 24): # jours
			tempsStr += '{}j '.format(diffTemps // (60 * 60 * 24))
			if (diffTemps % (60 * 60 * 24)) // (60 * 60): # heures
				tempsStr += '{}h '.format((diffTemps % (60 * 60 * 24)) // (60 * 60))
		elif diffTemps // (60 * 60):  # heures
			tempsStr += '{}h '.format(diffTemps // (60 * 60))
			if (diffTemps % (60 * 60)) // 60: # minutes
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

	def toDict(self) -> dict:
		return {  # on ajoute à la liste ce qui nous interesse
			'_id': self._id,
	        'idMsg': self._id,
	        'idAuteur': self.id_utilisateur,
	        'titre': self.titre,
	        'contenu': self.contenu,
	        'date-envoi': self.date_envoi,
	        'temps': self.convertTime(),
	        'tag-matière': self.matiere,
	        'matière': self.translate_matiere_spes_options_lv([self.matiere]),
	        'likes': self.likes,
	        'nb-likes': len(self.likes),
	        'réponses associées': [r.toDict() for r in self.reponses_associees.values()],
	        'reponsesDict': {idRep: rep.toDict() for (idRep, rep) in self.reponses_associees.items()},
	        'reponsesObjects': self.reponses_associees,
	        'a_like': self.aLike(),
	        'a_sign': self.aSign(),
	        'sign': self.sign,
	        'motif': self.motif,
	        'resolu': self.resolu,
	        'fileType' : self.fileType,
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
	        'fileType' : self.fileType
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

	def toDict(self) -> dict:
		return {
			'_id': self._id,
			'idRep': self._id,
	        'id-utilisateur': self.id_utilisateur,
	        'contenu': self.contenu,
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
		self.sign = params.get('sign', [])
		self.motif = params.get('motif', [])

		self.db_table = DB.db_messages

	def toDict(self) -> dict:
		return {  # on ajoute à la liste ce qui nous interesse
	        '_id': self._id,
	        'id-groupe': self.id_groupe,
	        'id-utilisateur': self.id_utilisateur,
	        'contenu': self.contenu,
	        'date-envoi': self.date_envoi,
	        'reponse': self.reponse,
	        'audio': self.audio,
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
	        'sign': self.sign,
	        'motif': self.motif
	    }

	def __str__(self):
		return str(self.toDict())

class Groupe(Actions):
	def __init__(self, params: dict):
		self._id = params['_id']
		self.nom = params['nom']
		self.id_utilisateurs = params['id-utilisateurs']
		self.moderateurs = params.get('moderateurs', [])
		self.sign = params.get('sign', [])
		self.motif = params.get('motif', [])

		self.db_table = DB.db_groupes

	def toDict(self) -> dict:
		return {  # on ajoute à la liste ce qui nous interesse
	        '_id': self._id,
	        'nom': self.nom,
	        'id-utilisateurs': self.id_utilisateurs,
	        'moderateurs': self.moderateurs,
	        'sign': self.sign,
	        'motif': self.motif
	    }

	def toDB(self) -> dict:
		return {  # on ajoute à la liste ce qui nous interesse
	        '_id': self._id,
	        'nom': self.nom,
	        'id-utilisateurs': self.id_utilisateurs,
	        'moderateurs': self.moderateurs,
	        'sign': self.sign,
	        'motif': self.motif
	    }

	def __str__(self):
		return str(self.toDict())


class Notification(Actions):
	def __init__(self, params: dict):
		self._id = params['_id']
		self.type = params['type']
		self.id_groupe = params['id_groupe']
		self.id_msg = params['id_msg']
		self.date = params['date']
		self.destinataires = params['destinataires']
		self.db_table = DB.db_notif

	def diffTemps(self):
		diff_temps = int((datetime.now() - self.date).total_seconds())
		return diff_temps

	def convertTime(self):
		tempsStr = ''
		diffTemps = self.diffTemps()
		# puis on se fait chier à trouver le délai entre le poste et aujourd'hui
		if diffTemps // (60 * 60 * 24 * 7): # semaines
			tempsStr += '{}sem '.format(diffTemps // (60 * 60 * 24 * 7))
			if (diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24): # jours
				tempsStr += '{}j '.format((diffTemps % (60 * 60 * 24 * 7)) // (60 * 60 * 24))
		elif diffTemps // (60 * 60 * 24): # jours
			tempsStr += '{}j '.format(diffTemps // (60 * 60 * 24))
			if (diffTemps % (60 * 60 * 24)) // (60 * 60): # heures
				tempsStr += '{}h '.format((diffTemps % (60 * 60 * 24)) // (60 * 60))
		elif diffTemps // (60 * 60):  # heures
			tempsStr += '{}h '.format(diffTemps // (60 * 60))
			if (diffTemps % (60 * 60)) // 60: # minutes
				tempsStr += '{}min '.format(diffTemps % (60 * 60) // 60)
		else:
			tempsStr = '{}min'.format(diffTemps // 60)

		return tempsStr

	def toDict(self) -> dict:
		if self.type == 'msg':
			grp = groupes[str(self.id_groupe)].toDict()
			msg = messages[str(self.id_msg)].toDict()
		elif self.type == 'demande':
			grp = demandes_aide[str(self.id_groupe)].toDict()
			msg = grp['reponsesDict'][str(self.id_msg)]
		sender = utilisateurs[str(msg['id-utilisateur'])].toDict()
		return {  # on ajoute à la liste ce qui nous interesse
			'_id': self._id,
	        'type': self.type,
	        'id_groupe': self.id_groupe,
			'groupe' : grp,
	        'id_msg': self.id_msg,
			'message' : msg,
			"sender": sender,
			'date': self.date,
	        'temps': self.convertTime(),
	        'destinataires': self.destinataires,
	        'userDest': [utilisateurs.get(str(destinataire)).toDict() for destinataire in self.destinataires]
	    }

	def toDB(self) -> dict:
		return {  # on ajoute à la liste ce qui nous interesse
	        '_id': self._id,
	        'type': self.type,
	        'id_groupe': self.id_groupe,
	        'id_msg': self.id_msg,
	        'date-date': self.date,
	        'destinataires': self.destinataires
	    }

	def __str__(self):
		return str(self.toDict())
