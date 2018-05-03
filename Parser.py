import Lexer
import BuildTree

index_current_token = -1
tokens = Lexer.lexer()


def lex():
	index_current_token += 1
	return tokens[index_current_token][0]

def parser():
	nextToken = lex()
	root = createNode("programRoot", None, False)
	programSub(nextTokenPair, root)

#1. program ⟶ 'program' 'id' '(' identifier_list ')' ';' declarations	subprogram_declarations compound_statement 	'.'

def programSub(nextTokenPair, root):
	nextTokenType = nextTokenPair[0]

	if(nextTokenType != "program"):
		return "error"

	programChild = createNode("program", "program", True)
	addNode(root, programChild)

	nextTokenType = lex()
	if(nextTokenType != "id"):
		return "error"

	idChild = createNode("id", "id", True)
	addNode(root, idChild)

	nextTokenType = lex()
	if(nextTokenType != "lpar"):
		return "error"

	lparChild = createNode("lpar", "(", True)
	addNode(root, lparChild)

	identifierListChild = createNode("identifierListRoot", None, False)
	addNode(root, identifierListChild)

	identifierListSub(identifierListChild)

	nextTokenType = lex()
	if (nextTokenType != 'rpar'):
		return "error"

	rparChild = createNode("rpar", ")", True)
	addNode(root, rparChild)

	nextTokenType = lex()
	if (nextTokenType != "scolon"):
		return "error"

	scolonChild = createNode("scolon", ";", True)
	addNode(root, scolonChild)

	declarationsChild = createNode("declarationsRoot", None, False)
	addNode(root, declarationsChild)

	declarationsSub(root, declarationsChild)

	subprogramDeclarationsChild = createNode("subprogramDeclarationsChild", None, False)
	addNode(root, subprogramDeclarationsChild)

	subprogramDeclarationsSub(root, subprogramDeclarationsChild)

	compoundStatementsChild = createNode("compoundStatementsChild", None, False)
	addNode(root, compoundStatementsChild)

	compoundStatementsSub(compoundStatementsChild)

	nextTokenType = lex()
	if (nextTokenType != "dot"):
		return "error"
		
	dotChild = createNode("dot", ".", True)
	addNode(root, dotChild)

#2. identifier_list ⟶ 'id' [',' identifier_list]
def identifierListSub():
	nextTokenType = lex()
	if (nextTokenType != "id"):
		return "error"
	
	nextTokenType = lex()
	if (nextTokenType == "comma"):
		identifierListSub()
	else:
		index_current_token -= 1


#3. declarations ⟶  {'var' identifier_list ':' type ';'}
def declarationsSub():
	nextTokenType = lex()
	if (nextTokenType != "var"):
		index_current_token -=1
		return

	identifier_listSub()

	nextTokenType = lex()
	if (nextTokenType != "colon"):
		return "error"

	typeSub()

	nextTokenType = lex()
	if (nextTokenType != "scolon"):
		return "error"

	declarationsSub()


#4. type ⟶ standard_type
def typeSub(nextTokenPair, root):
	typeChild = createNode('typeRoot', None, False)
	addNode(root, typeChild)

	standardTypeSub(nextTokenPair, typeChild)


#5. standard_type ⟶ 'integer'
def standardTypeSub():
    nextTokenType = lex()
    if(nextTokenType != 'integer'):
        return 'error'



#6. subprogram_declarations ⟶ {subprogram_declaration ';'}
def subprogramDeclarationsSub(root):
	nextTokenType = lex()

	
	
	if (nextTokenType != 'function' and nextTokenType != 'procedure'):
		index_current_token -= 1
		return

	subprogramDeclarationsChild = createNode("subprogramDeclarationsChild", None, False)
	addNode(root, subprogramDeclarationsChild)

	subprogramDeclarationSub(subprogramDeclarationsChild)

	nextTokenType = lex()
	if (nextTokenType != 'scolon'):
		return "error"
	scolonChild = createNode("scolon", ";", true)
	addNode(root, scolonChild)

	subprogramDeclarationChild = createNode("subprogramDeclarationChild", None, False)
	addNode(root, subprogramDeclarationChild)

	subprogramDeclarationsSub(subprogramDeclarationChild)





#7. subprogram_declaration ⟶ subprogram_head declarations compound_statement
def subprogramDeclarationSub():

	subprogramHeadSub()
	declarationsSub()
	compoundStatementsSub()



#8. subprogram_head ⟶ 'function' 'id' arguments ':' standard_type ';' | 'procedure' 'id' arguments ';'
def subprogramHeadsub(nextTokenPair, root):
	nextTokenType = lex()
	if(nextTokenType == 'function'):

		functionChild = createNode('function', 'function', True)
		addNode(root, functionChild)

		nextTokenType = lex()
		if(nextTokenType != 'id'):
			return 'error'

		idChild = createNode('id', nextTokenPair[1], True)		#Actual value of id (nextTokenPair = (token, value))
		addNode(root, idChild)

		argumentsChild = createNode('argumentsChild', None, False)
		addNode(root, argumentsChild)

		argumentsSub(nextTokenPair, argumentsChild)

		nextTokenType = lex()
		if(nextTokenType != 'colon'):
			return 'error'

		colonChild = createNode('colon', ':', True)
		addNode(root, colonChild)

		standardTypeChild = createNode('standardTypeChild', None, False)
		addNode(root, standardTypeChild)

		standardTypeSub(nextTokenPair, standardTypeChild)

		nextTokenType = lex()
		if(nextTokenType != 'scolon'):
			return 'error'

		scolonChild = createNode('scolon', ';', True)
		addNode(root, scolonChild)

	elif(nextTokenType == 'procedure'):

		procedureChild = createNode('procedure', 'procedure', True)
		addNode(root, procedureChild)

		nextTokenType = lex()
		if(nextTokenType != 'id'):
			return 'error'

		idChild = createNode('id', nextTokenPair[1], True)
		addNode(root, idChild)

		argumentsChild = createNode('argumentsChild', None, False)
		addNode(root, argumentsChild)

		argumentsSub(nextTokenPair, argumentsChild)

		nextTokenType = lex()
		if(nextTokenType != 'scolon'):
			return 'error'

		scolonChild = createNode('scolon', ';', True)
		addNode(root, scolonChild)

	else:
		return 'error'		#In case none of 'function' nor 'procedure' was found


#9. arguments ⟶ ['(' parameter_list ')']
def argumentsSub():
    nextTokenType = lex()
    if(nextTokenType != 'lpar'): 
        return

    parameterListSub()

    nextTokenType = lex()
    if(nextTokenType != 'rpar'):
        return 'error'

#10. parameter_list ⟶ identifier_list ':' type {';' identifier_list ':' type}  
def parameterListSub():
	identifierListSub()

	nextTokenType = lex()
	if (nextTokenType != 'colon'):
		return "error"

	typeSub()

	nextTokenType = lex()
	if (nextTokenType == 'scolon'):
		parameterListSub()
	else:
		index_current_token -= 1


#11. compound_statement ⟶ 'begin' [statement_list] 'end' 
def compoundStatementsSub():
	nextTokenType = lex()
	if (nextTokenType != "begin"):
		return "error"

	nextTokenType = lex()
	if (nextTokenType == "id"):
		index_current_token -= 1
		statementList()

	nextTokenType = lex()
	if (nextTokenType != "end"):
		return "error"


#12. statement_list ⟶ statement {';' statement}
def statementListSub(nextTokenPair, root):
	statementChild = createNode('statementChild', None, False)
	addNode(root, statementChild)

	statementSub(nextTokenPair, statementChild)

	nextTokenType = lex()
	if(nextTokenType == ";"):
		scolonChild = createNode('scolon', ';', True)
		addNode(root, scolonChild)

		statementChild = createNode('statementChild', None, False)
		addNode(root, statementChild)

		statementSub(nextTokenPair, statementChild)					#In case there are more statements
	
	else:
		index_current_token -= 1		#In case there are no more statements


#13. statement ⟶ ('id' [('assignop' expression) | '('expression_list')']) | compound_statement	| 'if' expression 'then' statement 'else' statement   | 'while' expression 'do' statement
def statementSub():
    nextTokenType = lex()
    if(nextTokenType == 'id'):
    	
    	nextTokenType = lex()
    	if(nextTokenType == 'assignop'): 		#Case of 'id' 'assignop' expression
    		expressionSub()

    	elif(nextTokenType == 'lpar'):			#Case of 'id' '('expression_list')'
    		expressionListSub()

    		nextTokenType = lex()
    		if(nextTokenType != 'rpar'):
    			return 'error'

    	else:									#Case of 'id'
    		index_current_token -= 1

    elif(nextTokenType == 'begin'):				#Case of compound statement
    	compoundStatementsSub()

    elif(nextTokenType == 'if'):				#Case of 'if' expression 'then' statement 'else' statement
    	expressionSub()

    	nextTokenType = lex()
    	if(nextTokenType != 'then'):
    		return 'error'

    	statementSub()

    	nextTokenType = lex()
    	if(nextTokenType != 'else'):
    		return 'error'

    	statementSub()

    elif(nextTokenType == 'while'):				#Case of 'while' expression 'do' statement 
    	expressionSub()

    	nextTokenType = lex()
    	if(nextTokenType != 'do'):
    		return 'error'

    	statementSub()

    else:
    	return 'error'

	
#14. variable ⟶ 'id'
def variable ():
	nextTokenType = lex()
	if (nextTokenType != 'id'):
		return "error"
	idChild = createNode("id", "id", True)
	addNode(root, idChild)



#15. procedure_statement ⟶ 'id' ['(' expression_list ')']
def procedureStatement():
	nextTokenType = lex()
	if (nextTokenType != "id"):
		return "error"

	nextTokenType = lex()
	if (nextTokenType != "lpar"):
		index_current_token -= 1
		return

	expressionListSub()

	nextTokenType = lex()
	if (nextTokenType != "rpar"):
		return "error"


#16. expression_list ⟶ expression {',' expression} 
def expressionListSub(nextTokenPair, root):
	expressionChild = createNode('expressionChild', None, False)
	addNode(root, expressionChild)

	expressionSub(nextTokenPair, expressionChild)

	while(True):							#We might have more expressions
		nextTokenType = lex()
		if(nextTokenType == "comma"):

			commaChild = createNode('comma', ',', True)
			addNode(root, commaChild)

			expressionChild = createNode('expressionChild', None, False)
			addNode(root, expressionChild)

			expressionSub(nextTokenPair, expressionChild)					#In case there are more expressions

		else:
			index_current_token -= 1		#In case there are no more expressions
			break


#17. expression ⟶ simple_expr ['relop' simple_expr]
def expressionSub():
    simpleExprSub()

    nextTokenType = lex()
    if(nextTokenType == 'relop'):
        simple_expr()
    else:
    	index_current_token -= 1
    	return


#18. simple_expr ⟶ (term | sign term) {'addop' term}
def simpleExprSub (root):
	nextTokenType = lex()
	if(nextTokenType == 'sign'):
		signChild = createNode("sign", "sign", True)
		addNode(root, signChild)
		termSub(root)
	else:
		index_current_token -= 1
		termSub(root)

	while(True):
		nextTokenType = lex()
		if(nextTokenType == 'addop'):
			addopChild = createNode("addop", "addop", True)
			addNode(root, addopChild)
			termSub(root)
		else:
			index_current_token -= 1
			break



#19. term ⟶ factor ['mulop' term]
def termSub():
	factorSub()

	nextTokenType = lex()
	if(nextTokenType == 'mulop'):
		termSub()

	else:
		index_current_token -= 1 			#In case there are no more terms


#20.factor ⟶ 'id' ['(' expression_list ')' ]	| 'num'   | '(' expression ')'   | 'not' factor
def factorSub(nextTokenPair, root):
	nextTokenType = lex()
	if(nextTokenType == 'id'):
		
		idChild = createNode('id', nextTokenPair[1], True)
		addNode(root, idChild)

		nextTokenType = lex()
		if(nextTokenType == 'lpar'):		#Case of 'id' '(' expression_list ')'

			lparChild = createNode('lpar', '(', True)
			addNode(root, lparChild)

			expressionListChild = createNode('expressionListChild', None, False)
			addNode(root, expressionListChild)

			expressionListSub(nextTokenPair, expressionListChild)

			nextTokenType = lex()
			if(nextTokenType != 'rpar'):
				return 'error'

			rparChild = createNode('rpar', ')', True)
			addNode(root, rparChild)

		else:
			index_current_token -= 1		#In case there's no expression list

	elif(nextTokenType == 'not'):			#Case of 'not' factor

		notChild = createNode('not', 'not', True)
		addNode(root, notChild)

		factorChild = createNode('factorChild', None, False)
		addNode(root, factorChild)

		factorSub(nextTokenPair, factorChild)

	elif(nextTokenType != 'num'):			#Case of 'num'
		return 'error'

	numChild = createNode('num', nextTokenPair[1], True)
