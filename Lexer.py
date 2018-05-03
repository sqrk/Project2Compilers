import re

variables = {

}

sign = ['+', '-']
addop = ['+', '-', 'or']
mulop = ['*', '/', 'div', 'mod', 'and']
relop = ['=', '<>', '<', '<=', '>=', '>']
assignop = [':=']
types = ['integer']
reservedWords = ['program', 'function', 'if', 'else', 'then', 'begin', 'end', 'read', 'write', 'var', 'while', 'do']
punct = {',': 'comma', ':': 'colon', ';': 'scolon', '(': 'lpar', ')': 'rpar', '.': 'dot', '[': 'lbra', ']': 'rbra'}
sep = [' ', ',', ':', ';', '(', ')', '.', '\n']
tokens = []


def getTokenType(nextToken):
    if (nextToken in reservedWords):
        return nextToken
    elif (nextToken in sign):
        return 'sign'
    elif (nextToken in assignop):
        return 'assignop'
    elif (nextToken in relop):
        return 'relop'
    elif (nextToken in mulop):
        return 'mulop'
    elif (nextToken in addop):
        return 'addop'
    elif (nextToken in types):
        return 'type'
    elif (nextToken in punct):
        return punct[nextToken]
    elif (nextToken[
        0].isalpha()):  # if a variable starts with a letter and followed by either digits or letters then its an 'id' and doesn't fulfill above conditions
        for char in nextToken:
            if (not (
                    char.isalpha() or char.isdigit() or char == "_")):  # If the variable contains something apart from letters digits and underscores, return error
                return 'error'
        return 'id'
    elif (nextToken[0].isdigit()):  # if a variable starts with a digit
        for char in nextToken:
            if (not char.isdigit()):
                return 'error'
        return 'num'


def lexer():
    with open('input.txt') as file:
        code = [i.strip() for i in file]

    tokenValue = []
    comment = 0
    count = 0

    for line in code:
        for char in line:
            if (char == "{" or comment):  # Skipping comments
                comment = 1
                if (char == "}"):
                    comment = 0
                continue

            else:
                if (char in sep):  # characters that indicate the beginning of a new token
                    if (tokenValue):  # If token is not empty, and current char should be skipped, token is complete
                        tokenType = getTokenType(''.join(tokenValue))
                        tokens.append((tokenType, ''.join(tokenValue)))

                        tokenValue = []

                    if (char != " "):  # If the character found is not a space, we need to send it to the lexer
                        tokenType = getTokenType(char)
                        continue  # Skip appending in tokenValue
                    else:
                        continue

                tokenValue.append(char)  # append char to token

                if (line[
                    -1] == char):  # If the char is the last one of the line, analyze it so that it doesn't get appended with the first from the next line (no separators)
                    tokenType = getTokenType(''.join(tokenValue))
                    tokens.append((tokenType, ''.join(tokenValue)))
                    tokenValue = []
                    continue

    return tokens


lexer()