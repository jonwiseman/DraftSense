import os
import json
import pandas as pd
import logging
import pickle


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)  # logging info

    with open(r'../Data/Dataset/comments.json') as f:       # load comment dataset
        comments = json.load(f)

    if os.path.exists(r'../Data/Dataset/labeling_progress.pickle'):     # loading an existing pickle
        logging.info('Loading exsiting pickle...')
        with open(r'../Data/Dataset/labeling_progress.pickle', 'rb') as f:
            df = pickle.load(f)
        flag = check_dataset(df, comments)
        if flag == 1:
            logging.error('Exiting without saving changes.')
            return 1
    else:       # first time creation
        df = pd.DataFrame(comments)     # create new DataFrame

    indexes = df[df['label'] == -1].index       # get remaining indexes for labeling
    logging.info(f'{len(indexes)} comments are unlabeled')

    for comment, index in comment_generator(df, indexes, comments):     # iterate through comments
        print(comment)      # print the comment for viewing
        flag = handle_response(df, index, comments)     # check to make sure that labels match up
        if not flag:
            logging.error('Error in processing comment.  No changes will be saved')
            raise LabelingError


def comment_generator(df, indexes, comments):
    cur_index = indexes[0]
    response = 'y'
    while response == 'y' and cur_index < len(indexes):
        response = str(input('Fetch another comment?'))
        if response == 'y':
            yield df.iloc[cur_index]['comment'], cur_index
            cur_index += 1
        elif response == 'n':
            exit_labeling(df, comments)
        else:
            while response != 'y' and response != 'n':
                response = str(input('Invalid command.  Fetch another comment?'))


def handle_response(df, index, comments):
    response = str(input('Please rate the comment: '))

    while not response.isnumeric() or (int(response) < 1 or int(response) > 4):
        response = str(input('Please rate the comment: '))

    response = int(response)
    df.at[index, 'label'] = response
    comments[index]['rating'] = response
    return df.iloc[index]['comment'] == comments[index]['comment']


def exit_labeling(df, comments):
    with open(r'../Data/Dataset/labeling_progress.pickle', 'wb') as f:
        pickle.dump(df, f)
    with open(r'../Data/Dataset/comments.json', 'w') as f:
        json.dump(comments, f)


def check_dataset(df, comments):
    if len(df) != len(comments):
        return 1

    mismatched = []
    for i in range(len(df)):
        if df.iloc[i]['label'] != comments[i]['label']:
            mismatched.append(i)

    if len(mismatched) > 0:
        logging.error(f'Mismatched comments at positions: {mismatched}')
        return 1

    return 0


class LabelingError(Exception):
    """Labels do not match up"""


if __name__ == '__main__':
    main()
