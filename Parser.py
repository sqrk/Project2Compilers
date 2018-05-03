import Lexer
import BuildTree

index_current_token = -1
tokens = Lexer.lexer()


def lex():
    index_current_token += 1
    return tokens[index_current_token]


def parser():
    nextToken = lex()
    root = createNode("programRoot", None, False)
    programSub((nextTokenType, nextTokenValue), root)


# 1. program ⟶ 'program' 'id' '(' identifier_list ')' ';' declarations	subprogram_declarations compound_statement 	'.'

def programSub(root):
    (nextTokenType, nextTokenValue) = lex()

    if (nextTokenType != "program"):
        return "error"

    programChild = createNode("program", "program", True)
    addNode(root, programChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != "id"):
        return "error"

    idChild = createNode("id", "id", True)
    addNode(root, idChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != "lpar"):
        return "error"

    lparChild = createNode("lpar", "(", True)
    addNode(root, lparChild)

    identifierListChild = createNode("identifierListRoot", None, False)
    addNode(root, identifierListChild)

    identifierListSub(identifierListChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != 'rpar'):
        return "error"

    rparChild = createNode("rpar", ")", True)
    addNode(root, rparChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != "scolon"):
        return "error"

    scolonChild = createNode("scolon", ";", True)
    addNode(root, scolonChild)

    declarationsChild = createNode("declarationsRoot", None, False)
    addNode(root, declarationsChild)

    declarationsSub(declarationsChild)

    subprogramDeclarationsChild = createNode("subprogramDeclarationsChild", None, False)
    addNode(root, subprogramDeclarationsChild)

    subprogramDeclarationsSub(subprogramDeclarationsChild)

    compoundStatementsChild = createNode("compoundStatementsChild", None, False)
    addNode(root, compoundStatementsChild)

    compoundStatementsSub(compoundStatementsChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != "dot"):
        return "error"

    dotChild = createNode("dot", ".", True)
    addNode(root, dotChild)


# 2. identifier_list ⟶ 'id' [',' identifier_list]
def identifierListSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != "id"):
        return "error"

    while True:
        (nextTokenType, nextTokenValue) = lex()
        if nextTokenType == "comma":
            identifierListSub()
        else:
            index_current_token -= 1
            break


# 3. declarations ⟶  {'var' identifier_list ':' type ';'}
def declarationsSub(root):
    while (True):
        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenPair[0] != "var"):
            index_current_token -= 1
            break

        varChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, varChild)

        identifierListChild = createNode("identifierListChild", None, False)
        addNode(root, identifierListChild)

        identifierListSub(identifierListChild)

        nextTokenPair = lex()
        if (nextTokenPair[0] != "colon"):
            return "error"
        # We don't have to create a node for this punctuations because the "root" of this sub-tree will have only one child
        # colonChild = createNode("colonChild", nextTokenPair[1], True)
        # addNode(root, colonChild)

        typeChild = createNode("typeChild", None, False)
        addNode(root, typeChild)

        typeSub(typeChild)

        nextTokenPair = lex()
        if (nextTokenPair[0] != "scolon"):
            return "error"


# In case we won't to use a recursion instead
# declarationsSub(root)


# !!! 4. type ⟶ standard_type
def typeSub(root):
    typeChild = createNode('typeRoot', None, False)
    addNode(root, typeChild)

    standardTypeSub(typeChild)


# !!! 5. standard_type ⟶ 'integer'
def standardTypeSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != 'integer'):
        return 'error'

    integerChild = createNode(nextTokenType, nextTokenValue, True)
    addNode(root, integerChild)


# 6. subprogram_declarations ⟶ {subprogram_declaration ';'}
def subprogramDeclarationsSub(root):
    while True:
        (nextTokenType, nextTokenValue) = lex()

        if (nextTokenType != 'function' and nextTokenType != 'procedure'):
            index_current_token -= 1
            break

        # Create "subprogramDeclarationChild".
        subprogramDeclarationChild = createNode("subprogramDeclarationChild", None, False)
        addNode(root, subprogramDeclarationChild)

        # Parse child.
        subprogramDeclarationSub(subprogramDeclarationChild)

        # Should terminate with a semicolon.
        nextTokenPair = lex()
        if (nextTokenType != 'scolon'):
            return "error"

        # scolonChild = createNode(nextTokenType, nextTokenType, true)
        # addNode(root, scolonChild)


# 7. subprogram_declaration ⟶ subprogram_head declarations compound_statement
def subprogramDeclarationSub(root):
    subprogramHeadChild = createNode("subprogramHeadChild", None, False)
    addNode(root, subprogramHeadChild)
    subprogramHeadSub(subprogramHeadChild)

    declarationsChild = createNode("declarationsChild", None, False)
    addNode(root, declarationsChild)
    declarationsSub(declarationsChild)

    compoundStatementsChild = createNode("compoundStatementsChild", None, False)
    addNode(root, compoundStatementsChild)
    compoundStatementsSub(compoundStatementsChild)


# !!! 8. subprogram_head ⟶ 'function' 'id' arguments ':' standard_type ';' | 'procedure' 'id' arguments ';'
def subprogramHeadSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == 'function'):

        functionChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, functionChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'id'):
            return 'error'

        idChild = createNode(nextTokenType, nextTokenValue,
                             True)  # Actual value of id ((nextTokenType, nextTokenValue) = (token, value))
        addNode(root, idChild)

        argumentsChild = createNode('argumentsChild', None, False)
        addNode(root, argumentsChild)

        argumentsSub(argumentsChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'colon'):
            return 'error'

        # colonChild = createNode(nextTokenType, nextTokenValue, True)
        # addNode(root, colonChild)

        standardTypeChild = createNode('standardTypeChild', None, False)
        addNode(root, standardTypeChild)

        standardTypeSub(standardTypeChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'scolon'):
            return 'error'

    # scolonChild = createNode(nextTokenType, nextTokenValue, True)
    # addNode(root, scolonChild)

    elif (nextTokenType == 'procedure'):

        procedureChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, procedureChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'id'):
            return 'error'

        idChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, idChild)

        argumentsChild = createNode('argumentsChild', None, False)
        addNode(root, argumentsChild)

        argumentsSub(argumentsChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'scolon'):
            return 'error'

    # scolonChild = createNode(nextTokenType, nextTokenValue, True)
    # addNode(root, scolonChild)

    else:
        return 'error'  # In case none of 'function' nor 'procedure' was found


# !!! 9. arguments ⟶ ['(' parameter_list ')']
def argumentsSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != 'lpar'):
        return

    parameterListChild = createNode('parameterListChild', None, False)
    addNode(root, parameterListChild)

    parameterListSub(parameterListChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != 'rpar'):
        return 'error'


# 10. parameter_list ⟶ identifier_list ':' type {';' identifier_list ':' type}
def parameterListSub(root):
    identifierListNode = createNode("identifierListChild", None, False)
    identifierListSub(identifierListNode)
    addNode(root, identifierListNode)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != 'colon'):
        return "error"

    typeSub()

    nextTokenType = lex()
    if (nextTokenType == 'scolon'):
        parameterListSub()
    else:
        index_current_token -= 1


# 11. compound_statement ⟶ 'begin' [statement_list] 'end'
def compoundStatementsSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != "begin"):
        return "error"

    beginChild = createNode(nextTokenType, nextTokenValue, True)
    addNode(root, beginChild)

    nextTokenPair = lex()
    if (nextTokenPair[0] == "id"):
        index_current_token -= 1
        idChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, idChild)
        statementList()

    nextTokenPair = lex()
    if (nextTokenPair[0] != "end"):
        return "error"

    endChild = createNode(nextTokenPair[0], nextTokenPair[1], True)
    addNode(root, endChild)


# !!! 12. statement_list ⟶ statement {';' statement}
def statementListSub(root):
    statementChild = createNode('statementChild', None, False)
    addNode(root, statementChild)

    statementSub(statementChild)

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == ";"):
        # scolonChild = createNode(nextTokenType, nextTokenValue, True)
        # addNode(root, scolonChild)

        statementChild = createNode('statementChild', None, False)
        addNode(root, statementChild)

        statementSub(statementChild)  # In case there are more statements

    else:
        index_current_token -= 1  # In case there are no more statements


# 13. statement ⟶ ('id' [('assignop' expression) | '('expression_list')']) | compound_statement	| 'if' expression 'then' statement 'else' statement   | 'while' expression 'do' statement
def statementSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == 'id'):

        idChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, idChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType == 'assignop'):  # Case of 'id' 'assignop' expression
            expressionSub()

        elif (nextTokenType == 'lpar'):  # Case of 'id' '('expression_list')'
            expressionListSub()

            (nextTokenType, nextTokenValue) = lex()
            if (nextTokenType != 'rpar'):
                return 'error'

        else:  # Case of 'id'
            index_current_token -= 1

    elif (nextTokenType == 'begin'):  # Case of compound statement
        compoundStatementsSub()

    elif (nextTokenType == 'if'):  # Case of 'if' expression 'then' statement 'else' statement
        expressionSub()

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'then'):
            return 'error'

        statementSub()

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'else'):
            return 'error'

        statementSub()

    elif (nextTokenType == 'while'):  # Case of 'while' expression 'do' statement
        expressionSub()

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType != 'do'):
            return 'error'

        statementSub()

    else:
        return 'error'


# 14. variable ⟶ 'id'
def variable():
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType != 'id'):
        return "error"
    idChild = createNode("id", "id", True)
    addNode(root, idChild)


# 15. procedure_statement ⟶ 'id' ['(' expression_list ')']
def procedureStatement(root):
    nextTokenType = lex()
    if (nextTokenType != "id"):
        return "error"

    idChild = createNode(nextTokenPair[0], nextTokenPair[1], True)
    addNode(root, idChild)

    nextTokenType = lex()
    if (nextTokenType != "lpar"):
        index_current_token -= 1
        return

    lparChild = createNode(nextTokenPair[0], nextTokenPair[1], True)
    addNode(root, lparChild)

    expressionListSub(lparChild)

    nextTokenType = lex()
    if (nextTokenType != "rpar"):
        return "error"


# !!! 16. expression_list ⟶ expression {',' expression}
def expressionListSub(root):
    expressionChild = createNode('expressionChild', None, False)
    addNode(root, expressionChild)

    expressionSub(expressionChild)

    while (True):  # We might have more expressions
        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType == "comma"):
            # commaChild = createNode(nextTokenType, nextTokenValue, True)
            # addNode(root, commaChild)

            expressionChild = createNode('expressionChild', None, False)
            addNode(root, expressionChild)

            expressionSub(expressionChild)  # In case there are more expressions

        else:
            index_current_token -= 1  # In case there are no more expressions
            break


# 17. expression ⟶ simple_expr ['relop' simple_expr]
def expressionSub():
    simpleExprSub()

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == 'relop'):
        simple_expr()
    else:
        index_current_token -= 1
        return


# 18. simple_expr ⟶ (term | sign term) {'addop' term}
def simpleExprSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == 'sign'):
        signChild = createNode("sign", "sign", True)
        addNode(root, signChild)
        termSub(root)
    else:
        index_current_token -= 1
        termSub(root)

    while (True):
        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType == 'addop'):
            addopChild = createNode("addop", "addop", True)
            addNode(root, addopChild)
            termSub(root)
        else:
            index_current_token -= 1
            break


# FIXME
# 19. term ⟶ factor ['mulop' term]
def termSub():
    factorSub()

    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == 'mulop'):
        termSub()

    else:
        index_current_token -= 1  # In case there are no more terms


# !!! 20.factor ⟶ 'id' ['(' expression_list ')' ]	| 'num'   | '(' expression ')'   | 'not' factor
def factorSub(root):
    (nextTokenType, nextTokenValue) = lex()
    if (nextTokenType == 'id'):

        idChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, idChild)

        (nextTokenType, nextTokenValue) = lex()
        if (nextTokenType == 'lpar'):  # Case of 'id' '(' expression_list ')'

            # lparChild = createNode(nextTokenType, nextTokenValue, True)
            # addNode(root, lparChild)

            expressionListChild = createNode('expressionListChild', None, False)
            addNode(root, expressionListChild)

            expressionListSub(expressionListChild)

            (nextTokenType, nextTokenValue) = lex()
            if (nextTokenType != 'rpar'):
                return 'error'

        # rparChild = createNode(nextTokenType, nextTokenValue, True)
        # addNode(root, rparChild)

        else:
            index_current_token -= 1  # In case there's no expression list

    elif (nextTokenType == 'not'):  # Case of 'not' factor

        notChild = createNode(nextTokenType, nextTokenValue, True)
        addNode(root, notChild)

        # factorChild = createNode('factorChild', None, False)
        # addNode(root, factorChild)

        factorSub(root)

    elif (nextTokenType != 'num'):  # Case of 'num'
        return 'error'

    numChild = createNode(nextTokenType, nextTokenValue, True)
    addNode(root, numChild)
