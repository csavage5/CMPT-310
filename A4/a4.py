# Cameron Savage, 301310824, cdsavage@sfu.ca



class KB():
    '''
    Class that represents a Knowledge Base. Contains
    methods for loading rules and storing atoms and 
    inferences.
    '''

    def __init__(self):
        # (key, value) = (head, atom list)
        self.rules = dict()
        
        # atoms known to be true via inference or 
        # 'tell'. Will be reset upon KB reload.
        # (key, value) = (atom, boolean)
        self.inferred = dict()

        # all atoms known to be true via 'tell' 
        # command. Will NOT be reset upon KB
        # reload.
        self.facts = dict()

        self.isFormattedCorrectly = True

    def loadKBRuleset(self, path: str):
        '''
        Loads new rules from provided file. Will
        wipe current rules and all known facts.
        '''

        # TODO implement

        try:
            file = open(path)
        
        except:
            print(f'Error: could not open file with provided filename "{path}". Nothing added to KB.')
            return

        # reset facts and rules
        self.inferred.clear()
        self.rules.clear()

        #rule = file.readline()

        for line in file:
            print(line)

            if line.strip() == "":
                continue

            #self.tokenizeRuleset(line)

            try:
                self.tokenizeRuleset(line)
            except:
                print("Error: file is not formatted correctly. Nothing added to KB.")
                return


        # while (rule != ""):
        #     print(rule)

        #     if rule.strip() == "":
        #         rule = file.readline()

        #     self.tokenizeRuleset(rule)

        #     # try:
        #     #     self.tokenizeRuleset(rule)
        #     # except:
        #     #     print("Error: file is not formatted correctly. Nothing added to KB.")
        #     #     return

        #     rule = file.readline().strip()
        

    def tokenizeRuleset(self, input: str) -> list:
        # TODO implement
        tokens = []
        temp = ""

        # find HEAD
        index = 0
        itr = input[index]
        while itr != "<" and index < len(input):
            temp += itr
            index += 1

            if index < len(input):
                itr = input[index]

        temp = temp.strip()

        if not is_atom(temp):
            print(f'Head {temp} not formatted correctly')
            raise Exception()

        tokens.append(temp)
        print(tokens)

        # find <--
        temp = ""
        while not is_letter(itr) and index < len(input):
            temp += itr
            index += 1

            if index < len(input):
                itr = input[index]

        temp = temp.strip()

        if temp != ("<--"):
            print(f'{temp} not formatted correctly')
            raise Exception()
        
        print(f'Found arrow {temp}')

        # find atoms + &
        temp = ""

        # TRUE if there's an ampersand BEFORE the current token
        # set to TRUE since there shouldn't be an '&' after '<--'
        ampersandCount = 1
        while index < len(input):
            itr = input[index]

            if itr == "&" and temp == "":
                # switch boolean value if ampersand is found
                # this will deal with edge case if there is
                # an '&' after '<--'
                ampersandCount += 1

            elif (itr == " " or itr == "&") and temp != "":
                # found end of atom token
                if ampersandCount != 1:
                    # no & separating atom tokens
                    # or too many &s between tokens,
                    # throw error
                    print("& not formatted correctly")
                    raise Exception()
                
                temp = temp.strip()
                tokens.append(temp)
                print(tokens)
                temp = ""
                
                if itr == "&":
                    # found & for next token
                    ampersandCount = 1
                else: 
                    ampersandCount = 0
            
            elif itr != " ":
                temp += itr

            index += 1
            

        if temp != "":
            temp = temp.strip()
            tokens.append(temp)
        print(tokens)

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
            # all atoms are valid, add to knowledge base
            self.facts[atom] = True

    def infer_all(self):
        '''
        Uses all rules to infer facts from atoms in
        knowledge base.
        '''
        # TODO implement

        # TODO display all atoms in self.inferred
        print("Newly inferred atoms: ")

        # TODO display all atoms in self.facts
        print("Atoms already known to be true: ")

        return


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

        elif itr != "":
            strTemp += itr

    if strTemp != "":
        tokens.append(strTemp)
        
    return tokens

# entry point for program
def main():

    kb = KB()
    
    while True:
        userInput = tokenizeInput(input("kb> "))
        print(userInput)

        # decide what to do based on first token
        if userInput[0] == "tell":
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

        elif userInput[0] == "infer_all":
            kb.infer_all()

        elif userInput[0] == "exit":
            break

        else:
            print(f'Error: unknown command "{userInput[0]}"')

if __name__ == "__main__":
    main()

