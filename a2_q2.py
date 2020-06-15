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
                if csp_sol.get(adjNode) == nodeTeam:
                    return False

    return True

