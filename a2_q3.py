# a1_q2.py
# Cameron Savage - 301310824

import csp
from search import *
import time

from a2_q1 import rand_graph
from a2_q2 import check_teams

def backtracking_search(csp, select_unassigned_variable = csp.first_unassigned_variable,
                        order_domain_values = csp.unordered_domain_values, 
                        inference = csp.no_inference):
    """Redefinition of backtracking_search from csp.py to include counting of assignments and
    unassignments"""

    def backtrack(assignment: dict):
        numAssignments = 0
        numUnassignments = 0

        if len(assignment) == len(csp.variables):
            return [assignment, numAssignments, numUnassignments]
        var = select_unassigned_variable(assignment, csp)

        for value in order_domain_values(var, assignment, csp):

            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                numAssignments += 1
                #print("Current # of assignments: " + str(numAssignments))
                removals = csp.suppose(var, value)

                if inference(csp, var, value, assignment, removals):
                    #print("calling recursion...")
                    result = backtrack(assignment)
                    #print("old # of assignments: " + str(numAssignments))
                    numAssignments += result[1]
                    numUnassignments += result[2]
                    #print("new # of assignments: " + str(numAssignments))
                    
                    if result[0] is not None:
                        return [result[0], numAssignments, numUnassignments]
                csp.restore(removals)

        csp.unassign(var, assignment)
        numUnassignments += 1
        return [None, numAssignments, numUnassignments]

    result = backtrack({})
    print("Total # of assignments: " + str(result[1]))
    print("Total # of unassignments: " + str(result[2]))
    assert result[0] is None or csp.goal_test(result[0])
    return result

def run_q3(hardcoded = False): 
    n = 31
    cycles = 5
    # outer: cycle # ; inner: graph instance
    totalRuntime = []
    totalAssignments = []
    totalUnassignments = []
    totalTeams = []

    for i in range(cycles):
        graphs = [rand_graph(0.8, n), rand_graph(0.8, n), rand_graph(0.8, n),
                  rand_graph(0.8, n), rand_graph(0.8, n), rand_graph(0.8, n)]
        
        # stores data from each solution
        runtime = []
        assignments = []
        unassignments = []
        teams = []

        colours = list(range(31))

        for graph in graphs:
            cspPuzzle = csp.MapColoringCSP(colours, graph)
            
            startTime = time.time()
            result = backtracking_search(cspPuzzle)
            elapsedTime = time.time() - startTime

            runtime.append(elapsedTime)
            print("Solution Corect? " + str(check_teams(graph, result[0])))
            # print(cspPuzzle.neighbors)
            # print(result)
            # print(str(check_teams(cspPuzzle.neighbors, result)))

        totalRuntime.append(runtime)


run_q3()