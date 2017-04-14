import tweepy
import csv
import traceback
import json
import unicodedata
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import time
import networkx
import sklearn
import numpy
import scipy
from sklearn.metrics import jaccard_similarity_score
import random


class getAllUsers(object):
    def __init__(self):
        """
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
        """
        self.userDetailsFile = "C:/Python27_new/files/users2.csv"
        self.relationsFile = "C:/Python27_new/files/relationsNew.csv"
        self.graphFile = "C:/Python27_new/files/graph2.graphml"
        self.featuresFile = "C:/Python27_new/files/features.csv"
        
    def readGraph(self):
        self.readingUsersFile()
        self.graph = networkx.read_graphml(self.graphFile)
        (self.followees, self.followers) = self.getFolloweesAndFollowers(self.graph)
        self.pageRanks = networkx.pagerank(self.graph)
        self.katz = networkx.katz_centrality(self.graph)
        self.paths = networkx.shortest_path(self.graph)
        return self.graph
                    
    def getFolloweesAndFollowers(self, graph):
        followees = {}
        followers = {}
        
        for node in networkx.edges_iter(graph):
            if node[0] in followees:
                followees[node[0]].append(node[1])
            else:
                followees[node[0]] = [node[1]]

            
            if node[1] in followers:
                followers[node[1]].append(node[0])
            else:
                followers[node[1]] = [node[0]]

        return followees, followers

    def readingUsersFile(self):
        readFile = open(self.userDetailsFile, "r")
        users = readFile.read().split("\n")
        users.pop()
        users.pop(0)

        friendsPercentage = {}
        favoritePercentage = {}
        
        for user in users:
            userInfo = user.split(",")
            """
            0 - user id
            1 - screen name
            2 - name
            3 - followers
            4 - listed count
            5 - status count
            6 - friends count
            7 - favorite count
            8 - location
            """
            try:
                friendsPercentage[userInfo[0]] = long(userInfo[6])/float(userInfo[3])
            except:
                friendsPercentage[userInfo[0]] = 0.0082

            try:
                favoritePercentage[userInfo[0]] = long(userInfo[7])/float(userInfo[5])
            except:
                favoritePercentage[userInfo[0]] = 0.219

        self.friends = friendsPercentage
        self.favorites = favoritePercentage
        

    def scorePropagation(self):
        writeFile = open(self.featuresFile, "wb")
        csvWriter = csv.writer(writeFile, delimiter = ",")
        
        for user in networkx.nodes(self.graph):
            #print user
            prunedUsers, score = self.propagateScore(user, 10)

            for u in prunedUsers:
                features = self.featureBuilding(user, u[0], score, u[1])
                featureRow = [user, u[0]]
                featureRow+=features
                
                csvWriter.writerow(featureRow)
                print "Features added for: {} - {}".format(user, u[0])
            
        writeFile.close()
        
    def propagateScore(self, user, limit):
        scores = {}
        followees = self.followees[user] if user in self.followees else []
        followers = self.followers[user] if user in self.followers else []
        #print followees, followers
        scoreToPropagate = 1.0/(len(followees)+len(followers))

        for u in followees+followers:
            self.propagateScoreHelper(scores, u, scoreToPropagate, 1)
            scores[u] = (scores[u] if u in scores else 0) + scoreToPropagate/2
        
        return sorted(scores.items(), key=lambda x: x[1], reverse = True)[:limit], scores[user] if user in scores else 0.0

    def propagateScoreHelper(self, scores, user, score, currIter):
        if currIter<3 and score>0:
            followees = self.followees[user] if user in self.followees else []
            followers = self.followers[user] if user in self.followers else []

            scoreToPropagate = score/(len(followees) + len(followers))

            for u in followees:
                self.propagateScoreHelper(scores, u, scoreToPropagate, currIter+1)
                scores[u] = (scores[u] if u in scores else 0) + scoreToPropagate/2


            for u in followers:
                self.propagateScoreHelper(scores, u, scoreToPropagate, currIter+1)
        

    def featureBuilding(self, source, destination, scoreSource, scoreDestination):
        ##Feature 0 : does source follow destination or not
        ##Feature 1 : does destination follow source or not
        ##Feature 2, 3: number of followers of source and destination
        ##Feature 4, 5: number of followees of source and destination
        ##Feature 6, 7: ratio of followers to followees or source and destination
        ##Feature 8, 9: scores of source and destination
        ##Feature 10: number of followers in common
        ##Feature 11: number of followees in common
        ##Feature 12, 13: percentage of friends for source and destination
        ##Feature 14, 15: Percentage of favorites for source and destination
        ##Feature 16, 17: Page rank of source and destination
        ##Feature 18, 19: Katz similarity of source and destination 
        ##Feature 20: Shortest Path Length from source and destination
        
        
        features = []
        ##0
        if destination in (self.followees[source] if source in self.followees else []):
            feat0 = 1
        else:
            feat0 = 0
        features.append(feat0)
    
        ##1
        if source in (self.followees[destination] if destination in self.followees else []):
            feat1 = 1
        else:
            feat1 = 0
        features.append(feat1)
    
        ##2, 3
        followees1 = self.followees[source] if source in self.followees else []
        feat2 = len(followees1)
        features.append(feat2)
        
        followees2 = self.followees[destination] if destination in self.followees else []
        feat3 = len(followees2)
        features.append(feat3)

        ##4, 5
        followers1 = self.followers[source] if source in self.followers else []
        feat4 = len(followers1)
        features.append(feat4)
        
        followers2 = self.followers[destination] if destination in self.followers else []
        feat5 = len(followers2)
        features.append(feat5)
        
        ##6, 7
        if len(followers1)==0:
            feat6 = -1.0
        else:
            feat6 = len(followees1)/float(len(followers1))
        features.append(feat6)

        if len(followers2)==0:
            feat7 = -1.0
        else:
            feat7 = len(followees2)/float(len(followers2))
        features.append(feat7)
        
        ##8, 9
        feat8 = scoreSource
        features.append(feat8)
        
        feat9 = scoreDestination
        features.append(feat9)

        ##10, 11
        feat10 = len(set(followees1).intersection(followees2))
        features.append(feat10)
        
        feat11 = len(set(followers1).intersection(followers2))
        features.append(feat11)
        
        ##12, 13
        feat12 = self.friends[source] if source in self.friends else 0.0082
        features.append(feat12)

        feat13 = self.friends[destination] if destination in self.friends else 0.0082
        features.append(feat13)
        
        ##14, 15
        feat14 = self.favorites[source] if source in self.favorites else 0.219
        features.append(feat14)
        
        feat15 = self.favorites[destination] if destination in self.favorites else 0.219
        features.append(feat15)

        ##16, 17
        feat16 = self.pageRanks[source]
        features.append(feat16)

        feat17 = self.pageRanks[destination]
        features.append(feat17)

        ##18, 19
        feat18 = self.katz[source]
        features.append(feat18)

        feat19 = self.katz[destination]
        features.append(feat19)

        ##20
        feat20 = len(self.paths[source][destination]) if source in self.paths and destination in self.paths[source] else 0
        features.append(feat20)
        
        return features
        
        
    def train(self):
        self.scorePropagation()
        
        
if __name__=="__main__":
    t = getAllUsers()
    graph = t.readGraph()
    t.train()
