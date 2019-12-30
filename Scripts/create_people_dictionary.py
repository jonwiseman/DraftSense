import pandas as pd
import pickle
import json


def main():
    years = [2010, 2011, 2012, 2013]
    teams = ['Dolphins',
             'Jets',
             'Patriots',
             'Bills',
             'Browns',
             'Ravens',
             'Bengals',
             'Steelers',
             'Colts',
             'Titans',
             'Jaguars',
             'Texans',
             'Chargers',
             'Broncos',
             'Chiefs',
             'Raiders',
             'Eagles',
             'Redskins',
             'Giants',
             'Cowboys',
             'Packers',
             'Vikings',
             'Lions',
             'Bears',
             'Falcons',
             'Buccaneers',
             'Panthers',
             'Saints',
             'Rams',
             '49ers',
             'Cardinals',
             'Seahawks']
    people = dict()

    for year in years:
        for team in teams:
            df = pd.read_excel(fr'../Data/Historical Depth Charts/{year}/{team}.xlsx')
            df = df[['Player', 'Pos']]
            df['Player'] = df['Player'].apply(clean_names)

            for player in list(df['Player'].values):
                if player in people:
                    years_dict = people[player]
                else:
                    years_dict = dict()

                years_dict[year] = {'team': team, 'role': df[df['Player'] == player]['Pos'].values[0]}
                people[player] = years_dict

    with open(fr'../Data/Coaches/coaches.json', 'r') as f:
        data = json.load(f)
    for line in data:
        meta = line['Metadata']
        coach = line['Coach']
        segmented = meta.split(' ')
        year = segmented[0]
        team = segmented[1:-1]
        team = team[-1]

        if coach in people:
            years_dict = people[coach]
        else:
            years_dict = dict()

        years_dict[year] = {'team': team, 'role': 'Coach'}
        people[coach] = years_dict

    pickle.dump(people, open(fr'../Data/Pickles/people.pickle', 'wb'))


def clean_names(x):
    full_name = x.split('\\')[0]
    full_name = full_name.replace('*', '')
    full_name = full_name.replace('+', '')
    return full_name


if __name__ == '__main__':
    main()

