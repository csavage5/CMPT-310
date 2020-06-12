# a1_q1.py
# Cameron Savage - 301310824

import random

# def check_validity(graph: dict):
#     nodeList = range(len(graph))
    
#     for node in nodeList:
#         neighbours = graph.get(node)

#         for adjacent in neighbours:
#             adjNeighbours = graph.get(adjacent)
            
#             if (node not in adjNeighbours):
#                 return False
    
#     return True


def rand_graph(p: float, n: int):
    random.seed()
    nodeList = list(range(n))
    #print(nodeList)
    graph = {}
    #init graph
    for node in range(n):
        graph.update({node : []})

    # populate graph
    for node in nodeList:

        for adjacent in nodeList:
            randChoice = random.randint(0, 100) * 0.01

            # check from the smaller node for the pair - avoids double-checking
            # pairs of nodes
            if node < adjacent and randChoice < p:
                # adjacent node is selected
                # get the current values for node and adjacent node
                nodeValue = graph.get(node)
                # if nodeValue == None:
                #     nodeValue = []
                
                adjacentValue = graph.get(adjacent)
                # if adjacentValue == None:
                #     adjacentValue = []

                #add node to the adjacent node's list
                if (node not in adjacentValue):
                    adjacentValue.append(node)
                    graph.update({adjacent : adjacentValue})

                #add the adjacent node to node's list
                if (adjacent not in nodeValue):
                    nodeValue.append(adjacent)
                    graph.update({node : nodeValue})

    #print("Friendship dictionary: ")          
    #print(graph)
    #print("Valid? " + str(check_validity(graph)))
    return graph
#print (3 not in [])
# rand_graph(0.35, 4)