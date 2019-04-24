#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from typing import Iterable

def longest_substrings(x: str, y: str) -> Iterable[str]:
    # source (rows)
    n = len(x)
    # target (columns)
    m = len(y)
    x = x.lower()
    y = y.lower()

    # initialize similarity matrix
    d = [[None for _ in range(m+1)] for _ in range(n+1)]

    # fill in the first cell
    d[0][0] = 0

    # for each row i from 1 to n
    # fill in the first column with zeros
    for i in range(1, n+1):
        d[i][0] = 0

    # for each column j from 1 to m
    # fill in the first row with zeros
    for j in range(1, m+1):
        d[0][j] = 0

    # initialize variable to save maximum value
    maxim = 0

    # recursively populate the matrix
    for i in range(1, n+1):
        for j in range(1, m+1):
            # only consider same letters in strings
            if x[i-1] == y[j-1]:
                d[i][j] = d[i-1][j-1] + 1
                # save max value
                if d[i][j] > maxim:
                    maxim = d[i][j]
            else:
                d[i][j] = 0

    # print the  matrix
    # for a in d:
    #     print(a)

    # initialize list of end points
    offsets = []

    # find end points in string
    for row in d:
        for ind, value in enumerate(row):
            if value == maxim:
                offsets.append(ind)

    # if no common substrings found
    if maxim == 0:
        print(None)
    else:
        # iterate over string and print common substrings
        print([y[o-maxim:o] for o in offsets])

if __name__ == '__main__':
    longest_substrings('mozart', 'mozzarella')
    longest_substrings('Haus', 'Maus')
    longest_substrings('Kleistermasse', 'Meisterklasse')
    longest_substrings('keep the interface!', 'KeEp ThE iNtErFaCe!')
    longest_substrings('Tod', 'Leben')
