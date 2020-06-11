# a1_q2.py
# Cameron Savage - 301310824

import csp
from search import *
import time

from a2_q1 import rand_graph
from a2_q2 import check_teams

class CSP(Problem):
    """
    Redefined from csp.py to include member field to track number 
    of backtracking unassignments.
    
    This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases (for example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(n^4) for the
    explicit representation). In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0
        self.nunassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
        self.nunassigns += 1

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print(assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: non conflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

def backtracking_search(csp, select_unassigned_variable = csp.first_unassigned_variable,
                        order_domain_values = csp.unordered_domain_values, 
                        inference = csp.no_inference):
    """Redefinition of backtracking_search from csp.py to include counting of
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
        #print("unassigning...")
        return [None, numAssignments, numUnassignments]

    result = backtrack({})
    #print("Total # of assignments: " + str(result[1]))
    #print("Total # of unassignments: " + str(result[2]))
    assert result[0] is None or csp.goal_test(result[0])
    return result[0]

def run_q3(hardcoded = False): 
    n = 31
    cycles = 5
    # outer: cycle # ; inner: graph instance
    totalRuntime = []
    totalAssignments = []
    totalUnassignments = []
    totalTeams = []

    #for i in range(cycles):
    for i in range(1):
        '''
        graphs = [rand_graph(0.1, n), rand_graph(0.2, n), rand_graph(0.3, n),
                  rand_graph(0.4, n), rand_graph(0.5, n), rand_graph(0.6, n)]
        '''
        n = 15
        cycles = 1
        graphs = [rand_graph(0.4, n)]
        # stores data from each solution
        runtime = []
        assignments = []
        unassignments = []
        teams = []

        colours = list(range(n))

        for graph in graphs:
            
            # test increasing numbers of colour combinations
            result = None
            attemptCounter = 1
            while result == None:
                print("Attempting Backtracking with " + attemptCounter + " teams...")
                cspPuzzle = csp.MapColoringCSP(colours[0:attemptCounter], graph)
                result = backtracking_search(cspPuzzle)
                attemptCounter += 1

            print("Completed with " + str( len( numOfTeams(result) ) ) + " teams")
            print(result)

            #elapsedTime = time.time() - startTime

            # runtime.append(elapsedTime)
            #print("Solution Corect? " + str(check_teams(graph, result[0])))
            # print(cspPuzzle.neighbors)
            # print(result)
            # print(str(check_teams(cspPuzzle.neighbors, result)))

        # totalRuntime.append(runtime)

def numOfTeams(result: dict) :
    size = len(result)
    teams = []

    for i in range(size):
        if result.get(i) not in teams:
            teams.append(result.get(i))

    return teams
run_q3()