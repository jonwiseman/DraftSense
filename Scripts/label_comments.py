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
    """
    The comment_generator method handles user input and yields comments.  User can input 'y' for fetching
    another comment and 'n' for exiting the program.
    :param df: master DataFrame
    :param indexes: list of indexes corresponding to unlabelled comments
    :param comments: master comments.json file
    :return: yield a comment for labeling
    """
    cur_index = indexes[0]      # index of current comment
    response = 'y'      # assume yielding a comment

    while response == 'y' and cur_index < len(df):     # while user wants to continue and there are still comments
        response = str(input('Fetch another comment?'))     # prompt user for further comment labeling
        if response == 'y':
            yield df.iloc[cur_index]['comment'], cur_index      # fetch another comment
            cur_index += 1      # increment index
        elif response == 'n':
            exit_labeling(df, comments)     # run exit method
        else:
            while response != 'y' and response != 'n':      # user entered an invalid command
                response = str(input('Invalid command.  Fetch another comment?'))


def handle_response(df, index, comments):
    """
    The handle_response method labels a comment based on user feedback.
    :param df: master DataFrame
    :param index: index of current comment
    :param comments: master comments.json file
    :return: True if comment was labeled successfully; false otherwise
    """
    response = str(input('Please rate the comment: '))      # prompt user for score

    while not response.isnumeric() or (int(response) < 1 or int(response) > 4):     # invalid comment score
        response = str(input('Please rate the comment: '))

    response = int(response)
    df.at[index, 'label'] = response        # update DataFrame and .json file
    comments[index]['label'] = response
    return df.iloc[index]['comment'] == comments[index]['comment']      # check to make sure the comments were changed


def exit_labeling(df, comments):
    """
    The exit_labeling method writes out labeling progress.
    :param df: master DataFrame
    :param comments: master comments.json file
    :return:
    """
    with open(r'../Data/Dataset/labeling_progress.pickle', 'wb') as f:      # pickle the DataFrame
        pickle.dump(df, f)
    with open(r'../Data/Dataset/comments.json', 'w') as f:      # write out the DataFrame
        json.dump(comments, f)


def check_dataset(df, comments):
    """
    The check_dataset method runs on a labeling_progress.pickle to make sure all indexes match
    :param df: master DataFrame
    :param comments: master comments.json file
    :return: an error flag (1) if the two records do not match; 0 otherwise
    """
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
