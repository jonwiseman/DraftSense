import pickle


def main():
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
             'Seahawks'
             ]
    years = ['2010', '2011', '2012', '2013']

    tracker = dict()
    for team in teams:
        year_dict = dict()
        for year in years:
            year_dict[year] = False
        tracker[team] = year_dict

    pickle.dump(tracker, open('/home/jon/Desktop/thesis/Data/Historical Depth Charts/tracker.p', 'wb'))


if __name__ == '__main__':
    main()
