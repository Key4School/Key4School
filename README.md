# CTL 2021 : Key4School <img src="https://github.com/Key4School/Key4School/blob/main/static/image/logo/favicon.png" width=40 >

## Utilisation

1. `npm install`
2. `pip install -r requirements.txt`
3. `python main.py`

## I - Introduction :

Notre volonté est de réunir les lycéens sur un réseau social centré sur l'entre-aide et le partage de la connaissance. Pour cela celui-ci est divisé en deux parties : une partie forum destinée à l'échange entre tous les élèves de la région, peu importe le lycée, l'académie ou le département ; la seconde, les messages privés, étant plutôt concentrés sur l'échange avec des personnes proches. Notre site se veut cependant concentré sur le scolaire : les demandes d'aides sont faites par matière et le but est de rester le plus possible sur des sujets en lien avec le lycée. Cependant la partie messages privés est beaucoup plus libre. On peut discuter avec les personnes de son choix sur les thèmes que l'on veut. Le côté scolaire de cette partie du site étant assuré par la création automatique de groupes classes permettant une communication plus aisée entre élèves.



## II - Répartition du site :

* page d'accueil : https://key4school.herokuapp.com/
* page de messages privés : https://key4school.herokuapp.com/messages/
* page de profil : https://key4school.herokuapp.com/profil/
* page de demandes enregistrées : https://key4school.herokuapp.com/saved/
* page de tutoriel : https://key4school.herokuapp.com/help/
* page d'administration (accès restreint aux administrateurs du site) : https://key4school.herokuapp.com/administration/
* page de recherche : https://key4school.herokuapp.com/recherche/?search=VotreRecherche
* page de question : https://key4school.herokuapp.com/question/
* page de commentaire : https://key4school.herokuapp.com/comments/idDuGroupe

### Fonctionnalités par page :

* Page d'accueil :

	* Affichage des demandes d'aide selon un référencement (nombre de likes et de commentaires).
	* Filtrage des demandes d'aide par matière en haut de la page.
	* Possibilité de liker une demande : icône "pouce vers le haut"
	* Possibilité de signaler une demande : bouton "signaler"
	* Possibilité d'enregistrer une demande : icône "marque page"
	* Possibilité d'accès à la page des commentaires/réponses : icône "bulle"
	* Système de scroll infini : toutes les demandes ne sont pas chargées d'un seul coup, elles se chargent au fur et à mesure du scroll.
	* Demandes d'aides : affichage du titre, de l'auteur, de la date de mise en ligne, de la matière, du contenu avec les pièces jointes si besoin, du nombre de likes, de commentaires.

* Page de messages privés :

	* Chat en direct :
		* Echange de texte, d'audio et d'image.
	* Affichage de tous les groupes de l'utilisateur.
	* Possibilité de filtrer les groupes.
	* Possibilité de créer un groupe avec filtre des utilisateurs.
	* Affichage des messages :
		* Séparation entre messages de l'utilisateur (à droite, couleur blanche) et des autres (à gauche, couleur en fonction du thème de l'utilisateur).
		* Affichage du pseudo de l'utilisateur (lien vers son profil en cliquant dessus).
		* Flèche vers le bas :
			* menu déroulant avec possibilité de signaler un message ou d'y répondre.
		* Trois petits points verticaux :
			* Options du groupe pour tous :
				* Aperçu du profil de chaque membre du groupe.
				* Possibilité de signaler le groupe.
				* Possibilité de quitter le groupe.
			* Options administrateur du groupe (par défaut : le créateur) :
				* Renommer le groupe.
				* Modifier le rôle dans le groupe pour chaque participant.
				* Ajouter des participants.
				* Possibilité de supprimer le groupe.
				* Possibilité d'activer ou désactiver l'automoderation sur le chat.
		* En haut affichage des participants du groupe par pseudo.
		* Barre de saisie de messages :
			* Affichage du message auquel on répond.
			* Icône "microphone" : enregistrement de messages vocaux avec possibilité de l'envoyer ou de le supprimer.
			* Icône "image" : possibilité d'envoyer une image.

* Page de profil :

	* Page personnelle :
		* Affichage des informations personnelles.
		* Possibilité de modifier sa photo de profil.
		* Possibilité de modifier certains champs : Pseudo, langues vivantes, spécialités, options, centres d'intérêts, adresse mail, téléphone, date de naissance, caractère.
		* Possibilité de modifier la visibilité de certaines informations (privé/public).
		* Choisir ses notifications (mails ...).
		* Modifier son thème (certains thèmes sont bloqués en fonction de l'xp de l'utilisateur).
		* Aperçu de ses dernières demandes d'aide.
		* Récapitulatif des sanctions de l'utilisateur.
		* Tous les champs modifiables sont soumis à l'auto-modération.
	* Page d'un autre utilisateur :
		* Affichage de toutes les informations publiques dont l'xp.
		* Possibilité de signaler le profil.
		* Possibilité de démarrer une discussion avec la personne.
		* Voir si la personne a le statut d'administrateur.

* Page de demandes enregistrées :

	* Affichage de toutes les demandes enregistrées par l'utilisateur afin de les retrouver plus vite.
	* Demandes d'aide : affichage du titre, de l'auteur, de la date de mise en ligne, de la matière, du contenu avec les pièces jointes si besoin, du nombre de likes, de commentaires.

* Page de tutoriel :

	* Mini tutoriel en 9 points expliquant rapidement le fonctionnement du site.

* Page d'administration :

	* Page réservée aux administrateurs du site.
	* Possibilité de visualiser toutes les demandes d'aide, tous les commentaires, les profils, les messages privées, et toutes les discussions signalées.
	* Possibilité de valider ou de supprimer chaque signalement.

* Page de recherche :

	* Accès via la barre de recherche.
	* Affichage de demandes d'aide par pertinence par rapport à la recherche.
	* Affichage de l'aperçu de quelques profils les plus pertinents avec possibilité d'en afficher plus.
	* Demandes d'aide : affichage du titre, de l'auteur, de la date de mise en ligne, de la matière, du contenu avec les pièces jointes si besoin, du nombre de likes, de commentaires.

* Page de question :

	* Page pour publier une demande d'aide.
	* Possibilité de mettre une pièce jointe (image ou pdf).
	* Mise en page de manière à donner un aperçu de la demande.

* Page de commentaires :

	* Affichage (en haut) de la demande d'aide avec toutes ses informations.
	* Champ de réponse pour poster un commentaire.
	* Affichage de tous les commentaires par date de publication.
	* Possibilité de liker ou de signaler un commentaire.



## III - Rôles dans le site :

* Rôles principaux:
	* Utilisateur : Rôles de toute personne lambda, aucun droit particulier.
	* Administrateur du site :
		* Peut supprimer toute demande, discussion, commentaire ou message qu'il juge inapproprié.
		* A accès à la page modération.
		* Peut valider ou supprimer tous les signalements.
		* Peut sanctionner tout utilisateur.
		* A accès au "casier judiciaire" de l'utilisateur *(historique de ses sanctions)*.

* Sanctions :
	* Mode Spectateur sur tout le site
	* Mode Spectateur sur le forum
	* Mode Spectateur sur les messages privés
	* Interdiction de modifier le profil
	* Réinitialisation du profil


* Rôles scolaires :
	* Elève : Aucun droit particulier.
	* Enseignant :
		* Dans les discussions privées :
			* Peut supprimer tous les messages des discussions dont il fait partie.
			* Peut activer l'auto-modération dans les discussions auxquelles il appartient.

* Rôles dans les discussions privées :
	* Participant : aucun droit particulier.
	* Administrateur d'une discussion :
		* Peut ajouter et enlever des participants.
		* Changer le rôle des participants.
		* Peut supprimer le groupe.
		* Peut activer l'auto modération dans les discussions auxquelles il appartient.

* Système d'xp :
	* Chaque utilisateur possède un nombre d'xp.
	* L'utilisateur gagne de l'xp pour :
		* chaque like qu'il reçoit.
		* chaque demande qu'il poste.
		* chaque commentaire qu'il poste.
	* Plus l'utilisateur a d'xp plus il monte en niveau.
	* Monter en niveau permet de débloquer :
		* De nouvelles palettes.
		* De nouveaux thèmes.

## IV - Notifications :

* Notifications pour :
	* Nouveau message dans un groupe de l'utilisateur.
	* Commentaire sur une demande de l'utilisateur.
	* Commentaire sur une demande enregistrée par l'utilisateur.
* Notifications :
	* Sur le bandeau du site à icône "cloche" :
		* Affichage du nombre de notifications plus affichage de toutes les notifications.
		* Possibilité de tout marquer comme lu.
	* Par mail *(pas encore intégré)*:
		* Mail personnalisé aux couleurs du site.
	* Sonore :
		* Lorsque l'on navigue sur le site.



## V - Innovations techniques :

* Backend :

	* Développement en Programmation Orientée Objet (POO) :
		* Allègement du code.
		* Stockage en cache : réduction des échanges avec la DB => optimisation des temps de chargement.

	* Utilisation de websockets sécurisés permettant une interaction direct avec le serveur notamment dans les messages privées.

	* Auto-modération :
		* Plus de 3 000 mots et expressions bannis.
		* Effective sur toutes les entrées publiques.
		* Implémentation optionelle sur les messages privés afin de garder un côté décontracté (possibilité de l'ajouter soi-même).

	* Scroll infini	:
		* Déploiment sur les discussions des messages privés et sur la page d'accueil et la page recherche pour les demandes d'aide.
		* Optimisation des temps de chargement.

	* Référencement :
		* Mise en valeur des demandes d'aide par :
			* le nombre de likes :
				* Plus une demande a de likes, plus il y a de gens qui ont besoin de la même aide.
				* Plus une demande a de likes, plus elle est mise en avant.
			* le nombre de commentaires :
				* Plus une demande a de commentaires, plus il y a de chances qu'un d'eux répondent à la question.
				* Plus une demande a de commentaires, moins elle est mise en avant.
		* Le référencement n'est pas basé sur la date de publication :
			* Pour éviter que des questions ne soient jamais répondues.
			* Pour éviter que les utilisateurs posent en boucle la même question si celle-ci n'a pas été répondue.

	* Site obligatoirement en HTTPS pour une sécurité optimale.

	* Création de groupes classes :
		* Chaque classe a son groupe dédié. 
		* A sa première connection l'utilisateur est rattaché automatiquement au groupe de sa classe.
		* Il est impossible pour l'utilisateur de quitter son groupe classe.
		* A la première connection si l'utilisateur est le premier de sa classe à se connecter au site, un groupe pour sa classe est automatiquement créé.


* Frontend :
	* Site responsive :
		* l'entièreté du site est responsive.
		* adapté pour téléphone.


* User Experience :
	* Système d'xp.
	* De nombreux thèmes sont à venir (notamment thème de saison et par matière). Ils seront déblocables par niveaux.


## VI - En cours de développement :

* Notifications par mail en cours de développement (on veut faire un style personnalisé mais nous n'avons pas encore eu le temps puisqu'on ne peut pas utiliser Bulma).
* De nombreux thèmes devraient arriver dans les prochaines semaines.
* Ajout d'un leaderbord avec récompense pour ceux ayant gagné le plus d'xp.
