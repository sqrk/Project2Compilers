def visit(root, level):
    for i in range(0, level):
        print('--', end='')
    print(root.tokenType, end='')
    if root.isTerminal:
        print(" ", root.tokenValue, end='')
    print("")

    for child in root.children:
        visit(child, level + 1)
