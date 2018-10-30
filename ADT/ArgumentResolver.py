

def resolveArguments(arguments):
    args = []
    for value in arguments["$values"]:
        from ADT.ResolverUtil import resolveNodeViaType
        variable = resolveNodeViaType(value["$type"], value)
        args.append(variable)
    return args