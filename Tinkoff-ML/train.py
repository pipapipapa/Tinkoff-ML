import argparse
import dill
import re
import sys
import os


def cleantxt(file):
    pattern = re.compile('[\W_0-9]+')
    return pattern.sub(' ', file).lower().split()


def train(model, file):
    file_cln = cleantxt(file)
    model = open(model, "wb+")
    try:
        data = dill.load(model)
    except:
        data = dict()
    for n in range(1, len(file_cln)):
        for i in range(len(file_cln) - n):
            if tuple(file_cln[i: i + n]) not in data:
                p = 1
                data[tuple(file_cln[i: i + n])] = [[[file_cln[i + n], 1 / p]], p]
            #data[file_cln[i: i + n]][data[file_cln[i: i + n]][0].index([[file_cln[i + n], '.']])[1] = data[file_cln[i: i + n]][data[file_cln[i: i + n]][0].index([[file_cln[i + n], '.']])[1] + (1 / p)
            for words in data[tuple(file_cln[i: i + n])][0]:
                if words[0] == file_cln[i + n]:
                    words[1] += (1 / p)
                words[1] *= p / (p + 1) 
            data[tuple(file_cln[i: i + n])][1] += 1
    new_data = data
    dill.dump(new_data, model)
    model.close()
    


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--input-dir', dest='input', required=False)

    parser.add_argument('--model', dest='model_file', required=True)

    if "--input-dir" not in sys.argv:
        file = input()

    args = parser.parse_args()

    for address, dirs, files in os.walk(args.input):
        for name in files:
            sample = open(os.path.join(address, name), "r", encoding="utf-8")
            train(args.model_file, sample.read())
            sample.close()
    


if __name__ == '__main__':
    main()