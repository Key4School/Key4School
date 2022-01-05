from routing.accueil import accueil, tuto, XP_tuto, mail_rendu, saved, about, leaderboard
from routing.administration import administration, suppressionMsg, validerMsg, sanction, signPost, signRepPost, signPostProfil, signPostDiscussion, signPostMsg
from routing.demandes_aide import question, comments, updateDemand, updateComment, file, DL_file, likePost, likeRep, resoudre, savePost
# from routing.flask_error import custom_404
from routing.functions import afficheNotif
from routing.login import login, signIn0, signIn1, signIn2, logout
from routing.messages import page_messages, redirectDM, uploadAudio, audio, uploadImage, image, createGroupe, updateGroupe, virerParticipant, modifRole, supprGroupe, updateGrpName, moreMsg, modererGrp
from routing.profil import profil, changeTheme, theme, updateprofile, userImg, updateImg, otherSubject, topLeaderboard, deleteAccount, emailNotVerify, emailVerification
from routing.recherche import recherche, recherche_user, morePost, moreUser
from routing.sockets import connectToNotif, disconnect, supprNotif, connectToGroup, postMsg, postLike
