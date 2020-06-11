# a1_q2.py
# Cameron Savage - 301310824

import csp
from search import *
import time

from a2_q1 import rand_graph
from a2_q2 import check_teams

def MapColoringCSP(colors, neighbors):
    """
    Redefined from csp.py to construct a revised CSP class

    Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = csp.parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), csp.UniversalDict(colors), neighbors, csp.different_values_constraint)

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

def run_q3(hardcoded = False): 
    n = 11
    trials = 5
    # outer index: trial #, inner: graph #
    totalRuntime = []
    totalAssignments = []
    totalUnassignments = []
    totalTeams = []
    totalAcChecks = []

    for _ in range(trials):
        
        graphs = [rand_graph(0.1, n), rand_graph(0.2, n), rand_graph(0.3, n),
                  rand_graph(0.4, n), rand_graph(0.5, n), rand_graph(0.6, n)]
        graphCounter = 1
        #graphs = [rand_graph(0.4, n)]

        # stores data from each trial to append to total lists
        runtime = []
        assignments = []
        unassignments = []
        teams = []
        acChecks = []
        # iterate through to grow colour / team size
        colours = list(range(n))

        for graph in graphs:
            #debug
            # print("Graph:")
            # print(graph)
            deltaChecks = 0
            deltaTime = 0
            elapsedTime = 0
            startTime = 0

            deltaAssigns = 0
            deltaUnassigns = 0

            result = None
            attemptCounter = 1
            print("Solving random graph: n = " + str(n) + ", " + "p = 0." + str(graphCounter))
            while result == None:
                print("--> Attempting with " + str(attemptCounter) + " teams...")
                cspPuzzle = MapColoringCSP(colours[0 : attemptCounter], graph)
                
                # startTime = time.time()
                # #print("----> Number of AC3 checks: " + str(csp.AC3(cspPuzzle)[1]))
                # deltaChecks += csp.AC3(cspPuzzle)[1]
                # elapsedTime = time.time() - startTime
                # deltaTime += elapsedTime

                startTime = time.time()
                result = csp.backtracking_search(cspPuzzle, select_unassigned_variable = csp.mrv,
                                                inference = csp.forward_checking)
                elapsedTime = time.time() - startTime
                deltaTime += elapsedTime

                #cspPuzzle instance is reset every loop, save the # of assigns/unassigns
                deltaAssigns += cspPuzzle.nassigns
                deltaUnassigns += cspPuzzle.nunassigns

                attemptCounter += 1

            print("Found solution in " + str(round(deltaTime, 3)) + " seconds.\n\n")
            graphCounter += 1
            # Display and save information
            runtime.append(deltaTime)
            #print("Completed in " + str(deltaTime) + " seconds")
            teams.append(numOfTeams(result))
            # print(result)
            # print("Completed with " + str( teams[-1] ) + " teams")
            assignments.append(deltaAssigns)
            #print("Total number of Assignments: " + str(assignments[-1]))
            unassignments.append(deltaUnassigns)
            #print("Total number of Unassignments: " + str(unassignments[-1]))
            #print(result)
            #print("Solution is " + str(check_teams(graph, result)))
            acChecks.append(deltaChecks)

            # end of graph loop

        # end of trial loop

        # trial over, display info so far
        totalRuntime.append(runtime)
        totalAssignments.append(assignments)
        totalUnassignments.append(unassignments)
        totalTeams.append(teams)
        totalAcChecks.append(acChecks)
        displayFormattedData(totalRuntime, totalAssignments, totalUnassignments, totalTeams, totalAcChecks)


def numOfTeams(result: dict) -> int:
    numTeams = []
    for i in range(len(result)):
        if result.get(i) not in numTeams:
            numTeams.append(result.get(i))

    return len(numTeams)

def displayFormattedData(time, assigns, unassigns, teams, acChecks):
    compTrials = len(time)
    print("\nCompleted trials #" + str(compTrials * 6 - 5) + " - " + str(compTrials * 6) + ", updating table...")
    print("|  Trial # \t|  Time (seconds)  |  Assigns \t|  Unassigns \t|  AC Checks \t|  # of Teams \t|")

    for trial in range (compTrials):
        for graph in range(len(time[trial])):
            print("     " + str((trial * 6) + (graph + 1)), end = "  \t| ")
            print("    " + str(round(time[trial][graph], 3)), end = " \t| ")
            print("    " + str(assigns[trial][graph]), end = " \t| ")
            print("    " + str(unassigns[trial][graph]), end = " \t| ")
            print("    " + str(acChecks[trial][graph]), end = " \t| ")
            print("    " + str(teams[trial][graph]), end = " \t|\n")
        print("--------------------------------------------------------------------------------------------------------")

run_q3()