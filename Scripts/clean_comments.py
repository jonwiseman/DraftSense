import logging
import json
import re


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    with open(r'../Data/Dataset/comments.json') as f:        # open master comments.json file
        comments = json.load(f)

    cleaned_comments = []       # storage for cleaned comments (.json format)
    for comment in comments:        # clean each comment in master comments.json file
        filtered_comment = keep_alphabetical(comment['comment'])
        cleaned_comments.append({
            'subject': comment['subject'],
            'comment': filtered_comment,
            'label': comment['label']
        })

    with open(r'../Data/Dataset/comments.json', 'w') as f:      # write out new comments.json file
        json.dump(cleaned_comments, f)


def keep_alphabetical(text):
    """
    Remove characters that have no value in document clustering.  This includes removing URLs, removing subreddit and
    Reddit user links, emojis, and any other extraneous characters.
    :param text: a Reddit comment (string)
    :return: a cleaned Reddit comment (string)
    """
    if text is None:  # no text was given
        return text

    cleaned = filter_url(text)  # remove URLs
    cleaned = re.sub(r'\n', ' ', cleaned)  # remove newline characters
    cleaned = re.sub(r'[*]', '', cleaned)  # remove asterisks
    cleaned = re.sub(r'\[', '', cleaned)  # remove left brackets
    cleaned = re.sub(r'\]', '', cleaned)  # remove right brackets
    cleaned = re.sub(r'[(]', '', cleaned)  # remove left parentheses
    cleaned = re.sub(r'[)]', '', cleaned)  # remove right parentheses
    cleaned = re.sub(r'[#]+', '', cleaned)  # remove hashtags
    cleaned = re.sub(r'/', ' ', cleaned)  # remove slashes
    cleaned = re.sub(r'"', '', cleaned)  # remove quotation marks
    cleaned = re.sub(r'(~)+', '', cleaned)  # remove tildes
    # cleaned = re.sub(r'[$%^+-@&_¯<>]+', '', cleaned)  # remove other miscellaneous characters
    cleaned = re.sub(r'\\', '', cleaned)  # remove back slashes
    cleaned = remove_emoji(cleaned)  # remove emojis

    return cleaned


def filter_url(text):
    """
    Remove URLs from a given string
    :param text: string of text
    :return: string of text without URLs
    """
    return re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', text)


def remove_emoji(string):
    """
    Remove emojis from a string.  Source: https://stackoverflow.com/a/49146722.
    :param string: text string
    :return: text string without emojis
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', string)


if __name__ == '__main__':
    main()
