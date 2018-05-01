import Lexer

index_current_token = -1
tokens = Lexer.lexer()


def lex():
	index_current_token += 1
	return tokens[index_current_token]

def parser():
	nextToken = lex()
	programSub(nextTokenPair)

def programSub(nextTokenPair):
	nextTokenType = nextTokenPair[0]

	if(nextTokenType != "program"):
		return "error"
	nextTokenType = lex()
	if(nextTokenType != "id"):
		return "error"
		#TREE
	nextTokenType = lex()
	if(nextTokenType != "lpar"):
		return "error"

	identifierListSub()

	nextTokenType = lex()
	if (nextTokenType != 'rpar'):
		return "error"
	nextTokenType = lex()
	if (nextTokenType != "scolon"):
		return "error"

	declarationsSub()
	subprogramDeclarationsSub()
	compoundStatementsSub()

	nextTokenType = lex()
	if (nextTokenType != "dot"):
		return "error"


def identifierListSub():
	nextTokenType = lex()
	if (nextTokenType != "id"):
		return "error"
	nextTokenType = lex()
	if (nextTokenType == ","):
		identifierListSub()
