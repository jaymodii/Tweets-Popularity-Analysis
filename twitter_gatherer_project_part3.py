#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 21:03:00 2020
Updated 2021-10-08 to work with Tweepy v4, as 3-->4 introduced breaking changes
Updated 2022-01-27 to work only with tweepy v4, and use the v2 twitter api

@author: silviana amethyst

This file collects data from twitter, and saves it to a JSON file.  
It requires a file called `twitter_credentials.py` to be on the path (the current
working directory is on the path), and that file must contain at least the following string variables:
    * bearer token

This file writes a file called `twitter_data.json`.  Saving of this file is 
goverened by the Twitter developer license agreement.

You'll use this same file for all three parts of the project.
"""

#%% declare the search query for recent tweets
query = 'Machine Learning'



#%% setup, do once
import tweepy, requests

if tweepy.__version__.split('.')[0]=='4':
    TweepyException = tweepy.errors.TweepyException
else:
    raise ImportError('`twitter_gatherer_project_part3.py` only works with tweepy major version 4.')

from twitter_credentials import bearer_token 

# Create a Client object, and connect to the Twitter API using the 
# authentication information from your `twitter_credentials.py` file
# see https://docs.tweepy.org/en/stable/client.html

# in this gatherer, we're using the `requests.Response` return_type, so that we can easily get the json for the returned data.
# I would have used `tweepy.Response` for Project Parts 2 and 3, so that the data type of tweets isn't dictionaries, but `Tweet` objects,
# but serialization of them using `dill` is broken (see https://github.com/tweepy/tweepy/issues/1792),
# so we're sticking with `requests.Response` and JSON for the entire project.
client = tweepy.Client(bearer_token=bearer_token, return_type = requests.Response)

#%% define the `collect` function.  should only need to do once.

def collect(client, query, num_to_collect=300):
    """
    A simple function for performing a search (of recent tweets only) on twitter, until you have a certain 
    number of tweets.
    """

    # some general fixed parameters for the search we'll perform.  in Part 2 and Part 3, you may have more freedom to customize.

    num_at_a_time = 100
    additional_fields = ['text','author_id', 'created_at', 'entities']
    expansions = ['referenced_tweets.id','attachments.media_keys', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id']
    media_fields = ['media_key', 'type', 'preview_image_url', 'alt_text']

    # a helper function
    def get_min_tweet_id(tweets):
        if tweets.json()['meta']['result_count']==0:
            raise ValueError("result_count==0")
        return min([int(t['id']) for t in tweets.json()['data']])

    # next, we curry a bit to simplify down below a bit
    # see https://docs.tweepy.org/en/stable/client.html#search-tweets, and find-in-page "search_recent_tweets"
    search_function_first_iteration = lambda: \
        client.search_recent_tweets(query = query, \
            max_results=num_at_a_time, \
            tweet_fields=additional_fields, \
            media_fields=media_fields, \
            expansions=expansions)

    # differs only in that it has the until_id field
    search_function_subsequent_iterations = lambda min_id: \
        client.search_recent_tweets(query = query, \
            max_results=num_at_a_time, \
            tweet_fields=additional_fields, \
            media_fields=media_fields, \
            expansions=expansions, \
            until_id=min_id, \
        )

    tweet_list = []
    
    try:
        new_tweets = search_function_first_iteration()
        min_id = get_min_tweet_id(new_tweets)
        tweet_list.extend(new_tweets.json()['data'])
    except ValueError as e:
        print(f'found no tweets with query {query}')
        return tweet_list


    while len(tweet_list) < num_to_collect:
        try:
            print(f"have {len(tweet_list)}, searching for more")

            new_tweets = search_function_subsequent_iterations(min_id)
            min_id = get_min_tweet_id(new_tweets)
            tweet_list.extend(new_tweets.json()['data'])


        except TweepyException as e:
            print("Exception: ", e)
            raise e

        except ValueError as e:
            print("Could not find any more tweets!")
            break
        else:
            if not new_tweets:
                print("Could not find any more tweets!")
                break

    print(f'done searching, have {len(tweet_list)} tweets for query "{query}"')
    return tweet_list

#%% actually search for the data.  result is a list of json-like objects
twitter_data = collect(client, query, num_to_collect=300)

#%% write the data

import json
with open('twitter_data_project_part3.json', 'w',encoding='utf8') as out:
    json.dump(twitter_data,out,indent=4, ensure_ascii=False)
