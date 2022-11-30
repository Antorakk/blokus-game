from controller.plateau import Plateau
from controller.player import Player
from constants import MAX_PIECES


def hasAllPieces(player : Player)->bool:
    """Fonction permettant de vérifier si un joueur n'a pas encore joué
    sur le plateau

    Args:
        player (Player): Le joueur actuel

    Returns:
        bool: Vrai => Il a pas encore joué 
    """
    return True if player.getNbPieces()==MAX_PIECES else False

def isPositionDepart(cube_traite,player : Player)->bool:
    """Fonction permettant de vérifier si le joueur place 
    sa pièce à la première position (premier placement)

    Args:
        cube_traite (_type_): Le cube d'origine de la pièce
        player (Player): le joueur actuel

    Returns:
        bool: Vrai => Le joueur est bien sur sa position de départ
    """
    return True if player.getPositionDepart()==cube_traite else False

def verifTotalPieces(piece,plateau:Plateau,player:Player)->bool:
    """Fonction permettant de vérifier que tous les carrés de la pièce
    respectent les conditions du jeu blokus, sinon la pièce ne peut pas
    se poser.

    Args:
        piece (_type_): La pièce jouée par le joueur
        plateau (Plateau): Le plateau de jeu
        player (Player): Le joueur actuel

    Returns:
        bool: Vrai => Il peut jouer
    """
    for part_piece in piece:
            if part_piece[0]<0 or part_piece[0]>19 or part_piece[1]<0 or part_piece[1]>19:
                return False

            if not verifAroundCube(player,part_piece,plateau):
                return False
            
    return True
        
def notPieceBelow(piece,plateau:Plateau)->bool:
    """Fonction permettant de vérifier qu'une pièce ne va pas se poser sur une pièce
    existante

    Args:
        piece (_type_): La pièce jouée par le joueur
        plateau (Plateau): Le plateau de jeu

    Returns:
        bool: Vrai => La pièce peut être posé
    """
    for cube in piece:
        if not isInPlateau(cube):
            return False
        x = cube[0]
        y = cube[1]
        if plateau.getColorOfCase(x,y)!='empty':
            return False
    return True

def isInPlateau(cube : list)->bool:
    return True if 0<=cube[0]<20 and 0<=cube[1]<20 else False


def verifAroundCube(player:Player,cube,plateau:Plateau)->bool:
    """Fonction permettant de vérifier qu'un cube n'a pas un côté adjacent
    avec une pièce déjà existante

    Args:
        player (Player): le joueur actuel
        cube (_type_): le cube de la pièce 
        plateau (Plateau): le plateau de jeu

    Returns:
        bool: Vrai => La pièce peut être joué
    """
    adjacents = getSquare(cube)[1]
    for coords in adjacents:
        x = coords[0]
        y = coords[1]
        if plateau.getColorOfCase(x,y) == player.getCouleur()[0]: # Le [0] c'est pour récup que la première lettre*
            return False
    return True


def coordsBlocs(piece : list, col : int , row : int) -> list:
    """Donnes les coordonnées de chaque piece d'un bloc si celui-ci est != 0
       0 équivaut à un emplacement "vide"
       >>> coords_blocs([1,1],2,2)
       >>> [3,3]

    Args:
        piece (list): la pièce du bloc
        row (int): la ligne à l'origine du premier cube (permet une simulation de déplacement de cube)
        col (int): la colonne à l'origine du premier cube 

    Returns:
        list: nouvelles coordonées d'une pièce dans un bloc.
    """
    new_piece : list = []
    for y in range(len(piece)): # Longeur
        for x in range(len(piece[0])): # Largeur
            if piece[y][x]==1:
                new_piece.append([y+row,col+x])
    return new_piece


def validPlacement(bloc: list[int], row: int, col: int, plateau: Plateau, player:Player) -> bool:
    """Fonction permettant de vérifier si un bloc peut être placer sur le plateau.

    Args:
        bloc (list[list]): le bloc à positionner sur le plateau
        row (int): ligne de position à l'origine de la pièce
        col (int): colonne de position à l'origine de la pièce
        plateau (Plateau): plateau de jeu
        player (Player): Joueur

    Returns:
        bool: le bloc peut être ajouté au tableau
    """
    playerColor : str = player.getCouleur()[0]
    new_bloc : list = coordsBlocs(bloc,col,row)
    
    #  Cas ou le joueur n'a pas encore joué, et il va jouer sa première pièce
    for each_cube in new_bloc:
        if hasAllPieces(player):
            if isPositionDepart(each_cube,player):
                if verifTotalPieces(new_bloc,plateau,player):
                    return True
        # Les cas généraux 
        else:
            print("Cas générale")
            if expectedPlayerInDiagonals(each_cube,plateau,playerColor):
                print("Joueur diagonale")
                if notPieceBelow(new_bloc,plateau):
                    print("Pas de pièce en dessous")
                    if verifTotalPieces(new_bloc,plateau,player):
                        print("Vérif total pièce")
                        return True
    return False
    

def getSquare(piece: list) -> list[list]:
    """Obtenir toutes les positions autour d'un cube

    Args:
        piece (list): le cube du bloc

    Returns:
        list[list]: liste des positions autour du cube
    """
    return [list(filter(lambda el:(0<=el[0]<=19 and 0<=el[1]<=19),getDiagonals(piece))),
            list(filter(lambda el:(0<=el[0]<=19 and 0<=el[1]<=19),getAdjacents(piece)))]

def getDiagonals(piece: list) -> list[list]:
    """Obtenir toutes les diagonales autour d'un cube

    Args:
        piece (list): le cube du bloc

    Returns:
        list[list]: liste des diagonales autour du cube
    """
    return [
            [piece[0]-1,piece[1]-1],[piece[0]-1,piece[1]+1],  
            [piece[0]+1,piece[1]-1],[piece[0]+1,piece[1]+1]     
    ]

def getAdjacents(piece: list) -> list[list]:
    """Obtenir toutes les côtés adjacents autour d'un cube

    Args:
        piece (list): le cube du bloc

    Returns:
        list[list]: liste des adjacents autour du cube
    """
    return [
                                 [piece[0]-1,piece[1]],   
            [piece[0],piece[1]-1]         ,           [piece[0],piece[1]+1], 
                                 [piece[0]+1,piece[1]]   
    ]

def expectedPlayerInDiagonals(piece: list, plateau: Plateau, colorPlayer: str) -> bool:
    """Fonction permettant de savoir si il existe dans une des diagonales il existe un cube de la couleur
    correspondante au joueur actuel

    Args:
        piece (list): le cube du bloc à ajouter
        plateau (Plateau): le plateau de jeu
        colorPlayer (str): la couleur du joueur

    Returns:
        bool: Vrai : il existe dans l'une des diagonales un carré existant de la même couleur.
              Faux : l'inverse.
    """
    diagonals = getSquare(piece)[0]
    # print(colorPlayer,plateau.getColorOfCase())
    for y,x in diagonals:
        if plateau.getColorOfCase(y,x) == colorPlayer:
            return True
    return False

def playerCanPlay(player:Player,plateau:Plateau)->bool:
    """Permet de vérifier si un joueur est en capacité de jouer ou non.

    Args:
        player (Player): Le joueur actuel
        plateau (Plateau): Le plateau derrière l'affichage graphique

    Returns:
        bool: Vrai = Il peut jouer, Faux l'inverse
    """
    for indice_piece in player.pieces.pieces_joueurs:
        for i in range(0,20):
            for j in range(0,20):
                if validPlacement(player.pieces.liste_pieces[indice_piece],i,j,plateau,player):
                    print(f"La pièce n°{indice_piece+1} peut jouer en {i}-{j}")
                    return True
    return False

if __name__ == "__main__":
    # Kind of test if you want to try 
    pass
    # tab = Plateau(20,20)
    # joueur = Player("Vert")
    # piece = joueur.jouerPiece(2)
    # if valid_placement(piece,16,0,tab,joueur):
    #     new_bloc = coords_blocs(piece,16,0)
    #     for y,x in new_bloc:
    #         tab.setColorOfCase(y,x,1)
    # joueur.pieces.rotate(2)
    # piece = joueur.jouerPiece(2)
    # if valid_placement(piece,14,2,tab,joueur):
    #         new_bloc = coords_blocs(piece,14,2)
    #         for y,x in new_bloc:
    #             tab.setColorOfCase(y,x,1)
    # piece = joueur.jouerPiece(2)
    # print(piece)
    # if valid_placement(piece,12,3,tab,joueur):
    #         new_bloc = coords_blocs(piece,12,3)
    #         for y,x in new_bloc:
    #             tab.setColorOfCase(y,x,1)
    # print(tab)
