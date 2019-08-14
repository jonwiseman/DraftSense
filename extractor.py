import glob
import pandas as pd
import pickle
import argparse


def main():
    parser = argparse.ArgumentParser(description='Extract football entities and mappings from Kaggle dataset')
    parser.add_argument('y', metavar='YEAR', type=int, help='Season year')
    args = parser.parse_args()

    year = args.y

    file_names = glob.glob('/home/jon/Desktop/thesis/csv/*.csv')
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
                city_names.append(team.split()[0] + ' ' + team.split()[1])  # ERROR: NEW YORK GETS FUCKED UP
        else:  # Cities with one name (ex. 'Denver')
            aliases[team.split()[0]] = team
            city_names.append(team.split()[0])

    pickle.dump(full_names, open(f'/home/jon/Desktop/thesis/{year}/full_names.p', "wb"))
    pickle.dump(team_names, open(f'/home/jon/Desktop/thesis/{year}/team_names.p', "wb"))
    pickle.dump(city_names, open(f'/home/jon/Desktop/thesis/{year}/city_names.p', "wb"))
    pickle.dump(players_teams,
                open(f'/home/jon/Desktop/thesis/{year}/players_teams_mapping.p', 'wb'))  # Pickle players-teams dictionary
    pickle.dump(aliases, open(f'/home/jon/Desktop/thesis/{year}/teams_aliases.p', 'wb'))  # Pickle aliases-teams dictinoary
    pickle.dump(teams, open(f'/home/jon/Desktop/thesis/{year}/teams.p', 'wb'))  # Pickle list of teams


if __name__ == '__main__':
    main()
