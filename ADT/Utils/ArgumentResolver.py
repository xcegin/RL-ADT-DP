

def resolveArguments(arguments, resolverUtil):
    args = []
    for value in arguments["$values"]:
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        variable = resolveNodeViaType(value["$type"], value, resolverUtil)
        args.append(variable)
    return args