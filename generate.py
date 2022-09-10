import argparse
import dill
import re
import sys
import os
import random
import numpy


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', dest='model_file', required=True)

    parser.add_argument('--prefix', dest='prefix', required=False)
    
    parser.add_argument('--length', dest='length', type=int, required=True)

    args = parser.parse_args()

    model = open(args.model_file, 'rb+')
    try:
        data = dill.load(model)
    except:
        data = dict()

    if "--prefix" not in sys.argv:
            args.prefix = random.choice(list(data.keys()))

    args.prefix = str(args.prefix).lower().split()

    for i in range(args.length):

        if tuple(args.prefix) not in data:
            break
        next_word = numpy.random.choice([e[0] for e in data[tuple(args.prefix)][0]], p=[data[tuple(args.prefix)][0][w][1] for w in range(len(data[tuple(args.prefix)][0]))])

        print(next_word, end=' ')

        args.prefix = args.prefix[1::]
        args.prefix.append(next_word)


if __name__ == '__main__':
    main()
