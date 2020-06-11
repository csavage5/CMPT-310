# a1_q2.py
# Cameron Savage - 301310824

def check_teams(graph: dict, csp_sol: dict):
    graphSize = len(graph)

    for node in range(graphSize):
        nodeValue = graph.get(node)
        nodeTeam = csp_sol.get(node)

        #verify all adjacent nodes are on different teams
        for adjNode in nodeValue:
            # if adjNode < node, it has already been checked
            if adjNode > node:
                #print("Adjacent node " + str(adjNode) + "'s team: " + str(csp_sol.get(adjNode)) + " | current node " + str(node) + "'s team: " + str(nodeTeam))
                if csp_sol.get(adjNode) == nodeTeam:
                    return False

    return True

# graph = {1: [0, 2], 0: [1, 3], 3: [0], 2: [1]}
# sol = {0:1, 1:0, 2:1, 3:0}

# print(check_teams(graph, sol))
