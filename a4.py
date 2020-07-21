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
        self.facts = dict()

        # all atoms known to be true via 'tell' 
        # command. Will NOT be reset upon KB
        # reload.
        self.tells = dict()


    def loadKBFile(self, path: str):
        '''
        Loads new rules from provided file. Will
        wipe current rules and all known facts.
        '''

        # TODO implement
        self.facts.clear()
        self.rules.clear()
        

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
            self.tells[atom] = True
            self.facts[atom] = True

    def infer_all(self):
        '''
        Uses all rules to infer facts from atoms in
        knowledge base.
        '''
        # TODO implement
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
def tokenize(input: str) -> list:
    tokens = []

    strTemp = ""

    for itr in input:
        if itr == " " and strTemp != "":
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
    
    while true:
        userInput = tokenize(input("kb> "))
        print(userInput)

        # decide what to do based on first token
        if userInput[0] == "tell":
            if len(userInput) > 1:
                kb.expandKB(userInput[1:])
            
            else:
                print("Error: must provide at least one atom")
            
        elif userInput[0] == "load":

            if len(userInput) > 1:
                kb.loadKBFile(userInput[1])
            
            else:
                print("Error: must provide a file path")
        
        elif userInput[0] == "clear_tells":
            kb.tells.clear()
            kb.facts.clear()

        elif userInput[0] == "infer_all":
            kb.infer_all()

        elif userInput[0] == "exit":
            break

        else:
            print(f'Error: unknown command "{userInput[0]}"')



if __name__ == "__main__":
    main()

