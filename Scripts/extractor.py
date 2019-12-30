import glob
import pandas as pd
import pickle
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Extract football entities and mappings from Kaggle dataset')
    parser.add_argument('y', metavar='YEAR', type=int, help='Season year')
    args = parser.parse_args()

    year = args.y

    file_names = glob.glob(r'../Data/Kaggle CSV Files/Stats/*.csv')
    master_frame = pd.read_csv(file_names[0])
    master_frame = master_frame[master_frame['Year'] == year]
    master_frame = master_frame[['Name', 'Team']]

    for file in file_names[1:]:
        frame = pd.read_csv(file)
        frame = frame[frame['Year'] == year]
        frame = frame[['Name', 'Team']]
        master_frame = master_frame.merge(frame, how='outer')

    master_frame['Name'] = master_frame['Name'].apply(lambda x: x.split(', ')[1] + ' ' + x.split(', ')[0])

    full_names = []
    team_names = []
    city_names = []
    players_teams = master_frame.set_index(keys='Name', inplace=False).to_dict()['Team']  # Players-teams dictionary

    teams = list(master_frame['Team'].unique())  # List of all teams
    aliases = {}  # Dictionary mapping football aliases to organizations
    for team in teams:
        full_names.append(team)  # Add team name to entities list

        short_name = team.split()[-1]  # Add short name
        team_names.append(short_name)
        aliases[short_name] = team  # Map short name to team name

        if len(team.split()) == 3:  # Cities with two names (ex. 'San Francisco')
            aliases[team.split()[0] + ' ' + team.split()[1]] = team  # Map city name to team name
            if team.split()[0] + ' ' + team.split()[1] != 'New York':
                city_names.append(team.split()[0] + ' ' + team.split()[1])  # ERROR: NEW YORK GETS MESSED UP
        else:  # Cities with one name (ex. 'Denver')
            aliases[team.split()[0]] = team
            city_names.append(team.split()[0])

    if not os.path.exists(fr'../Data/Pickles/teams.pickle'):
        pickle.dump(full_names, open(f'../Data/Pickles/teams.pickle', "wb"))
    if not os.path.exists(fr'../Data/Pickles/team_names.pickle'):
        pickle.dump(team_names, open(f'../Data/Pickles/team_names.pickle', "wb"))
    if not os.path.exists(fr'../Data/Pickles/city_names.pickle'):
        pickle.dump(city_names, open(f'../Data/Pickles/city_names.pickle', "wb"))
    if not os.path.exists(fr'../Data/Pickles/teams_aliases.pickle'):
        pickle.dump(aliases, open(f'../Data/Pickles/teams_aliases.pickle', 'wb'))  # Pickle aliases-teams dictionary
    pickle.dump(players_teams,
                open(f'../Data/Pickles/{year}/players_teams_mapping.pickle', 'wb'))  # Pickle players-teams dictionary


if __name__ == '__main__':
    main()
