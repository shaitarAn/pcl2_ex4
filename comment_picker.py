#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# PCL II, FS 19
# Uebung 3 Aufgabe 1
# Author: Anastassia Shaitarova, Varvara Stein
# Matrikelnr.: 17705062  , 18743500

import json
import bz2
import sys
import re
from pathlib import Path
from typing import BinaryIO
import time

def mk_meme_corpus(infile: BinaryIO, outfile: str,
                     min_score: int=100,
                     min_len: int=1,
                     max_len: int=50):
    '''
    Reads through large binary file with multiple json objects,
    extracts short and popular comments from json,
    writes unique comments to zipped file.
    '''

    hash_values = set()
    with bz2.open(outfile, 'w') as out:
        for line in infile:
            data = json.loads(line)
            comment = data['body']
            # replace new lines within a comment with a space
            comment = re.sub(r'\n+', r' ', comment)
            if min_len < len(comment) < max_len:
                if data['score'] >= min_score:
                    # deduplicate
                    comment_hash = hash(comment)
                    if comment_hash not in hash_values:
                        hash_values.add(comment_hash)
                        out.write(comment.encode())
                        out.write(b'\n')

def main():
    # to get a sample with repeating comments
    # bzcat RC_2012-06.bz2 | head -25541 > data_25541lines.json

    start = time.time()
    infile = Path('Korpusdaten/RC_2012-06.bz2')
    outfile = format('laconic_corpus.txt')
    with bz2.open(infile, 'r') as f:
        mk_meme_corpus(f, outfile)

    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("This programm took {:0>2}:{:0>2}:{:05.2f} to run.".format(int(hours),int(minutes),seconds))

if __name__ == '__main__':
    main()
