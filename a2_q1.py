# a1_q1.py
# Cameron Savage - 301310824

import random

def check_validity(graph: dict):
    nodeList = range(len(graph))
    
    for node in nodeList:
        neighbours = graph.get(node)

        for adjacent in neighbours:
            adjNeighbours = graph.get(adjacent)
            
            if (node not in adjNeighbours):
                return False
    
    return True

def rand_graph(p: float, n: int):
    random.seed()
    nodeList = list(range(n))
    graph = {}
    pairCounter = 0
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
                pairCounter += 1
                # adjacent node is selected
                # get the neighbour values for node and adjacent node keys
                nodeNeighbours = graph.get(node)
                adjacentNeighbours = graph.get(adjacent)

                #add node to the adjacent node's list
                if (node not in adjacentNeighbours):
                    adjacentNeighbours.append(node)
                    graph.update({adjacent : adjacentNeighbours})

                #add the adjacent node to node's list
                if (adjacent not in nodeNeighbours):
                    nodeNeighbours.append(adjacent)
                    graph.update({node : nodeNeighbours})

    print("Created graph (n, p = " + str(n) + ", "+ str(p) + ") with " + str(pairCounter) + " connected pairs.\nChecking validity..." + str(check_validity(graph)))
    return graph

# rand_graph(0.35, 4)