import networkx
import numpy
import matplotlib.pyplot as plt
import csv
import traceback
import d3py
from flask import Flask
from flask import render_template

class extractingData(object):
    def __init__(self):
        self.userFile = "C:/Python27_new/files/users.csv"
        self.edgesFile = "C:/Python27_new/files/relations.csv"
        self.pageRankFile = "C:/Python27_new/files/pageRank1.csv"
        self.followersCount = {}
        self.listsCount = {}
        self.friendsCount = {}
        def userLabels():
            userDict = {}
            readFile = open(self.userFile, "r")
            text = readFile.read().split('\n')
            text.pop()
            i = 0
            for line in text:
                fields = line.split(",")
                userDict[fields[0]] = fields[1]
                self.followersCount[fields[0]] = fields[3]
                self.listsCount[fields[0]] = fields[4]
                self.friendsCount[fields[0]] = fields[6]
            
            readFile.close()
            return userDict

        self.labels = userLabels()
        self.userFollows = {}
        self.userFollowees = {}

    def buildEdges(self):
        userFollows = {}
        userFollowees = {}
        readFile = open(self.edgesFile, "r")
        text = readFile.read().split("\n")
        text.pop()

        for edge in text:
            ends = edge.split(",")
            if ends[1]=="":
                continue
            if ends[0] in userFollows:
                userFollows[ends[0]].append(ends[1])
            else:
                userFollows[ends[0]] = [ends[1]]

            if ends[1] in userFollowees:
                userFollowees[ends[1]].append(ends[0])
            else:
                userFollowees[ends[1]]= [ends[0]]

        
        self.userFollows = userFollows
        self.userFollowees = userFollowees
        print "edges constructed"
        return userFollows

    def buildGraph(self, edges):
        graph = networkx.DiGraph(edges)
        networkx.write_graphml(graph, "graph2.graphml")
        return graph
    
    def calculatingPageRank(self, graph):
        d = 0.8
        iters = 3

        pageRanks = {}
        totalNodes = len(graph.nodes())

        for node in graph.nodes():
            pageRanks[node] = 1.0/totalNodes

        for i in range(iters):
            print "iteration: ", i
            newPageRanks = {}
            for node in graph.nodes():
                print node, i
                newRank = (1-d)/totalNodes
                for node1 in graph.nodes():
                    if node in graph.neighbors(node1):
                        newRank = newRank + d*(pageRanks[node1]/len(graph.neighbors(node1)))

                newPageRanks[node] = newRank
            pageRanks = newPageRanks

        return pageRanks


if __name__ == "__main__":
    tw = extractingData()
    edges = tw.buildEdges()
    graph = tw.buildGraph(edges)
    
    ranks = tw.calculatingPageRank(graph)
            
        
