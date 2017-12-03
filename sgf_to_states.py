import os
import numpy as np
import sys
from go import Board, BoardError, View, clear, getch

# creer la liste contenant la liste des coups joues dans le sgf
def sgf_to_moves_list(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()

    if 'AB[' in content or 'AW[' in content:
        return False

    moves = []
    ind = 0

    while True:
        if len(moves) % 2 == 0:
            index = content.find(';B[', ind)
            if index == -1:
                break
        else:
            index = content.find(';W[', ind)
            if index == -1:
                break

        if content[index + 3] == ']':
            moves.append('pass')
            ind = index + 4
            continue

        x, y = [ord(letter) - ord('a') for letter in content[index+3:index+5]]

        moves.append((x, y))
        ind = index + 6

    return moves

def moves_to_one_state(taille,moves,numero_du_coup):
    #joue les coups donnees par le fichier sfg jusqu'as un coup donne
    self=Board(taille)

    for i, move in enumerate(moves):
        if i<numero_du_coup:
            """
            Makes a move at the given location for the current turn's color.
            """
            x=move[0]+1
            y=move[1]+1

        # Check if coordinates are occupied
            if self[x, y] is not self.EMPTY:
                raise BoardError('Cannot move on top of another piece!')

        # Store history and make move
            self._push_history()
            self[x, y] = self._turn

        # Check if any pieces have been taken
            taken = self._take_pieces(x, y)

        # Check if move is suicidal.  A suicidal move is a move that takes no
        # pieces and is played on a coordinate which has no liberties.
            if taken == 0:
                self._check_for_suicide(x, y)

        # Check if move is redundant.  A redundant move is one that would
        # return the board to the state at the time of a player's last move.
            self._check_for_ko()

            self._flip_turn()
            self._redo = []
        
        
    return self 

def sgf_to_states(filename,taille):
    #stocke tout les etats dans une liste
    moves=sgf_to_moves_list(filename)
    
    states=[]
    i=0
    while i<len(moves):
        states.append(moves_to_one_state(taille,moves,i))
        i=i+1
    return states

