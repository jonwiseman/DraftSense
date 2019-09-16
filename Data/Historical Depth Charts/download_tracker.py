import pickle


def main():
    tracker = pickle.load(open('tracker.p', 'rb'))
    teams = list(tracker.keys())
    for download in get_next_year(tracker):
        submitted = input(f'Has {download} been saved?')

    pickle.dump(tracker, open('/home/jon/Desktop/thesis/Data/Historical Depth Charts/tracker.p', 'wb'))


def get_next_year(tracker):
    for team in tracker:
        for year in tracker[team]:
            if tracker[team][year] is False:
                if input('Continue download?') == 'y':
                    yield team + ' ' + year
                    tracker[team][year] = True
                else:
                    return


if __name__ == '__main__':
    main()
