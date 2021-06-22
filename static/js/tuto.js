var num = 2;
var imageMax = 6;
var lien = "/";
var textes = "Après votre première connexion sur le site vous trouverez, sur la page d'accueil, les dernières questions postées sur le site.";
var titre = "1. Accueil";
var x = setInterval(function() {
  if (num == 2) {
    lien = "/";
    textes = "Les matière définissent les questions que vous souhaitez voir. Si l'on ne veut voir que les questions de français, on décoche donc toutes les matières qui ne nous intéressent pas.";
    titre = "2. Filtrer les demandes d'aide";
  }
  if (num == 3) {
    lien = "/question";
    textes = 'Pour poser une question, rien de plus simple ! Cliquer sur "Poser une question" et une interface vous sera proposée. Il suffit de remplir l\'objet de votre question ainsi que le détail afin que la communauté vous aide au mieux. Si vous avez une photo du problème n\'hésitez pas à l\'ajouter en cliquand sur "Fichier".';
    titre = "3. Poser une question";
  }
  if (num == 4) {
    lien = "/messages/60c5ad88186fbabb20bb2a7e/";
    textes = "Dans le menu déroulant à droite de votre écran, vous trouverez l'onglet \"Messages privés\". En appuyant sur le \"+\" vous pouvez chercher d'autres utilisateurs afin de débuer une conversation avec eux. Vous pouvez également envoyer des messages vocaux.";
    titre = "4. Les messages privés";
  }
  if (num == 5) {
    lien = "/profil";
    textes = "Sur votre profil vous pouvez renseigner vos informations comme votre pseudo, vos langues vivantes, votre adresse mail, votre numéro de téléphone, bien évidemment vous pouvez choisir de les rentre publiques ou non.";
    titre = "5. Votre Profil";
  }
  if (num == 6) {
    lien = "/XP_tuto";
    textes = "Le système d'XP permet de récomprenser votre contribution sur le site. Il vous permet de débloquer des récompenses uniques en fonction de votre niveau, comme par exemple un large choix de thème pour le site lui même. Vos récompenses ainsi que votre niveau apparaissent sur votre page de profil ";
    titre = "6. Le système d'XP";
  }
})

function suivant() {
  num += 1;
  if (num == imageMax+1) {
    document.getElementById("next").style.display = "none";
    document.getElementById("fini").style.display = "block";
  }
  document.getElementById("iframTuto").src = lien;
  document.getElementById("texte").innerText = textes;
  document.getElementById("titre").innerText = titre;
  document.getElementById("progressTuto").value = num-1;
}

function precedent() {
  num -= 1;
  if (num == 0) {
    num = 1;
  }
  if (num == imageMax+1) {
    document.getElementById("next").style.display = "block";
    document.getElementById("fini").style.display = "none";
  }
  document.getElementById("iframTuto").src = lien;
  document.getElementById("texte").innerText = textes;
  document.getElementById("titre").innerText = titre;
  document.getElementById("progressTuto").value = num-1;
}

function touche(e) {
  var touche = event.keyCode;
  if (touche == 37) {
    precedent();
  } else if (touche == 39) {
    suivant();
  }
}
