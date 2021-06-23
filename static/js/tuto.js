var page = 0;
var imageMax = 5;

var data = [
  {
    'texte': "Après votre première connexion sur le site vous trouverez, sur la page d'accueil, les dernières questions postées sur le site.",
    'titre': "1. Accueil",
    'lien': "/"
  },
  {
    'texte': "Les matière définissent les questions que vous souhaitez voir. Si l'on ne veut voir que les questions de français, on décoche donc toutes les matières qui ne nous intéressent pas.",
    'titre': "2. Filtrer les demandes d'aide",
    'lien': "/"
  },
  {
    'texte': 'Pour poser une question, rien de plus simple ! Cliquez sur "Poser une question" et une interface vous sera proposée. Il suffit de remplir l\'objet de votre question ainsi que le détail afin que la communauté vous aide au mieux. Si vous avez une photo du problème n\'hésitez pas à l\'ajouter en cliquant sur "Fichier".',
    'titre': "3. Poser une question",
    'lien': "/question/"
  },
  {
    'texte': "Dans le menu déroulant à droite de votre écran, vous trouverez l'onglet \"Messages privés\". En appuyant sur le \"+\" vous pouvez chercher d'autres utilisateurs afin de débuter une conversation avec eux. Vous pouvez également envoyer des messages vocaux.",
    'titre': "4. Les messages privés",
    'lien': "/messages/"
  },
  {
    'texte': "Sur votre profil vous pouvez renseigner vos informations comme votre pseudo, vos langues vivantes, votre adresse mail, votre numéro de téléphone, bien évidemment vous pouvez choisir de les rendre publiques ou non.",
    'titre': "5. Votre Profil",
    'lien': "/profil/"
  },
  {
    'texte': "Le système d'XP permet de récompenser votre contribution sur le site. Il vous permet de débloquer des récompenses uniques en fonction de votre niveau, comme par exemple un large choix de thèmes pour le site lui-même. Vos récompenses ainsi que votre niveau apparaissent sur votre page de profil ",
    'titre': "6. Le système d'XP",
    'lien': "/XP_tuto/"
  }
]

function update(){
  document.getElementById("iframTuto").src = data[page].lien;
  document.getElementById("texte").innerText = data[page].texte;
  document.getElementById("titre").innerText = data[page].titre;
  document.getElementById("progressTuto").value = page+1;
}

function suivant() {
  page += 1;
  if (page > 5) {
    page = 5;
  }
  if (page == imageMax) {
    document.getElementById("next").style.display = "none";
    document.getElementById("fini").style.display = "block";
  }
  update();
}

function precedent() {
  page -= 1;
  if (page < 0) {
    page = 0;
  }
  if (page == imageMax-1) {
    document.getElementById("next").style.display = "block";
    document.getElementById("fini").style.display = "none";
  }
  update();
}

function touche(e) {
  var touche = event.keyCode;
  if (touche == 37) {
    precedent();
  } else if (touche == 39) {
    suivant();
  }
}
