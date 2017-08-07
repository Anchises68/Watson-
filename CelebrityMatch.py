'''
Created on Aug 4, 2017

@author: alexmireles
'''
import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle):
    twitter_consumer_key = 'bGdNXwpmwC5HZfkeAaBxlD2W8'
    twitter_consumer_secret = '5KEUc9otby7ZyEPq6nRBKGtdg1O1FyF2e88aY64ZvjX3K4LMFq'
    twitter_access_token = '65173395-LN8bPsAjqIHrFtT1JXqLGKeSiKI9Zl1fokmhbJNEI'
    twitter_access_secret = 'piehxmwFJuAoACRiML6YGOlOQQl4vvzgZ7S6QjOv2PBji'

    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)


    statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)

    text = (b'')

    for status in statuses:
        if (status.lang =='en'):
            text += status.text.encode('utf8')
        
    pi_username = '7e9b4315-bf2b-408e-85eb-2723933f4b09'
    pi_password = 'QscNn5JCQgLl'

    personality_insights = PersonalityInsights(username=pi_username, password=pi_password)
    pi_result = personality_insights.profile(text)
    return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
    
def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data
    
user_handle = "@RealAlexJones"
celebrity_handle = "@realDonaldTrump"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

user = flatten(user_result)
celebrity = flatten(celebrity_result)
compared_results = compare(user, celebrity)
sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    print (keys),
    print (user[keys]),
    print ('->'),
    print (celebrity[keys]),
    print ('->'),
    print (compared_results[keys])
