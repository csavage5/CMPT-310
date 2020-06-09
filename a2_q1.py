# a1_q1.py
# Cameron Savage - 301310824

import random

def rand_graph(p, n):
    random.seed()
    nodeList = list(range(n))
    #print(nodeList)
    graph = {}
    #graph.update({0:[1,2]})
    # fill graph
    for node in nodeList:

        for adjacent in nodeList:
            randChoice = random.randint(0, 100) * 0.01
            if node != adjacent and randChoice < p:
                # adjacent node is selected
                # get the current values for node and adjacent node
                nodeValue = graph.get(node)
                if nodeValue == None:
                    nodeValue = []
                
                adjacentValue = graph.get(adjacent)
                if adjacentValue == None:
                    adjacentValue = []

                #add node to the adjacent node's list
                if (node not in adjacentValue):
                    adjacentValue.append(node)
                    graph.update({adjacent : adjacentValue})

                #add the adjacent node to node's list
                if (adjacent not in nodeValue):
                    nodeValue.append(adjacent)
                    graph.update({node : nodeValue})
    print("Friendship dictionary: ")          
    print(graph)

    return graph

rand_graph(0.35, 4)