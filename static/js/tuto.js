var page = 0;
var imageMax = 8;

var data = [
  {
    'texte': "Bienvenue sur <b>Key4School</b> ! Nous sommes ravis de votre arrivée ! Key4School est un réseau social développé par 12 lycéens d’Ile de France a destination des lycéens. L’objectif est d’y <b>trouver de l’aide et de s’entraider facilement</b> !",
    'titre': "1. Présentation",
    'lien': "/"
  },
  {
    'texte': "Dès votre arrivée sur le site, vous êtes sur la <b>page d’accueil</b> où se trouvent les questions posées par d’autres membres les <em>plus likées</em>. Les questions ne concernent <b>uniquement</b> les matières que vous étudiez, pour en sélectionner une en particulier vous pouvez utiliser les <b>filtres</b> en haut de page. Si en défilant vous tombez sur une question à laquelle vous pouvez répondre alors n’hésitez-pas, il vous suffit de <b>cliquer sur la bulle en dessous</b> ! ",
    'titre': "2. Accueil",
    'lien': "/"
  },
  {
    'texte': 'Quand vous avez une <b>question à poser</b>, vous pouvez dans un premier temps taper les mots-clés dans la <b>barre de recherche</b> et regarder s’il y en a déjà une qui y répond. Si vous ne trouvez pas votre réponse, vous n’avez qu’à cliquer sur <em>« Poser une question »</em> et remplir le <b>formulaire</b> qui vous ait donné. Vous pouvez également joindre un fichier comme un exercice, par exemple. Essayez d’être poli et le plus clair possible. Une fois que vous estimez que vous avez obtenu réponse à votre question, vous n’avez plus qu’à la mettre en tant que <b>résolue</b> afin de fermer le sujet.',
    'titre': "3. Poser une question",
    'lien': "/question/"
  },
  {
    'texte': "En dessous de chaque question, vous avez la possibilité de l’<b>enregistrer</b> afin de pouvoir la retrouver dans la page correspondante accessible dans le menu en haut à droite. Cela vous permet ainsi soit d’y répondre plus tard soit d’être informé si elle est résolue par quelqu’un. ",
    'titre': "4. Demandes enregistrées",
    'lien': "/saved/"
  },
  {
    'texte': "Ils sont accessibles à partir du menu en haut à droite, vous pouvez <b>créer</b> des groupes avec le « + », <b>envoyer des messages, des vocaux et même des images</b> !",
    'titre': "5. Messages privés",
    'lien': "/messages/"
  },
  {
    'texte': "Accessibles en haut à droite de votre écran, elles vous indiquent si vous avez un nouveau message ou si quelqu’un a répondu à une de vos questions / une question que vous avez enregistrée.",
    'titre': "6. Notifications",
    'lien': "/"
  },
  {
    'texte': "Accessible depuis le menu déroulant, il vous permet de <b>renseigner vos informations</b> comme votre pseudo, vos langues vivantes, options et spécialités. Vous pouvez également ajouter une photo de profil ou ajouter des moyens de contact en décidant bien évidemment de les rendre publiques ou non. Vous y retrouverez aussi <b>vos questions posées</b>. <u><b>Nous vous invitons à le compléter dès votre première visite !</b></u>",
    'titre': "7. Profil",
    'lien': "/profil/"
  },
  {
    'texte': "Il permet de <b>récompenser votre contribution</b> sur le site. Vous pouvez ainsi débloquer des <b>récompenses uniques en fonction de votre niveau</b>, comme un large choix de <b>thèmes</b> pour le site lui-même. Vos récompenses ainsi que votre niveau apparaissent sur votre page de profil.",
    'titre': "8. Système d'XP",
    'lien': "/XP_tuto/"
  },
  {
    'texte': "Afin de profiter d’une expérience agréable sur <b>Key4School</b>, nous vous demandons de toujours <b>rester courtois et bienveillant</b>. Sachez qu’il existe un <b>système d’auto-modération</b> qui concerne les questions et leurs réponses, il est également possible de l’activer dans n’importe quel groupe de messages dans les paramètres de celui-ci. Dans tous les cas, si vous remarquez quelque chose qui est déplacé et ne devrait pas se trouvez sur Key4School, vous pouvez le <u><b>signaler</b></u> et des <b>sanctions</b> peuvent être prises.",
    'titre': "9. Veillez au bon déroulement de votre passage sur Key4School",
    'lien': "/"
  }
]

function update(){
  document.getElementById("iframTuto").src = data[page].lien;
  document.getElementById("texte").innerHTML = data[page].texte;
  document.getElementById("titre").innerHTML = data[page].titre;
  document.getElementById("progressTuto").value = page+1;
}

function suivant() {
  page += 1;
  if (page > 8) {
    page = 8;
  }
  if (page == imageMax) {
    document.getElementById("next").style.display = "none";
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
