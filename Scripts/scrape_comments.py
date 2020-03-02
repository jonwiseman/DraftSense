import argparse
import configparser
import logging
import praw
import json


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)  # logging info
    parser = argparse.ArgumentParser(description='Scrape comments from Reddit using PRAW, a registered Reddit account, '
                                                 'and a valid Reddit dev application.  Scraped comments will be stored '
                                                 'in .json format (ex. Mahomes.json), in the Data/Threads folder.'
                                                 'Only one player at a time may be specified.')
    config = configparser.ConfigParser()  # reading configuration file (to get Reddit account and application details)

    parser.add_argument('n', metavar='NAME', type=str, nargs='+', help='Player name')
    args = parser.parse_args()  # parse arguments

    name = ' '.join(args.n)  # get name of player to scrape
    config.read(r'..\configuration.conf')  # read and parse configuration file

    reddit = praw.Reddit(client_id=config['Reddit']['client_id'],
                         client_secret=config['Reddit']['client_secret'],
                         password=config['Reddit']['password'],
                         user_agent=config['Reddit']['user_agent'],
                         username=config['Reddit']['username'])  # create Reddit instance

    nfl = reddit.subreddit('nfl')  # get the instance of the r/nfl subreddit

    post_id = None  # numeric post ID of draft thread
    for submission in nfl.search(f'author:NFL_Mod title:"{name}"'):  # search the official moderator threads
        post_id = submission.id

    logging.info(f'Submission found with id: {post_id}')

    if post_id is None:  # player not found in the mod's post history
        logging.error('Name not found in u/NFL_Mod post history.  Comment data cannot be scraped.')
        raise PlayerError

    logging.info('Gathering comments...')

    post = reddit.submission(id=post_id)
    post.comments.replace_more(limit=None)  # gather all comments

    comments = []
    for top_level_comment in post.comments:  # scrape all top- and second-level comments
        for second_level_comment in top_level_comment.replies:
            comments.append({'comment_id': second_level_comment.id,
                             'post_id': second_level_comment.submission.id,
                             'comment': second_level_comment.body})
        comments.append({'comment_id': top_level_comment.id,
                         'post_id': top_level_comment.submission.id,
                         'comment': top_level_comment.body})

    logging.info(f'{len(comments)} comments scraped for {name}')
    with open(fr'..\Data\Threads\{name.split()[-1]}.json', 'w') as f:  # dump comments in .json file
        json.dump(comments, f)  # dump scraped data in .json format


class PlayerError(Exception):
    """Name not found"""


if __name__ == '__main__':
    main()
