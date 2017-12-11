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

            self.move(x,y)
        
        
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

