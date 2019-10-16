import argparse
import json
import pickle
import spacy
import pandas as pd
from datetime import datetime
from datetime import timedelta
from spacy.pipeline import EntityRuler


def main():
    parser = argparse.ArgumentParser(description='Annotate text with the entities contained in each article, as well'
                                                 'as which NFL week the article corresponds to.')
    parser.add_argument('y', metavar='YEAR', type=int, help='Season year')
    args = parser.parse_args()

    year = args.y

    nlp = spacy.load("en_core_web_lg")
    with open(f'/home/jon/Desktop/thesis/Data/Articles/Processed/{year}_processed.json', 'r') as f:
        articles = json.load(f)
    teams = pickle.load(open('/home/jon/Desktop/thesis/Pickles/2010/team_names.p', 'rb'))
    people = pickle.load(open('/home/jon/Desktop/thesis/Pickles/people.p', 'rb'))

    names = list(people.keys())

    ruler = EntityRuler(nlp, overwrite_ents=True)
    patterns = [{'label': 'NFL', 'pattern': team} for team in teams]
    name_patterns = [{'label': 'NFL', 'pattern': name} for name in names]
    patterns.extend(name_patterns)
    ruler.add_patterns(patterns)
    ruler.add_patterns(name_patterns)
    nlp.add_pipe(ruler)

    merge_ents = nlp.create_pipe("merge_entities")
    nlp.add_pipe(merge_ents)

    names.extend(teams)
    entities = {person: 0 for person in names}
    processed = []
    next_year = []

    games = pd.read_csv('/home/jon/Desktop/thesis/Data/Kaggle CSV Files/Games/spreadspoke_scores.csv')
    games = games[games['schedule_season'] == year]
    games = games[['schedule_date', 'schedule_season', 'schedule_week']]
    games.drop_duplicates(['schedule_date', 'schedule_week'], inplace=True)
    games.drop_duplicates(['schedule_season', 'schedule_week'], keep='last', inplace=True)
    games['schedule_date'] = pd.to_datetime(games['schedule_date'])

    date_map = {}

    for i in range(len(games) - 1):
        start = games.iloc[i]['schedule_date']
        end = games.iloc[i + 1]['schedule_date']
        index = pd.date_range(start, end)
        date_map[games.iloc[i]['schedule_week']] = index

    date_map['Offseason'] = pd.date_range(datetime(2010, 2, 7), datetime(2010, 9, 6))

    for article in articles:
        this_article = []
        doc = nlp(article['content'])
        for ent in doc.ents:
            if ent.label_ == 'NFL':
                entities[ent.text] += 1
                if ent.text not in this_article:
                    this_article.append(ent.text)

        article['Entities'] = this_article
        week = get_week(date_map, clean_date(article['date']))
        if week is None:
            next_year.append(article)
        else:
            article['Week'] = week
            processed.append(article)

    with open(f'/home/jon/Desktop/thesis/Data/Articles/Annotated/{year}_annotated.json', 'w') as f:
        json.dump(processed, f)

    with open(f'/home/jon/Desktop/thesis/Data/Articles/Annotated/{year+1}_addendum.json', 'w') as f:
        json.dump(next_year, f)


def clean_date(date):
    return datetime.strptime(date.replace(',', ''), '%b %d %Y')


def get_week(date_map, date):
    for week in date_map:
        if date in date_map[week]:
            return week

    return None


if __name__ == "__main__":
    main()
