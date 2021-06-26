# CTL 2021 : Key4School

## I Introduction :

Notre volonté est de réunir les lycéens sur un réseau social centré sur l'entre-aide et le partage de la connaissance.
Pour cela celui-ci est divisé en deux parties : une partie forum destinée à l'échange entre tous les élèves de la région,
peut importe le lycée, l'académie ou le département, la seconde, les messages privés, étant plutôt concentrés sur l'échange avec des
personnes proches. Notre site se veut cependant concentré sur l'école : les demandes d'aides sont faites par matière et le but et de rester
le plus possible sur des sujets en lien avec le lycée. Cependant la partie messages privés et beaucoup plus libre. On peut discuter avec
les personnes de son choix sur les thèmes que l'on veut. Le côté scolaire de cette partie du site étant assuré par la création automatique de
groupe classe permettant une communication plus aisée entre élèves.



## II Répartition du site :

* page d'accueil : https://key4school.herokuapp.com/
* page de messages privés : https://key4school.herokuapp.com/messages/
* page de profil : https://key4school.herokuapp.com/profil/
* page de demandes enregistrées : https://key4school.herokuapp.com/saved/
* page de tutoriel : https://key4school.herokuapp.com/help/
* page d'administration (accès restreint aux administarteurs du site) : https://key4school.herokuapp.com/administration/
* page de recherche : https://key4school.herokuapp.com/recherche/?search=VotreRecherche
* page de question : https://key4school.herokuapp.com/question/
* page de commentaire : https://key4school.herokuapp.com/comments/idDuGroupe

### Fonctionnalités par page :

* Page d'accueil :

	* Affichage des demandes d'aides selon leur nombre de like et de commentaires.
	* Filtres des demandes d'aides par matière en haut de la page.
	* Possibilité de liker une demande : icône "pouce vers le haut"
	* Possibilité de signaler une demande : bouton "signaler"
	* Possibilité d'enregistrer une demande : icône "marque page"
	* Possibilité d'accès à la page commentaire : icône "bulle"
	* Système de scroll infini : toutes les demandes ne sont pas chargés d'un seul coup, elle se charge au fur et à mesure du scroll.
	* Demande d'aides : affichage du titre, de l'auteur, de la date de mise en ligne, de la matière, du contenu avec les pièces jointes si besoin, du nombre de likes, de commentaires.

* Page de messages privés:

	* Affichage de tous les groupes de l'utilisateur.
	* Possibilité de filtrer les groupes.
	* Possibilité de créer un groupe avec filtre des utilisateurs.
	* Affichage des messages :
		* Séparation entre messages de l'utilisateur (à droite, couleur blanche) et autre (à gauche, couleur en fonction du thème de l'utilisateur).
		* Affichage du pseudo de l'utilisateur (lien vers son profil en cliquant dessus).
		* Flèche vers le bas :
			* menu déroulant avec possibilité de signalé un message ou d'y répondre.
		* trois petits points verticaux :
			* Options du groupe pour tous :
				* Aperçu du profil de chaque membre du groupe.
				* Possibilité de signalé le groupe.
				* Possibilité de quitter le groupe.
			* Options administrateur du groupe (par défaut le créateur) :
				* Renommer le groupe.
				* Modifier le rôle dans le groupe de chaque participant.
				* Ajouter des participants.
				* Possibilité de supprimer le groupe.
		* En haut affichage des participants du groupe par pseudo.
		* Barre de saisi de messages :
			* Affichage du message auquel on répond.
			* icône "microphone" : enregistrement de messages vocaux avec possibilité de l'envoyer ou de le supprimer.

* Page de profil :

* Page personnelle :
	* Affichage des informations personnelles.
	* Possibilité de modifier sa photo de profil.
	* Possibilité de modifier certains champs : Pseudo, langues vivantes, spécialités, options, Centres d'intérêts, adresse mail, Téléphone, Date de Naissance, Caractère.
	* Possibilité de modifier la visibilité de certaines informations.
	* Choisir ses notifications.
	* Modifier son thème (certains thèmes sont bloqués en fonction de l'xp de l'utilisateur).
	* Aperçu de ses dernières demandes d'aide.
	* Récapitulatif des sanctions de l'utilisateurs.
	* Tous les champs modifiables sont soumis à l'auto-modération.
* Page des autres :
	* Affichage de toutes les informations publiques dont l'xp.
	* Possibilité de Signaler le profil.
	* Possibilité de démarrer une discussion avec la personne.
	* Voir si la personne est Administrateur.

* Page de demandes enregistrées :

	* Affichage de toutes les demandes enregistrés par l'utilisateur afin de les retrouver plus vite.
	* Demande d'aides : affichage du titre, de l'auteur, de la date de mise en ligne, de la matière, du contenu avec les pièces jointes si besoin, du nombre de likes, de commentaires.

* Page de tutoriel :

	* Mini tutoriel en 6 points expliquant rapidement le fonctionnement du site.

* Page d'administration :

	* Page réservée aux administrateurs du site.
	* Possibilité de visualiser tous les demandes d'aide, les commentaires, les profils, les messages privées, les discussions signalés.
	* Possibilité de valider ou de supprimer chaque signalement.

* Page de recherche :

	* Accès via la barre de recherche.
	* Affichage de demandes d'aide par pertinance par rapport à la recherche.
	* Affichage de l'aperçu de quelques profils les plus pertinants avec possibilité d'en afficher plus.
	* Demande d'aides : affichage du titre, de l'auteur, de la date de mise en ligne, de la matière, du contenu avec les pièces jointes si besoin, du nombre de likes, de commentaires.

* Page de question :

	* Page pour publier une demande d'aide.
	* Possibilité de mettre une pièce jointe (image ou pdf).
	* Mise en page de manière à donner un aperçu de la demande.

* Page de commentaire :

	* Affichage en haut de la demande d'aide avec toutes ses informations.
	* Champ de réponse pour poster un commentaire.
	* Affichage de tous les commentaires par date de publication.
	* Possibilité de liker ou de signaler un commentaire.



## III Rôles dans le site :

* Rôles principaux:
	* Utilisateur : Rôles de toute personne lambda, aucun droit particulier.
	* Administrateur du site : Peut supprimer toutes demandes, commentaires, discussion ou message qu'il juge inapproprié. A accès à la page modération. Peut valider ou supprimer tous les signalements. Peut sanctionner tout utilisateur.

* Sanctions :
	* Mode Spectateur sur tout le site
	* Mode Spectateur sur le forum
	* Mode Spectateur sur les messages privés
	* Interdiction de modifier le profil
	* Réinitialisation du profil


* Rôles scolaires :
	* Elève : Aucun droit particulier.
	* Enseignant : Dans les discussions privées, ils peuvent supprimer tous les messages des discussions dont ils font parti.

* Rôles dans les discussions privés :
	* Participant : aucun droit particulier.
	* Administrateur d'une discussion : peut ajouter et enlever des participants, changer le rôle des participants, peut supprimer le groupe.

* Système d'xp :
	* Chaque utilisateur possède un nombre d'xp.
	* L'utilisateur gagne de l'xp pour :
		* chaque like qu'il reçoit.
		* chaque demande qu'il poste.
		* chaque commentaire qu'il poste.
	* Plus l'utilisateur a d'xp plus il monte en niveau.
	* Monter en niveau permet de débloquer :
		*	De nouvelles palettes.
		* De nouveaux thèmes.

## VI Notifications :

	* Notifications pour :
		* Nouveaux Messages dans un groupe de l'utilisateur.
		* Commentaire sur une demande de l'utilisateur.
		* Commentaire sur une demande enregistrée par l'utilisateur.
	* Notifications :
		* Sur le bandeau du site icône "cloche" :
			* Affichage du nombre de notifications plus affichage de toutes les notifications.
			* Possibilité de tout marquer comme lu.
		* Par mail (par encore intégré):
			* Mail personnalisé aux couleurs du site.



## V Innovation technique :

	* Backend :
		* Développement en Programmation Orientée Objet :
			* Alègement du code.
			* Stockage en cache : réduction des échanges avec la DB : optimisation des temps de chargement.
		* Utilisation de socket permettant une interaction direct avec le serveur notamment dans les messages privées.
		* Auto-modération :
			* Plus de 3000 mots et expressions  bannis.
			* Effectif sur tout les inputs publiques.
			* Pas d'implémentation sur les messages privés afin de garder un côté décontracté.
		* Site responsive :
			* l'entièreté du site est responsive.
			* Adapté pour téléphone.


## V Probleme technique à régler :

	* Les PDF ne sont pas visualisable sur Heroku.
	* Notifications par mail en cours de développement (on voulait faire un style perso mais on a pas encore eu le temps puisqu'on ne peut pas utiliser bulma)
	*
