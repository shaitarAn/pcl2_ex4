#!/usr/bin/env python3
#-*- coding: utf-8 -*-

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

    hash_values = set()
    with bz2.open(outfile, 'w') as out:
        for line in infile:
            data = json.loads(line)
            comment = data['body']
            comment = re.sub(r'\n+', r' ', comment)
            if min_len < len(comment) < max_len:
                if data['score'] >= min_score:
                    comment_hash = hash(comment)
                    if comment_hash not in hash_values:
                        hash_values.add(comment_hash)
                        out.write(comment.encode())
                        out.write(b'\n')

def main():
    start = time.time()
    # bzcat RC_2012-06.bz2 | head -25541 > data_25541lines.json
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
