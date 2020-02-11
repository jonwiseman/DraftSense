import argparse
import logging
import glob
import json


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)  # logging info
    parser = argparse.ArgumentParser(description='Prepare the dataset for labeling by consolidating all .json files '
                                                 'into one large .json file, called comments.json.  The consolidated '
                                                 'file will be stored under Data/Datasets, and serves as the labeled '
                                                 'dataset file.')

    args = parser.parse_args()  # parse arguments (for this file, this will just process the help argument)

    paths = glob.glob(r'../Data/Threads/*.json')

    consolidated = []  # consolidated .json files
    for path in paths:  # for each player in the Threads folder...
        player_name = path.replace('\\', '/').split('/')[-1].split('.json')[0]  # Get the name (helps with labeling)
        with open(path) as f:  # open the corresponding .json file
            comments = json.load(f)
        for comment in comments:  # keep the subject, comment, and label
            consolidated.append({'subject': player_name,
                                 'comment': comment['comment'],
                                 'label': -1})  # all labels are initialized to -1 (represents an unlabeled file)

    with open(r'../Data/Dataset/comments.json', 'w') as f:  # dump the new .json file
        json.dump(consolidated, f)


if __name__ == '__main__':
    main()
