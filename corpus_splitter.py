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
import time

# here I go monkeypatching AGAIN
# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
ssl._create_default_https_context = ssl._create_unverified_context

# abstracts.txt.training.gz
# abstracts.txt.test.gz
# abstracts.txt.development.gz

# Die Abstracts, die für das Test- oder Dev-Set ausgewählt wurden, dürfen natürlich nicht auch im Trainings-Set stehen.

# Stelle zuerst sicher, dass du gefahrlos durch das XML-File iterieren und die Ausgabesätze zusammenbauen kannst, ohne deinen Arbeitsspeicher zu überlasten.

def split_corpus(infile: BinaryIO, targetdir: str,
                   n: int=3):

    dev = Path(format(targetdir+'/abstracts.txt.development.gz'))
    test = Path(format(targetdir+'/abstracts.txt.test.gz'))
    train = Path(format(targetdir+'/abstracts.txt.training.gz'))

    abs = 0
    hash_values = set()
    abstracts = []
    for _, abstract in ET.iterparse(infile, tag='document'):
        text = ' '.join(sent.text for sent in abstract.iterfind('.//section/sentence'))
        # to deduplicate abstracts
        text_hash = hash(text)
        if text_hash not in hash_values:
            hash_values.add(text_hash)
        abs += 1
        abstracts.append(text)
        abstract.clear()

    print(abs)
    deva = sample(abstracts, n)
    testa = sample((a for a in abstracts if a not in deva), n)
    traina = (a for a in abstracts if a not in testa and a not in deva)

    with gzip.open(dev, 'wb') as d, gzip.open(
                    test, 'wb') as t, gzip.open(
                    train, 'wb') as tr:

        for a in deva:
            d.write(a.encode())
            d.write(b'\n')
        for a in testa:
            t.write(a.encode())
            t.write(b'\n')
        for a in traina:
            tr.write(a.encode())
            tr.write(b'\n')

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
    start = time.time()
    stream = urlopen('https://files.ifi.uzh.ch/cl/pcl/pcl2/abstracts.xml.gz')
    # stream = Path('Korpusdaten/abstracts.xml.gz')
    # stream = format('25642278.xml.gz')
    outfile_dir = format('Korpusdaten')
    with gzip.open(stream) as inp:
        split_corpus(inp, outfile_dir)

    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("This programm took {:0>2}:{:0>2}:{:05.2f} to run.".format(int(hours),int(minutes),seconds))

if __name__ == '__main__':
    main()
