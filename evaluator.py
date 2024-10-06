import decimal, re, sys

def isoper(token):
    return token in ["^", "*", "/", "+", "-"]

def issign(token):
    return token in ["+", "-"]

def isnum(token):
    return re.fullmatch("[-+]?\\d+\\.?\\d*", token) is not None

def isnumpart(token):
    return token in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

def isopen(token):
    return token in ["(", "[", "{"]

def isclose(token):
    return token in [")", "]", "}"]

def gettokens(expr, debug):
    number, tokens = [], []
    for char in re.sub("\\s+", "", expr):
        if isnumpart(char): number.append(char)
        elif isoper(char) or isopen(char) or isclose(char):
            if len(number) > 0:
                tokens.append("".join(number))
                number.clear()
            tokens.append(char)
        else: raise Exception("Syntax error: invalid token", char)
    if len(number) > 0: tokens.append("".join(number))
    if debug: print("Tokens:", str(tokens))
    i = 0
    while i < len(tokens):
        if isoper(tokens[i]):
            if i == 0 or isopen(tokens[i - 1]): tokens.insert(i, "0")
            elif i == len(tokens) - 1 or isclose(tokens[i + 1]): tokens.insert(i + 1, "0")
        elif i > 0 and isopen(tokens[i]) and (isclose(tokens[i - 1]) or isnum(tokens[i - 1])): tokens.insert(i, "*")
        elif i > 1 and isnum(tokens[i]) and isoper(tokens[i - 1]) and isoper(tokens[i - 2]):
            tokens.insert(i - 1, "(")
            tokens.insert(i, "0")
            tokens.insert(i + 3, ")")
        if debug: print("Tokens:", tokens)
        i += 1
    return tokens

def getpostfix(tokens, debug):
    prec, oper, output = {"^": 2, "*": 1, "/": 1, "+": 0, "-": 0}, [], []
    for token in tokens:
        if isnum(token): output.append(token)
        elif isoper(token):
            while len(oper) > 0 and not isopen(oper[-1]) and prec.get(oper[-1]) >= prec.get(token): output.append(oper.pop())
            oper.append(token)
        elif isopen(token): oper.append(token)
        elif isclose(token):
            while len(oper) > 0 and not isopen(oper[-1]): output.append(oper.pop())
            if len(oper) > 0: oper.pop()
        else: raise Exception("Syntax error: invalid token", token)
        if debug: print("Oper:", str(oper), "\nOutput:", str(output), "\n")
    while len(oper) > 0: output.append(oper.pop())
    return output

def evaluate(value1, value2, operation):
    if operation == "+": return decimal.Decimal(value1) + decimal.Decimal(value2)
    elif operation == "-": return decimal.Decimal(value1) - decimal.Decimal(value2)
    elif operation == "*": return decimal.Decimal(value1) * decimal.Decimal(value2)
    elif operation == "/": return decimal.Decimal(value1) / decimal.Decimal(value2)
    elif operation == "^": return decimal.Decimal(value1) ** decimal.Decimal(value2)
    else: return None

def getvalue(postfix):
    stack = []
    for token in postfix:
        if isoper(token):
            value2, value1 = stack.pop(), stack.pop()
            stack.append(evaluate(value1, value2, token))
        elif isnum(token): stack.append(token)
    return stack.pop()

def main(argv):
    argv.pop(0)
    argv = list(map(lambda arg: arg.lower(), argv))
    debug = "-d" in argv
    if debug: argv.remove("-d")
    expr = "".join(argv)
    print("Expr:", expr)
    tokens = gettokens(expr, debug)
    postfix = getpostfix(tokens, debug)
    if debug: print("Postfix:", "  ".join(postfix))
    value = getvalue(postfix)
    print("Result:", str(value))

main(sys.argv)