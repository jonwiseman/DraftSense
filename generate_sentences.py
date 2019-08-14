import argparse
import pandas as pd
import pickle
import nltk
import nltk.data
import re


def main():
    parser = argparse.ArgumentParser(description='Generate training sentences for learning football entities')
    parser.add_argument('y', metavar='YEAR', type=int, help='Season year')
    args = parser.parse_args()

    year = args.y

    corpus = pd.read_json(f'/home/jon/Desktop/thesis/{year}/{year}.json')
    team_names = pickle.load(open(f'/home/jon/Desktop/thesis/{year}/team_names.p', 'rb'))
    city_names = pickle.load(open(f'/home/jon/Desktop/thesis/{year}/city_names.p', 'rb'))

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    train_sentences = []
    for i in range(len(corpus)):
        for sent in tokenizer.tokenize(corpus.iloc[i]['content']):
            found_entities = []
            for entity in team_names:
                found_entities.extend([(m.start(), m.end(), 'NFL') for m in re.finditer(entity, sent)])
            for entity in city_names:
                found_entities.extend([(m.start(), m.end(), 'NFL') for m in re.finditer(entity, sent)])
            if len(found_entities):
                train_sentences.append((sent, {'entities': found_entities}))

    pickle.dump(train_sentences, open('training_sentences.p', 'wb'))


if __name__ == '__main__':
    main()