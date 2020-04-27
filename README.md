[![CodeFactor](https://www.codefactor.io/repository/github/jonwiseman/draftsense/badge)](https://www.codefactor.io/repository/github/jonwiseman/draftsense)

This repository contains files related to DraftSense, a sentiment analyzer developed for CS495: Honors Projects in Computing.

## Goal  
There are two primary goals for DraftSense:

1. Produce a labeled sentiment analysis dataset specifically related to the NFL and draft picks  
2. Train a sentiment analyzer for automatic detection of polarity towards a draft pick (positive or negative)  

Additionally, the design of DraftSense was guided by three principles:

* Comprehensive: the ability to collect a large volume of data  
* Specific: collecting data specific to NFL draft picks  
* Accurate: accurately predict sentiment to summarize the public’s reactions to NFL draft picks  


## Methodology  
The general pipeline for DraftSense is shown below:

![Processing Pipeline](https://github.com/jonwiseman/DraftSense/blob/master/Docs/Images/DraftSense.png?raw=true)

The r/nfl subreddit has an official moderating bot that posts draft reaction threads;  [here](https://www.reddit.com/r/nfl/comments/8flkos/round_5_pick_4_shaquem_griffin_olb_central/) is an example of a draft reaction thread.  All draft reaction threads are posted by u/NFL_MOD, so finding the relevant thread involves iterating through that account's posts.  Every top- and second-level comment is scraped and stored in relevent .json files.  Comments are consolidated into a master .json file, cleaned, and labeled to produce the sentiment analysis dataset.  There are five labels in this dataset:

* -1: the comment has not been labeled yet (absent for a fully labelled dataset)  
* 1: positive  
* 2: negative  
* 3: joke or meme  
* 4: junk or irrelevant  

The distribution of labels is shown below:

![Label Distribution](https://github.com/jonwiseman/DraftSense/blob/master/Docs/Images/labels.png?raw=true)

Four machine learning models were trained on the labelled dataset.  Each model and its related performance is shown below:

| Model | Performance | 
| ------------- |:-------------:|
| Logistic Regression | 77% |
| Naive Bayes | 65% |
| Random Forest | 77% |
| Support Vector Machine | 84% |

## Files  
Below is an overview of what is contained in each folder, presented in the recommended order of viewing.

**Scripts**  
The "Scripts" folder contains the Python scripts for automated subreddit scraping, comment data cleaning, labeling preparation, and comment labeling.  You can run any of them from the command line.  Also note that a configuration file is needed to parse a user's Reddit account information.  The configuration file MUST be stored in the project's root directory.  The format of this configuration file is as follows:  

[Reddit]  
client_id =  
client_secret =   
password =   
user_agent =   
username =   

The configuration file used for this project is not included, due to security concerns.  For information related to creating a Reddit account and application development, see [this](https://www.reddithelp.com/en) link.  Each script can be run from the command line; running a script with the argument --help will display the script's purpose and parameters.  Below is a description of each Script and its use cases:  

*scrape_comments.py*  
Scrape comments from Reddit using PRAW, a registered Reddit account, and a valid Reddit dev application.  The user must supply the name of the player whose thread is to be scraped as a command line argument.  Scraped comments will be stored in .json format in appropriate folders, under the "Data\Threads" section.  If the desired player is not found, then an error will be returned.

*prepare_labeling.py*  
Consolidate all comment threads into a single master file for ease of cleaning and labeling.  The master .json file will be called "comments.json," and contain the following fields:

* subject: the player the comment is discussing  
* comment: text data of the comment  
* label: the label assigned to the comment

The script itself labels all comments as -1 (unlabeled).  

*clean_comments.py*  
Cleans the text data of all comments by removing emojis, URLs, links to other subreddits and Reddit users, newlines, tabs, and extraneous characters (i.e. non-punctuation characters).  Most of these characters have no value in sentence embedding, and so are removed at this stage.  

*label_comments.py*  
Incrementally label each comment in the dataset.  There are two records kept: comments.json, which is updated as the labeling goes on, and labeling_progress.pickle, which is a pickled DataFrame updated after each labelling session.  If labeling_progress.pickle is present, it is assumed that labeling is in progress; to avoid errors, the two records are compared and any unmatched labels are reported to the user.

**Data**  
The Data folder contains the project's developed dataset and intermediate data.  Intermediate data includes raw, unconsolidated draft threads that have not been processed; these are stored under "Data/Threads"  The dataset is stored under "Data/Dataset;" the labeling_progress.pickle is also stored here.  Finally, the file "Data/'Kaggle CSV Files'" contains additional data from Kaggle that will be used to assess the performance of players after they are drafted.

**Docs**  
The Docs folder contains project documents, such as the project's proposal, milestone reports, and the final report.  The requirements.txt is also stored here.  

**Notebooks**  

*Exploratory Data Analysis*  
Contains some exploratory data analysis on the fully labeled dataset.

*Gensim Sentence Embedding*  
Contains model creation using Sent2Vec as implemented by GenSim.
