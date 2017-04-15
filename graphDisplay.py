import matplotlib.pyplot as plt
import networkx
import prediction

class showRecommendations(object):
    def __init__(self):
        self.graph = networkx.DiGraph()
        self.pos = networkx.spring_layout(self.graph)

    def showGraph(self, source, normalEdges, predictedNodes):

        self.graph.add_edges_from(normalEdges)

        ##building recomendation List
        recosEdges = []
        s = [source]
        nodes = []

        for node in normalEdges:
            if node[0] not in nodes and node[0]!=source:
                nodes.append(node[0])

            if node[1] not in nodes and node[1]!=source:
                nodes.append(node[1])
            

        for node in predictedNodes:
            recosEdges.append((source, node))

        self.graph.add_nodes_from(s)
        self.graph.add_nodes_from(nodes)
        self.graph.add_nodes_from(predictedNodes)
        self.graph.add_edges_from(normalEdges)
        self.graph.add_edges_from(recosEdges)
        
        self.pos = networkx.spring_layout(self.graph)
        networkx.draw_networkx_nodes(self.graph, self.pos, nodelist = s, node_color='g')        
        networkx.draw_networkx_nodes(self.graph, self.pos, nodelist = nodes, node_color='y', alpha = 0.4, node_size = 200)
        networkx.draw_networkx_nodes(self.graph, self.pos, nodelist = predictedNodes, node_color='c')

        networkx.draw_networkx_edges(self.graph, self.pos, edgelist = normalEdges, edge_color = 'r', alpha = 0.2)
        networkx.draw_networkx_edges(self.graph, self.pos, edgelist = recosEdges, edge_color = 'b')
        
        networkx.draw_networkx_labels(self.graph, self.pos, font_size=3)

        plt.axis('off')
        plt.savefig('recommend.png')
        plt.show()
    
        
