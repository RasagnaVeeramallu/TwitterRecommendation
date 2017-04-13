import csv
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import mlTesting
import networkx

class edgePrediction(object):
    def __init__(self):
        #self.featuresFile = "C:/Python27_new/files/features.csv"
        self.features = "C:/Python27_new/files/trainingFeatures.csv"
        self.truthValues = "C:/Python27_new/files/trainingTruthValues.csv"
        
    def getTrainingFeatures(self):

        featuresFile = open(self.features, "r")
        self.features = featuresFile.read().split("\n")
        self.features.pop()

        truthValues = open(self.truthValues, "r")
        self.truth = truthValues.read().split("\n")
        self.truth.pop()

        for i in range(len(self.features)):
            self.features[i] = self.features[i].split(",")
            self.truth[i] = int(self.truth[i])

        #print features[0]
            
    def trainClassifier(self):
        self.getTrainingFeatures()

        #self.clf = RandomForestClassifier(n_estimators = 500, oob_score = True)
        #self.clf = RandomForestRegressor(n_estimators = 500, oob_score = True)
        self.clf = KMeans(n_clusters = 2, random_state = 0)
        self.clf.fit(self.features)
        #print self.truth[:10]
        #self.clf.fit(self.features, self.truth)
        """
        print self.clf.labels_
        print self.clf.cluster_centers_
        print len(self.truth)
        print len(self.features)
        """
        
    def predict(self):
        while(True):
            node = raw_input("Enter the node ID to predict: ")
            if node=="done" or node=="exit":
                break
            
            probableConnections = self.getFeatures(node)
            print node, probableConnections

    def getFeatures(self, source):
        graph = mlTesting.getAllUsers()
        g = graph.readGraph()
        print "graph read"
        prunedUsers, score = graph.propagateScore(source, 30)
        probableConnections = []
        for u in prunedUsers:
            features = graph.featureBuilding(source, u[0], score, u[1])[1:]
            testFeatures = [features]
            #print testFeatures
            inFollowees = 1 if source in graph.followees and u[0] in graph.followees[source] else 0
            inFollowers = 1 if source in graph.followers and u[0] in graph.followers[source] else 0
            predictionResult = self.clf.predict(testFeatures)[0]
            if predictionResult==1:
                probableConnections.append(u[0])

        return probableConnections

if __name__ == "__main__":
    p = edgePrediction()
    p.trainClassifier()
    p.predict()
