#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# PCL II, FS 19
# Uebung 3 Aufgabe 1
# Author: Anastassia Shaitarova, Varvara Stein
# Matrikelnr.: 17705062  , 18743500

from typing import Iterable
import sys

def longest_substrings(x: str, y: str) -> Iterable[str]:
    '''
    finds longest common substrings between two words
    '''
    # length of source (num of rows)
    len_src = len(x)
    # length of target (num of columns)
    len_trg = len(y)

    x = x.lower()
    y = y.lower()

    # initialize similarity matrix and fill it with zeros
    d = [[0 for _ in range(len_trg+1)] for _ in range(len_src+1)]

    # initialize variable to save maximum value
    maxim = 0

    # recursively populate the matrix
    for i in range(1, len_src+1):
        for j in range(1, len_trg+1):
            # only consider same letters in both strings
            if x[i-1] == y[j-1]:
                # add only diagonally
                d[i][j] = d[i-1][j-1] + 1
                # save max value
                if d[i][j] > maxim:
                    maxim = d[i][j]

    # print the  matrix
    # for row in d:
    #     print(row)

    # initialize list of end points
    offsets = []

    # find end points in target string
    for row in d:
        for ind, value in enumerate(row):
            if value == maxim:
                offsets.append(ind)

    # if no common substrings found
    if maxim == 0:
        print(None)
    else:
        # iterate over traget string and print common substrings
        print([y[o-maxim:o] for o in offsets])

def main():
    string1 = sys.argv[1]
    string2 = sys.argv[2]
    # longest_substrings('mozart', 'mozzarella')
    # longest_substrings('Haus', 'Maus')
    # longest_substrings('Kleistermasse', 'Meisterklasse')
    # longest_substrings('keep the interface!', 'KeEp ThE iNtErFaCe!')
    # longest_substrings('Tod', 'Leben')
    longest_substrings(string1, string2)

if __name__ == '__main__':
    main()
