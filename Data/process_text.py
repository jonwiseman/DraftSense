import argparse
import json
import re
import pickle


def main():
    parser = argparse.ArgumentParser(description='Pre-process text, including removing excessive whitespace, spaces '
                                                 'before punctuation, articles with no dates, replacing full team names'
                                                 ' with shortened versions, and fixing a few quirky ESPN notations.'
                                                 'Also removes articles that do not have dates')
    parser.add_argument('y', metavar='YEAR', type=int, help='Season year')
    args = parser.parse_args()

    year = args.y

    with open(f'/home/jon/Desktop/thesis/Data/Articles/Raw/{year}.json', 'r') as f:
        data = json.load(f)
    full_team_names = pickle.load(open(f'/home/jon/Desktop/thesis/Pickles/2010/full_names.p', 'rb'))
    people = pickle.load(open(f'/home/jon/Desktop/thesis/Pickles/people.p', 'rb'))

    players = list(people.keys())
    processed = []
    for article in data:
        if has_date(article):
            article['title'] = clean_text(article['title'])
            article['content'] = clean_text(article['content'])

            article['title'] = clean_team_names(article['title'], full_team_names)
            article['content'] = clean_team_names(article['content'], full_team_names)

            article['title'] = clean_names(article['title'], players)
            article['content'] = clean_names(article['content'], players)
            processed.append(article)

    with open(f'/home/jon/Desktop/thesis/Data/Articles/Processed/{year}_processed.json', 'w') as f:
        json.dump(processed, f)


def clean_text(text):
    if text is None:
        return text
    cleaned = re.sub(r'\s\s+', ' ', text)
    cleaned = re.sub(r'\n', '', cleaned)
    cleaned = re.sub(r'\s([,.?!;)])', r'\1', cleaned)
    cleaned = re.sub(r'No. (\d)', r'number \1', cleaned)
    return cleaned


def clean_team_names(text, long_names):
    if text is None:
        return text

    cleaned_text = text
    for name in long_names:
        comp = name.split(' ')
        team = comp[-1]
        city = comp[0]
        if len(comp) == 3:
            city = ' '.join(comp[:-1])

        cleaned_text = re.sub(name, team, cleaned_text)
        if city != 'New York':
            cleaned_text = re.sub(city, team, cleaned_text)
    return cleaned_text


def clean_names(text, players):
    if text is None:
        return text

    cleaned_text = text
    for name in name_replacement_generator(text, players):
        comp = name.split(' ')
        first_name = comp[0]
        last_name = comp[-1]

        cleaned_text = re.sub(last_name, name, cleaned_text)
        cleaned_text = re.sub(rf'{first_name}\s{first_name}', rf'{first_name}', cleaned_text)

    return cleaned_text


def name_replacement_generator(text, players):
    for name in players:
        if name in text:
            yield name


def has_date(article):
    if article['date'] is None:
        return False

    return True


if __name__ == '__main__':
    main()
