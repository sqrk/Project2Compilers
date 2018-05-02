import Lexer

index_current_token = -1
tokens = Lexer.lexer()


def lex():
	index_current_token += 1
	return tokens[index_current_token][0]

def parser():
	nextToken = lex()
	programSub(nextTokenPair)

#1. program ⟶ 'program' 'id' '(' identifier_list ')' ';' declarations	subprogram_declarations compound_statement 	'.'

def programSub(nextTokenPair):
	nextTokenType = nextTokenPair[0]

	if(nextTokenType != "program"):
		return "error"
	nextTokenType = lex()
	if(nextTokenType != "id"):
		return "error"

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
def typeSub():
	standardTypeSub()


#5. standard_type ⟶ 'integer'
def standardTypeSub():
    nextTokenType = lex()
    if(nextTokenType != 'integer'):
        return 'error'


#6. subprogram_declarations ⟶ {subprogram_declaration ';'}
def subprogramDeclarationsSub():
	nextTokenType = lex()
	if (nextTokenType != 'function' and nextTokenType != 'procedure'):
		index_current_token -= 1
		return

	subprogramDeclarationSub()

	nextTokenType = lex()
	if (nextTokenType != 'scolon'):
		return "error"

	subprogramDeclarationsSub()



#7. subprogram_declaration ⟶ subprogram_head declarations compound_statement
def subprogramDeclarationSub():

	subprogramHeadSub()
	declarationsSub()
	compoundStatementsSub()



#8. subprogram_head ⟶ 'function' 'id' arguments ':' standard_type ';' | 'procedure' 'id' arguments ';'
def subprogramHeadsub():
	nextTokenType = lex()
	if(nextTokenType == 'function'):

		nextTokenType = lex()
		if(nextTokenType != 'id'):
			return 'error'

		argumentsSub()

		nextTokenType = lex()
		if(nextTokenType != 'colon'):
			return 'error'

		standardTypeSub()

		nextTokenType = lex()
		if(nextTokenType != 'scolon'):
			return 'error'

	elif(nextTokenType == 'procedure'):

		nextTokenType = lex()
		if(nextTokenType != 'id'):
			return 'error'

		argumentsSub()

		nextTokenType = lex()
		if(nextTokenType != 'scolon'):
			return 'error'

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
def statementListSub():
	statementSub()

	nextTokenType = lex()
	if(nextTokenType == ";"):
		statementSub()					#In case there are more statements
	
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
def expressionListSub():
	expressionSub()

	while(True):							#We might have more expressions
		nextTokenType = lex()
		if(nextTokenType == "comma"):
			expressionSub()					#In case there are more expressions

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
def simpleExprSub ():
	nextTokenType = lex()
	if(nextTokenType == 'sign'):
		termSub()
	else:
		index_current_token -= 1
		termSub()

	while(True):
		nextTokenType = lex()
		if(nextTokenType == 'addop'):
			termSub()
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
def factorSub():
	nextTokenType = lex()
	if(nextTokenType == 'id'):

		nextTokenType = lex()
		if(nextTokenType == 'lpar'):		#Case of 'id' '(' expression_list ')'

			expressionListSub()

			nextTokenType = lex()
			if(nextTokenType != 'rpar'):
				return 'error'
		else:
			index_current_token -= 1		#In case there's no expression list

	elif(nextTokenType == 'not'):			#Case of 'not' factor
		factorSub()

	elif(nextTokenType != 'num'):			#Case of 'num'
		return 'error'

