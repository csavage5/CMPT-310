# Cameron Savage, 301310824, cdsavage@sfu.ca



class KB():
    '''
    Class that represents a Knowledge Base. Contains
    methods for loading rules and storing atoms and 
    inferences.
    '''

    def __init__(self):
        # set of rules loaded from knowledge base file
        # (key, value) = (head, atoms[])
        self.rules = dict()
        
        # atoms known to be true via inference. 
        # Will be reset upon KB reload.
        # (key, value) = (atom, boolean)
        self.inferred = dict()

        # all atoms known to be true via 'tell' 
        # command. Will be reset upon KB reload.
        # (key, value) = (atom, boolean)
        self.facts = dict()

        self.isFormattedCorrectly = True

    def loadKBRuleset(self, path: str):
        '''
        Loads new rules from provided file. Will
        wipe current rules and all inferences.
        '''

        # TODO test

        try:
            file = open(path)
        
        except:
            print(f'Error: could not open file with provided filename "{path}". Nothing added to KB.')
            return

        # reset known atoms and rules
        self.inferred.clear()
        self.rules.clear()
        self.facts.clear()

        # create temporary dictionary to store atoms in before
        # checking validity
        tempRules = dict()
        tokens = []

        # tokenize each line of the file
        for line in file:
            #print(line)

            if line.strip() == "":
                continue

            try:
                tokens.append(self.tokenizeRuleset(line.strip()))
            except:
                print(f'Error: knowledge base {path} is not formatted correctly. Nothing added to KB.')
                return

        # add atoms to ruleset
        for tokenList in tokens:
            self.rules[tokenList[0]] = tokenList[1:]

        # Display added clauses
        self.printRules()
        
    def tokenizeRuleset(self, input: str) -> list:
        # TODO test for edge cases
        tokens = []
        atom = ""

        # find HEAD
        index = 0
        itr = input[index]
        while itr != "<" and index < len(input):
            atom += itr
            index += 1

            if index < len(input):
                itr = input[index]

        atom = atom.strip()

        if not is_atom(atom):
            print(f'Error: "{atom}" is not a valid atom')
            raise Exception()

        tokens.append(atom)
        #print(tokens)

        # find <--
        atom = ""
        while itr in "<- " and index < len(input):
            atom += itr
            index += 1

            if index < len(input):
                itr = input[index]

        atom = atom.strip()

        if atom != ("<--"):
            print(f'Error: implication "{atom}" not formatted correctly')
            raise Exception()

        # find atoms + &
        atom = ""
        ampersandCount = 0

        while index < len(input):
            itr = input[index]
            
            # Termination of atom
            if (itr == "&" or index == len(input) - 1):
                
                if itr == "&":
                    ampersandCount += 1

                # Error Checking
                if itr == '&' and atom == "":
                    # error - incorrect '&' formatting
                    print(f'Error: "&" character not formatted correctly')
                    raise Exception()
                
                # Tokenize atom
                elif atom != "":
                    if itr != "&":
                        atom += itr

                    atom = atom.strip()

                    if not is_atom(atom):
                        print(f'Error: "{atom}" is not a valid atom')
                        raise Exception()

                    tokens.append(atom)
                    #print(tokens)
                    atom = ""

            else:
                # Add char to atom
                atom += itr

            index += 1

        # print(f'ampersandCount: {ampersandCount}')
        # print(f'number of tokens: {len(tokens)}')
        # print(f'tokens: {tokens}')

        # -2 from tokens since HEAD is included
        if ampersandCount != len(tokens) - 2:

            print(f'Error: "&" character not formatted correctly')
            raise Exception()

        #print(tokens)

        return tokens

    def expandKB(self, newAtoms: list):
        '''
        Adds new atoms to knowledge base.
        '''

        # if ANY atom is invalid, can't add
        # any atoms to knowledge base.
        for atom in newAtoms:
            # check if atoms are valid
            if not is_atom(atom):
                print(f'Error: "{atom}" is not valid - no atoms added to knowledge base')
                return

        for atom in newAtoms:
            # TODO check if atom is already known
            # all atoms are valid, add to knowledge base

            if self.facts.get(atom, False) or self.inferred.get(atom, False):
                print(f'  atom "{atom}" already known to be true')

            else:
                self.facts[atom] = True
                print(f'  "{atom}" added to KB')

    def infer_all(self):
        '''
        Uses all rules to infer facts from atoms in
        knowledge base.
        '''

        # End condition: after looping through all rules,
        #                nothing new was inferred
        madeInference = True
        newInferences = []

        while (madeInference == True):
            madeInference = False
            
            # make pass on all rules
            for head in self.rules:

                # if HEAD is NOT believed
                if not self.isKnown(head):
                    #print(f'-> {head} is NOT believed to be true')
                    # check if all b_1, ... , b_n are true
                    foundFalse = False
                    for atom in self.rules[head]:
                        #print(f'---> checking atoms {self.rules[head]} for truth...')
                        if not self.isKnown(atom):
                            foundFalse = True
                            break

                    # add head to inferred if 
                    # b_i, ... , b_n are true
                    if foundFalse == False:
                        self.inferred[head] = True
                        newInferences.append(head)
                        madeInference = True

        print(f'  Newly inferred atoms:')
        prefix = "    "

        if len(newInferences) == 0:
            print(f'{prefix}<none>')
        
        else:
            for atom in newInferences:
                print(f'{prefix}{atom}', end = "")
                prefix = ", "
    
        print(f'\n  Atoms already known to be true:')
        prefix = "    "

        if len(self.facts.keys()) + len(self.inferred.keys()) == 0:
            print(f'{prefix}<none>')
        
        else:
            for atom in self.facts:
                print(f'{prefix}{atom}', end = "")
                prefix = ", "

            for atom in self.inferred:
                if atom not in newInferences:
                    print(f', {atom}', end = "")
        
        print()

    def isKnown(self, atom: str) -> bool:
        '''
        Checks if the given atom has been inferred or 
        is known via "tell" command
        '''
        return self.facts.get(atom, False) or self.inferred.get(atom, False)

    def printRules(self):
        print(f'{len(self.rules.keys())} definite clauses read in:')

        for key in self.rules:
            print(f'  {key} <-- ', end = "")
            
            value = self.rules[key]

            prefix = ""
            for atom in value:
                print(f'{prefix}{atom} ', end = "")
                prefix = '& '
            
            print()


# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"

# separate user input into tokens
def tokenizeInput(input: str) -> list:
    
    tokens = []
    strTemp = ""

    for itr in input:
        if itr == " " and strTemp != "":
            # found end of token
            tokens.append(strTemp)
            strTemp = ""

        elif itr != "" and itr != " ":
            strTemp += itr

    if strTemp != "":
        tokens.append(strTemp.strip())
        
    return tokens

# entry point for program
def main():

    kb = KB()
    
    while True:
        userInput = tokenizeInput(input("\nkb> "))
        #print(userInput)

        if len(userInput) == 0:
            print("Error: no input")

        # decide what to do based on first token
        elif userInput[0] == "tell":
            if len(userInput) > 1:
                kb.expandKB(userInput[1:])
            
            else:
                print("Error: must provide at least one atom.")
            
        elif userInput[0] == "load":

            if len(userInput) > 1:
                kb.loadKBRuleset(userInput[1])
            
            else:
                print("Error: must provide a file path.")
        
        elif userInput[0] == "clear_atoms":
            kb.facts.clear()
            kb.inferred.clear()

        elif userInput[0] == "infer_all":
            kb.infer_all()

        elif userInput[0] == "exit":
            break

        elif userInput[0] == "disp_facts":
            print(kb.facts)

        elif userInput[0] == "disp_inferred":
            print(kb.inferred)

        elif userInput[0] == "disp_rules":
            kb.printRules()

        else:
            print(f'Error: unknown command "{userInput[0]}"')

if __name__ == "__main__":
    main()

