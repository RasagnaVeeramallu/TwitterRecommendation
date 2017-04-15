import csv
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import mlTesting
import networkx
import graphDisplay
from random import shuffle

class edgePrediction(object):
    def __init__(self):
        self.features = "trainingFeatures.csv"
        self.truthValues = "trainingTruthValues.csv"
        self.graphFile = "graph2.graphml"
        self.graph = networkx.read_graphml(self.graphFile)
        
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
    
    def trainClassifier(self):
        self.getTrainingFeatures()

        self.clf = KMeans(n_clusters = 2, random_state = 0)
        self.clf.fit(self.features)
        
    def predict(self):
        while(True):
            node = raw_input("Enter the node ID to predict: ")
            if node=="done" or node=="exit":
                break
            
            probableConnections = self.finalPredictions(node)
            toDisplay = self.returnEdgesForDisplay(node, probableConnections)
            print toDisplay['prediction']
            display = graphDisplay.showRecommendations()
            display.showGraph(node, toDisplay['edges'], toDisplay['prediction'])
            
            
    def pathPredictions(self, source):
        
        kc = networkx.shortest_path(self.graph)
        reco = []
        for node1 in kc:
            for node2 in kc[node1]:
                if source in kc[node1][node2]:
                    for node in kc[node1][node2]:
                        reco.append(node)
                    
        return list(set(reco))
        

    def getFeatures(self, source):
        graph = mlTesting.getAllUsers()
        g = graph.readGraph()
        
        prunedUsers, score = graph.propagateScore(source, 10)
        probableConnections = []
        for u in prunedUsers:
            features = graph.featureBuilding(source, u[0], score, u[1])[1:]
            testFeatures = [features]

            inFollowees = 1 if source in graph.followees and u[0] in graph.followees[source] else 0
            inFollowers = 1 if source in graph.followers and u[0] in graph.followers[source] else 0
            predictionResult = self.clf.predict(testFeatures)[0]
            if predictionResult==1 and inFollowees!=1:
                probableConnections.append(u[0])

        return probableConnections

    def finalPredictions(self, source):
        pathPrediction = self.pathPredictions(source)
        scorePrediction = self.getFeatures(source)
        
        recos = set(scorePrediction).union(set(pathPrediction))
        pageRanks = networkx.pagerank(self.graph)
        
        temp = sorted(recos, key = lambda x: pageRanks[x], reverse = True)[:20]
        if source in temp:
            temp.remove(source)
        shuffle(temp)
        return temp[:5]
        

    def edgeHelper(self, followees, node, depth, res, covered):
        if depth==0 or node in covered:
            return
        tempList = followees[node] if node in followees else []
        covered.append(node)
        for node1 in tempList:
            res["edges"].append((node, node1))
            self.edgeHelper(followees, node1, depth-1, res, covered)
        
    def returnEdgesForDisplay(self, source, predictions):
        graph = mlTesting.getAllUsers()
        g = graph.getFolloweesAndFollowers(self.graph)
        followees = g[0]
        edges = {}
        edges["edges"] = []
        edges["prediction"] = predictions
        covered = []
        
        self.edgeHelper(followees, source, 2, edges, covered)
        return edges

        
if __name__ == "__main__":
    p = edgePrediction()
    p.trainClassifier()
    p.predict()
