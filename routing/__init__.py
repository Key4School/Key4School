from routing.accueil import (XP_tuto, about, accueil, leaderboard, mail_rendu,
                             saved, tuto)
from routing.administration import (administration, sanction, signPost,
                                    signPostDiscussion, signPostMsg,
                                    signPostProfil, signRepPost,
                                    suppressionMsg, validerMsg)
from routing.demandes_aide import (DL_file, comments, file, likePost, likeRep,
                                   question, resoudre, savePost, updateComment,
                                   updateDemand)
# from routing.flask_error import custom_404
from routing.functions import afficheNotif
from routing.login import login, logout, signIn0, signIn1, signIn2
from routing.messages import (audio, createGroupe, image, modererGrp,
                              modifRole, moreMsg, page_messages, redirectDM,
                              supprGroupe, updateGroupe, updateGrpName,
                              uploadAudio, uploadImage, virerParticipant)
from routing.profil import (changeTheme, deleteAccount, emailNotVerify,
                            emailVerification, otherSubject, profil, theme,
                            topLeaderboard, updateImg, updateprofile, userImg)
from routing.recherche import morePost, moreUser, recherche, recherche_user
from routing.sockets import (connectToGroup, connectToNotif, disconnect,
                             postLike, postMsg, supprNotif)
