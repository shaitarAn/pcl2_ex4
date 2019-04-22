#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import gzip
import ssl
from pathlib import Path
import random
from typing import BinaryIO
from urllib.request import urlopen
import lxml.etree as ET
import time

# This programm took 00:35:55.79 to run.
# It used up to 7.3GB of RAM out of 8GB.

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
            abstracts.append(text)
        abstract.clear()

    return abstracts

def split_corpus(infile: BinaryIO, targetdir: str,
                   n: int=1000):

    dev = Path(format(targetdir+'/abstracts.txt.development.gz'))
    test = Path(format(targetdir+'/abstracts.txt.test.gz'))
    train = Path(format(targetdir+'/abstracts.txt.training.gz'))

    abstracts = iterate_thru_corpus(infile)

    devs = sample(abstracts, n)
    tests = sample((a for a in abstracts if a not in devs), n)
    trains = (a for a in abstracts if a not in tests and a not in devs)

    with gzip.open(dev, 'wb') as d, gzip.open(
                    test, 'wb') as t, gzip.open(
                    train, 'wb') as tr:

        for a in devs:
            d.write(a.encode())
            d.write(b'\n')
        for a in tests:
            t.write(a.encode())
            t.write(b'\n')
        for a in trains:
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
    # to run from local file:
    # stream = Path('Korpusdaten/abstracts.xml.gz')
    # using a sample:
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
