# Cameron Savage, 301310824, cdsavage@sfu.ca



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
    userInput = tokenize(input("kb> "))
    print(userInput)

    # decide what to do based on first token

    if userInput[0] == "tell":

    elif userInput[0] == "load":

    elif userInput[0] == "infer_all":



if __name__ == "__main__":
    main()

