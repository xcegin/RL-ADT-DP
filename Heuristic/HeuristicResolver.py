# TODO should be all the variables, not just the arguments for the small operation, abs is fine propably ->
# TODO ideally track data dependencies
from Enviroment.MathOperationsUtil import smallestValue


def resolveHeuristic(valuesOfArguments, arguments, heuristic):
    componentOfHeuristic = heuristic[0].split("+")
    finalValue = 0
    for component in componentOfHeuristic:
        componentValue = 0
        if "abs" in component:
            component = component.replace("(", "")
            component = component.replace(")", "")
            component = component.replace("abs", "")
            args = component.split(" ")
            substract = False
            for argument in args:
                if argument in valuesOfArguments and not substract:
                    componentValue += valuesOfArguments[argument]
                elif argument in valuesOfArguments and substract:
                    componentValue -= valuesOfArguments[argument]
                elif argument == "-":
                    substract = True
                elif isint(argument):
                    if substract:
                        componentValue -= int(argument)
                    else:
                        componentValue += int(argument)
                elif isfloat(argument):
                    if substract:
                        componentValue -= float(argument)
                    else:
                        componentValue += float(argument)
            finalValue += componentValue
        elif "small" in component:
            component = component.replace("(", "")
            component = component.replace(")", "")
            component = component.replace("small", "")
            component = component.replace(" ", "")
            if component in arguments:
                componentValue += smallestValue(arguments[component].variableType)
            finalValue += componentValue
    return finalValue


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False