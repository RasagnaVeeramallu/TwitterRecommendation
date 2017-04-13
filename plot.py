import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
pos = nx.spring_layout(G)

# Picked Node
nodeSet1 = [1]
# All the others
nodeSet2 = [2,3,4,5,6,7]
nodeSet3 = [8,10,11,12]
# Recommended
nodeSet4 = [9,12]
# First level neighbours
edgeSet1 = [(1,2),(1,3),(1,5),(1,7)]
# Second level
edgeSet2 = [(2,8),(2,12),(7,11),(3,10)]
# Recommended Link
edgeSet3 = [(1,12),(1,9)]

G.add_nodes_from(nodeSet1)
G.add_nodes_from(nodeSet2)
G.add_nodes_from(nodeSet3)

G.add_edges_from(edgeSet1)
G.add_edges_from(edgeSet2)
G.add_edges_from(edgeSet3)

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, nodelist = nodeSet1, node_color = 'r')
nx.draw_networkx_nodes(G, pos, nodelist = nodeSet2, node_color = 'y')
nx.draw_networkx_nodes(G, pos, nodelist = nodeSet3, node_color = 'c')
nx.draw_networkx_nodes(G, pos, nodelist = nodeSet4, node_color = 'g')
nx.draw_networkx_edges(G, pos, edgelist = edgeSet1, edge_color = 'y')
nx.draw_networkx_edges(G, pos, edgelist = edgeSet2, edge_color = 'c')
nx.draw_networkx_edges(G, pos, edgelist = edgeSet3, edge_color = 'g')
nx.draw_networkx_labels(G,pos)

plt.axis('off')
plt.savefig("recommend.png")
plt.show()
