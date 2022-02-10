import tweepy

# Variables that contains the credentials to access Twitter API

# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


# Create API object
api = connect_to_twitter_OAuth()

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)

api.update_status("Test tweet from Tweepy")

