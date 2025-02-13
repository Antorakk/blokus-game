from random import randint
from models.Player import Player
from models.Plateau import Plateau
from utils.game_utils import validPlacement,coordsBlocs,getDiagonals,getAdjacents
from copy import deepcopy
from config import APP_PATH

def pickPiece(joueur:Player)->int:
    index = 100
    while index not in joueur.pieces.pieces_joueurs:
        index = randint(0,20)
    return index


def managePiece(joueur:Player,plateau:Plateau,positions:list):

    choix = 0
    if len(positions) > 1:
        choix = randint(0,len(positions)-1)
    x,y = positions[choix]

    checkIf = False
    cannotPlay = False
    idPiece = 0
    piece = []
    print(f"Ce qui arrive en x : {x} et y : {y}")

    copyPieces = deepcopy(joueur.pieces.pieces_joueurs)
    # print(copyPieces)

    while not checkIf and not cannotPlay: 
        idPiece =  pickPiece(joueur)
        
        if idPiece in copyPieces:
            copyPieces.remove(idPiece)
            piece = joueur.jouerPiece(idPiece)
            checkIf = validPlacement(piece,x,y,plateau,joueur)

        if not len(copyPieces):
            choix = 0
            if len(positions) > 1:
                choix = randint(0,len(positions)-1)
                x,y = positions[choix]
                positions.remove( positions[ choix ] )
                copyPieces = deepcopy(joueur.pieces.pieces_joueurs)
            else: cannotPlay = True

    if checkIf and not cannotPlay:
        joueur.hasPlayedPiece(idPiece)
        return coordsBlocs(piece,y,x),idPiece
    else: return [ -1, -1 ],idPiece

def adjacents(x,y,plateau:Plateau,indexJoueur:int)->list:
    adjs = [[x-1,y],[x,y-1],[x,y+1],[x+1,y]]

    possibilites = []
    grille = plateau.getTab()

        
    if grille[adjs[0][0]][adjs[0][1]] != indexJoueur and grille[adjs[1][0]][adjs[1][1]] != indexJoueur:
        possibilites.append([adjs[0][0],adjs[1][1]])
    
    if grille[adjs[0][0]][adjs[0][1]] != indexJoueur and grille[adjs[2][0]][adjs[2][1]] != indexJoueur:
        possibilites.append([adjs[0][0],adjs[2][1]])
    
    if grille[adjs[3][0]][adjs[3][1]] != indexJoueur and grille[adjs[1][0]][adjs[1][1]] != indexJoueur:
        possibilites.append([adjs[3][0],adjs[1][1]])
    
    if grille[adjs[3][0]][adjs[3][1]] != indexJoueur and grille[adjs[2][0]][adjs[2][1]] != indexJoueur:
        possibilites.append([adjs[3][0],adjs[2][1]])
    
    return list(filter(lambda coords : 0<=coords[0]<=19 and 0<=coords[1]<=20 and grille[coords[0]][coords[1]]!=indexJoueur,possibilites))

def getPossibilities(indexJoueur:int,plateau:Plateau,joueur:Player)->list:
    p = []
    grille = plateau.getTab()
    for i,ligne in enumerate(grille):
        for j,col in enumerate(ligne):
            if col == indexJoueur:
                possibilities = adjacents(i,j,plateau,indexJoueur)
                if len(possibilities):
                    for _pos in possibilities:
                        p.append(_pos)
    if not len(p):
        return [joueur.getPositionDepart()]
    return p

def easy_automate(joueurActuel : Player,plateau : Plateau,index:int,view,db):

    cheminFichierPiece = APP_PATH + r"/../media/pieces/" + joueurActuel.getCouleur().upper()[0] + "/1.png"
    # cheminFichierPiece = PIECES_IMAGES_URL[joueurActuel.getCouleur().upper()[0]][0]

    possibilities = getPossibilities(index,plateau,joueurActuel)
    pieceBlokus,idPiece = managePiece(joueurActuel,plateau,possibilities)

    if pieceBlokus[ 0 ] != -1:
        for xpos,ypos in pieceBlokus:
            view._addToGrid(cheminFichierPiece,ypos,xpos)
            plateau.setColorOfCase(xpos,ypos,index)

        db.addPoints(joueurActuel.couleur,len(pieceBlokus))
        db.addToHistoriquePlayer(joueurActuel.couleur,pieceBlokus[0][0],pieceBlokus[0][1],idPiece,0,0)
