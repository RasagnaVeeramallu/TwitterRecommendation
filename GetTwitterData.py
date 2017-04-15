import tweepy
import csv
import traceback
import json
import unicodedata
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import time

class TwitterData(object):
    def __init__(self):
        ACCESS_TOKEN = '1527563580-eMMTMOFV7vsbQXNSInWfPzDdZvcrxS0s6dWKlx5'
        ACCESS_SECRET = 'GiEr7Tui5fKO7UWVJJXgUYKDyLWbWByZKAjqcIYUXxEGc'
        CONSUMER_KEY = 'CnznZF1paZftiPwdk3NYzCyWZ'
        CONSUMER_SECRET = 'zQHoLrOu6DiWJQDqnTjcnhRCCI1PQ3HOCLAuA3uthf0jfl5lcE'

        ##for twitter
        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        self.twitter_stream = TwitterStream(auth=oauth)

        ##for tweepy
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        self.userDetailsFile = "C:/Python27_new/files/users.csv"
        self.relationsFile = "C:/Python27_new/files/relations.csv"


    def getSampleData(self, tweetCount):
        iterator = self.twitter_stream.statuses.sample()

        ##preparing to write user data to csv file
        #csvFile = open(self.userDetailsFile, "wb")
        #csvWriter = csv.writer(csvFile, delimiter = ",")

        userScreenNames = []
        userIds = []
        
        fileHeader = ['id', 'screen_name', 'name', 'followers_count', 'listed_count', 'statuses_count', 'friends_count', 'favourites_count', 'location']
        #csvWriter.writerow(fileHeader)

        for tweet in iterator:
            
            try:
                userInfo = []
                userInfo.append(tweet['user']['id'])
                userInfo.append(tweet['user']['screen_name'])
                userInfo.append(unicodedata.normalize('NFKD', tweet['user']['name']).encode('ascii','ignore'))
                userInfo.append(tweet['user']['followers_count'])
                userInfo.append(tweet['user']['listed_count'])
                userInfo.append(tweet['user']['statuses_count'])
                userInfo.append(tweet['user']['friends_count'])
                userInfo.append(tweet['user']['favourites_count'])

                if tweet['user']['location']: 
                    userInfo.append(unicodedata.normalize('NFKD', tweet['user']['location']).encode('ascii','ignore'))

                else:
                    userInfo.append("")
                if tweet['user']['followers_count']<=500:
                    #csvWriter.writerow(userInfo)
                    print userInfo
                    userIds.append(tweet['user']['id'])
                    userScreenNames.append(tweet['user']['screen_name'])
                    tweetCount-=1
                
            except:
                print str(traceback.print_exc())
            
            if tweetCount<=0:
                break
        csvFile.close()
        return userIds


    def getFollowersForId(self, userId):
        followers = tweepy.Cursor(self.api.followers, id = userId).items()
        time.sleep(11)
        userFollowers = [user.id for user in followers]
        
        return userFollowers


    def getRelations(self, userIds):
        csvFile = open(self.relationsFile, "wb")
        csvWriter = csv.writer(csvFile, delimiter = ",")
        for userId in userIds:
            followerIdList = self.getFollowersForId(userId)
            for fId in followerIdList:
                csvWriter.writerow([userId, fId])

        csvFile.close()
        

if __name__=="__main__":
    print "Twitter Data"
    twData = TwitterData()
    users = twData.getSampleData(5)
    #twData.getRelations(users)
        
