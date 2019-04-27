#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import gzip
import ssl
from pathlib import Path
import random
from typing import BinaryIO
from urllib.request import urlopen
# import xml.etree.ElementTree as ET
import lxml.etree as ET

# here I go monkeypatching AGAIN
# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

def iterate_thru_corpus(infile):
    abstracts = []
    hash_values = set()
    for _, abstract in ET.iterparse(infile, tag='document'):
        text = ' '.join(sent.text for sent in abstract.iterfind('.//section/sentence'))
        text_hash = hash(text)
        if text_hash not in hash_values:
            hash_values.add(text_hash)
            yield text
            # abstracts.append(text)
        abstract.clear()

    # return abstracts

def split_corpus(infile: BinaryIO, targetdir: str,
                   n: int=3):

    dev = Path(format(targetdir+'/abstracts.txt.development.gz'))
    test = Path(format(targetdir+'/abstracts.txt.test.gz'))
    train = Path(format(targetdir+'/abstracts.txt.training.gz'))

    abstracts = (abs for abs in iterate_thru_corpus(infile))
    devs = (i for i in abstracts if i in sample(abstracts, n))
    tests = (i for i in abstracts if i in sample(abstracts, n))
    # print(type(rands))
    # for i in abstracts:
        # print('8')
    # print(type(rest))
    # split = int(len(rands)/2)
    # devs = rands[:split]
    # tests = rands[split:]
    # trains = (a for a in abstracts if a not in tests and a not in devs)
    print('\n'.join(devs))
    print('\n'.join(tests))

    # print(len(devs))
    # print(len(tests))
    # print(sum(1 for a in trains))


def sample(iterable, k):
    """
    Returns @param k random items from @param iterable.
    """
    reservoir = []
    for t, item in enumerate(iterable):
        if t < k:
            reservoir.append(item)
        else:
            m = random.randint(0,t)
            if m < k:
                reservoir[m] = item

    return reservoir


def main():
    # stream = urlopen('https://files.ifi.uzh.ch/cl/pcl/pcl2/abstracts.xml.gz')
    # stream = Path('Korpusdaten/abstracts.xml.gz')
    stream = format('25642278.xml.gz')
    outfile_dir = format('Korpusdaten')
    with gzip.open(stream) as inp:
        split_corpus(inp, outfile_dir)

if __name__ == '__main__':
    main()
