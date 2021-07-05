**diapo 1**

* Logo Key4school avec nom du site. On peut rajouter les noms des peronnes du groupe.

**diapo 2**

* Titre : présentation de Key4School.

* txt à dire :
  * Notre volonté est de réunir les lycéens sur un réseau social centré sur l'entre-aide et le partage de la connaissance. Pour cela celui-ci est divisé en deux parties : une partie forum destinée à l'échange entre tous les élèves de la région, peu importe le lycée, l'académie ou le département ; la seconde, les messages privés, étant plutôt concentrés sur l'échange avec des personnes proches. Notre site se veut cependant concentré sur le scolaire : les demandes d'aides sont faites par matière et le but est de rester le plus possible sur des sujets en lien avec le lycée. Cependant la partie messages privés est beaucoup plus libre. On peut discuter avec les personnes de son choix sur les thèmes que l'on veut. Le côté scolaire de cette partie du site étant assuré par la création automatique de groupes classes permettant une communication plus aisée entre élèves. Nous avons fait ce choix car il existe déjà beaucoup de réseaux sociaux de divertissements et assez peu d'entre-aide. Nous pensons donc que Key4School sera un réseau social utile aux lycéens.

* sur la diapo :
 * Réunir les lycéens sur un réseau social d'entre-aide.
 * Forum pour échanger avec l'ensemble des lycéens de la région.
 * Messages privés pour l'échange avec des personnes proches.
 * Site concentrés sur le scolaire :
  * Forum de demandes d'aide par matière et sujet en lien avec le lycée.
  * Messages privés avec création automatique de groupes classe.


**diapo 3**

* Titre : Répartition du travail.

* Sur la diapo :
  * répartition en trois groupes : backend, frontend, et UX.
  * frontend :
    * languages utilisés : HTML/CSS/JS.
    * côté visuel du site.
  * backend :
    * languages utilisés : Python.
    * côté serveur du site.
    * gestion de la db.
    * optimisation du site.
  * UX :
    * profil.
    * système d'xp.
    * récompenses.
    * thèmes pour le site.

**Démonstration sur le site** ( on quitte le ppt)

* Page d'accueil :
  * passage rapide (le jury connait)
  * likes, commentaires, signalement, apercu de profil, enregistrement.
  * filtre par matière.

* Page poser une question :
  * passage rapide (le jury connait)
  * choix de la matière, du titre, du contenu, de la pièce jointe (pdf ou img), envoyer ou annuler.

* Page de recherche :
  * passage rapide (le jury connait)
  * affichage des recherches les plus pertinentes.
  * affichage de quelque profil correspondant avec possibilité d'en afficher plus.

* page de demandes enregistrés :
  * passage rapide (le jury connait).

* page de commentaires :
  * passage rapide (le jury connait).
  * envoi de réponse et affichage de tous les commentaires.

* page de messages privés :
  * passage rapide (le jury connait).
  * affichage des groupes par date du dernier msg.
  * création de nouveaux groupes :
    * filtre d'utilisateurs et choix du nom du groupe.
  * sur le groupe :
    * envoi de msg txt, audio image et lien.
    * options du groupe :
      * si utilisateur admin :
        * possibilité de modérer le grp.
        * changer le rôle des participants, ou les retirer du grp.
        * changer le nom du grp.
        * fermer le grp.
        * ajouter des participants.
  * filtre des grp par nom et utilisateurs.

* page de profil :
  * passage rapide (le jury connait).
  * modifier infos perso, visibilité, photo de profil, thème.
  * affichage de l'xp.
  * choix des notifications.
  * affichage des demandes d'aides.
  * casier judiciaire.

  * autre utilisateur :
    * affichage de l'xp, de toutes les info publiques.
    * Si admin affichage du casier judiciaire.
    * possibilité de démarrer un conversation privée avec cet utilisateur.

* page de tuto :
  * passage rapide (le jury connait).

* responsive :
  * demo du responsive avec l'outils dev du navigateur.

**diapo 4** (retour au ppt)

* Titre : administration

* auto-moderation :
  * + de 3500 mots et expression bannis.
  * appliquée sur toutes les entrées publiques du site.
  * possibilité de l'appliquer sur les messages privés (au choix des administrateurs de la discussion)
* administrateurs :
  * page réservé.
  * peuvent voir toutes les demandes d'aides, les utilisateurs, et les discussions signalés.
  * peuvent valider ou supprimer tous signalement.
  * peuvent sanctionner les utilisateurs.
* casier judiciaire :
  * l'historique des sanctions d'un utilisateur est conservé.
  * affiché sur la page profil et visible par l'utilisateur et les administrateurs.
* sanction :
  * du simple avertissement au mode spectateur.
  * pas de ban définitif.


**diapo 5**

* Titre : notifications

* forme de notifications :
  * onglet notification dans le bandeau du site.
  * notifications sonore quand l'utilisateur est sur le site (au choix de l'utilisateur).
  * notification par mail (au choix de l'utilisateur).. (inclure un screenshot d'un exemple de mail)
  * modification de l'icône du site.
* Notifications pour :
  * nouveaux messages privés.
  * commentaire sur une demande de l'utilisateur ou enregistrée.



**diapo 6**

* Titre : Programmation Orientée Objet.

(mettre un sreenshot du code)

* allègement du code :
  * un code plus esthétique.
  * attributs et méthodes permettant de simplifier le reste du code.
  * utilisation d'objets pour tous les éléments stockés dans la db.
* optimisation :
  * stockage des objets en cache.
  * accès plus rapide.
  * réduction des temps de chargement.
  * limitation des échanges avec la db.

**diapo 7**

* Titre : Référencement et algorithme de tri.

* But :
  * présenter à l'utilisateur les demandes auxquelles il sera le plus apte à répondre et qui auront besoin le plus de réponse.
  * affichage sur l'écran d'accueil d'uniquement les demandes d'aide des autres.
  * affichage uniquement des demandes d'aide sur les matières de l'utilisateur.
  * algorithme de tri basé sur le nombre de likes et de commentaire.

**diapo 8**

* Titre : Autres solutions Technique.

* Websocket :
  * échanges direct avec le serveur.
* Scroll infini :
  * optimisation des temps de chargement.
* https :
  * une sécurité accrue.
* création de groupe classe :
  * afin de retrouver facilement les personnes de son entourage.

**diapo 9**

* Titre : A venir prochainement dans Key4School :

* De nombreux nouveaux thèmes : (mettre les screenshots d'Estelle).
* Leaderboard des meilleurs xp.
* développement du site en version appli mobile et desktop.
