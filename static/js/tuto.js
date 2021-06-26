var page = 0;
var imageMax = 8;

var data = [
  {
    'texte': "Bienvenue sur key4school ! Nous sommes ravis de votre arrivée ! key4school est un réseau social développé par 12 lycéens d’Ile de France a destination des lycéens. L’objectif est d’y trouver de l’aide et de s’entraider facilement.",
    'titre': "1. Présentation", 
    'lien': "/"
  },
  {
    'texte': "Dès votre arrivée sur le site, vous êtes sur la page d’accueil où se trouvent les toutes dernières questions posées par d’autres membres. Les questions ne concernent uniquement les matières que vous étudiez, pour en sélectionner une en particulier vous pouvez utiliser les filtres en haut de page. Si en défilant vous tombez sur une question à laquelle vous pouvez répondre alors n’hésitez-pas, il vous suffit de cliquer sur la bulle en dessous ! ",
    'titre': "2. Accueil",
    'lien': "/"
  },
  {
    'texte': 'Quand vous avez une question à poser, vous pouvez dans un premier temps taper les mots-clés dans la barre de recherche et regarder s’il y en a déjà une qui y répond. Si vous ne trouvez pas votre réponse, vous n’avez qu’à cliquer sur « Poser une question » et remplir le formulaire qui vous ai donné. Vous pouvez également joindre un fichier comme un exercice par exemple. Essayez d’être poli et le plus clair possible. Une fois que vous estimez que vous avez obtenu réponse à votre question, vous n’avez plus qu’à la mettre en tant que résolue afin de fermer le sujet.',
    'titre': "3. Poser une question",
    'lien': "/question/"
  },
  {
    'texte': "En dessous de chaque question, vous avez la possibilité de l’enregistrer afin de pouvoir la retrouver dans la page correspondante accessible dans le menu en haut à droite. Cela vous permet ainsi soit d’y répondre plus tard soit d’être informé si elle est résolue par quelqu’un. ",
    'titre': "4. Demandes enregistrées",
    'lien': "/saved/"
  },
  {
    'texte': "Ils sont accessibles à partir du menu en haut à droite, vous pouvez créer des groupes avec le « + », envoyer des messages, des vocaux et même des images ! Vous retrouverez également de base un groupe avec les gens de votre classe afin d’échanger simplement. ",
    'titre': "5. Messages privés",
    'lien': "/messages/"
  },
  {
    'texte': "Accessibles en haut à droite de votre écran, elles vous indiquent si vous avez un nouveau message ou si quelqu’un a répondu à une de vos questions / une question que vous avez enregistrée.",
    'titre': "6. Notifications",
    'lien': "/accueil/"
  },
  {
    'texte': "Accessible depuis le menu déroulant, il vous permet de renseigner vos informations comme votre pseudo, vos langues vivantes, options et spécialités. Vous pouvez également ajouter une photo de profil ou ajouter des moyens de contact en décidant bien évidemment de les rendre publiques ou non. Vous y retrouverez aussi vos questions posées. Nous vous invitons à le compléter dès votre première visite !",
    'titre': "7. Profil",
    'lien': "/profil/"
  },
  {
    'texte': "Il permet de récompenser votre contribution sur le site. Vous pouvez ainsi débloquer des récompenses uniques en fonction de votre niveau, comme un large choix de thèmes pour le site lui-même. Vos récompenses ainsi que votre niveau apparaissent sur votre page de profil.",
    'titre': "8. Système d'XP",
    'lien': "/XP_tuto/"
  },
  {
    'texte': "Afin de profiter d’une expérience agréable sur key4school, nous vous demandons de toujours rester courtois et bienveillant. Sachez qu’il existe un système d’auto-modération qui concerne les questions et leurs réponses, il est également possible de l’activer dans n’importe quel groupe de messages dans les paramètres de celui-ci. Dans tous les cas, si vous remarquez quelque chose qui est déplacé et ne devrait pas se trouvez sur key4school, vous pouvez le signaler et des sanctions peuvent être prises.",
    'titre': "9. Veiller au bon déroulement de votre passage sur key4school",
    'lien': "/accueil/"
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
  if (page > 8) {
    page = 8;
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
