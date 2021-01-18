import json
import pandas as pd
import tweepy as tw
import datetime as dt

with open('twitter_credentials.json', 'r') as file:
    data = file.read()

creds = json.loads(data)

auth = tw.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

api = tw.API(auth, wait_on_rate_limit_notify=True)

tweet_dict = {
    'created_at':[],
    'full_text':[],
    'retweet_count':[],
    'favorite_count':[],
    'lang':[]    
}

for status in tw.Cursor(api.user_timeline, screen_name='@CBCGDF_China', tweet_mode="extended").items():
    for key in tweet_dict.keys():
        tweet_dict[key].append(status._json[key])

df = pd.DataFrame.from_dict(tweet_dict)

def convert_date(str_date):
    return dt.datetime.strptime(str_date, '%a %b %d %H:%M:%S +0000 %Y')

df['created_at'] = df['created_at'].apply(convert_date)

df.to_excel('CBCGDF_China_tweet_history.xlsx', index=False)