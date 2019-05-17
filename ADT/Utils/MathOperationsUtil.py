import random
import sys
from decimal import Decimal
from math import sin, cos, tan, pi

NOT_VALID = "NOT_VALID"


def resolveMathOperation(numOfAction, value, type):

    def interMathOperation():
        if not isNumerical(type):
            return NOT_VALID
        elif numOfAction == 0:
            return float(value) + 1
        elif numOfAction == 1:
            return float(value) - 1
        elif numOfAction == 2:
            return float(value) * 2
        elif numOfAction == 3:
            return float(value) / 2
        elif numOfAction == 4:
            return 0
        elif numOfAction == 5:
            return 1
        elif numOfAction == 6:
            return value
        elif numOfAction == 7:
            return float(value) + 20
        elif numOfAction == 8:
            return float(value) - 20

    value = interMathOperation()
    return correctValue(value, type)


def resolveContinuousType(action, type):
    return correctContinuous(action, type)

def resolveContinuousTypeWithOperation(action, type, value):
    return correctContinuousWithOperation(action, type, value)

def resolveMin(type):
    if type == "t_int":
        return -2147483647
    elif type == "t_char16_t":
        return -32768
    elif type == "t_char":
        return -127
    elif type == "t_char32_t":
        return -2147483648
    # TODO: REINVENT BOOL OPERATIONS - This should not be here, heuristic deals with them, so somehow fix it probs - or return 0/1
    elif type == "t_bool":
        return False
    elif type == "t_wchar_t":
        return 0
    elif type == "t_int128":
        return -9223372036854775807
        # TODO: Return different values for the coverage tool
    elif type == "t_float128" or type == "t_double":
        return float('-inf')
    elif type == "t_float":
        return float('-inf')
    elif type == "t_decimal128":
        return float('-inf')
    elif type == "t_decimal32":
        return float('-inf')
    elif type == "t_decimal64":
        return float('-inf')


def correctValue(value, type):
    if type == "t_int":
        return int(value)
    elif type == "t_char16_t":
        return int(value)
    elif type == "t_char":
        return int(value)
    elif type == "t_char32_t":
        return int(value)
    # TODO: REINVENT BOOL OPERATIONS - This should not be here, heuristic deals with them, so somehow fix it probs - or return 0/1
    elif type == "t_bool":
        return int(value)
    elif type == "t_wchar_t":
        return int(value)
    elif type == "t_int128":
        return int(value)
        # TODO: Return different values for the coverage tool
    elif type == "t_float128" or type == "t_double":
        return round(float(value),2)
    elif type == "t_float":
        return round(float(value),2)
    elif type == "t_decimal128":
        return round(float(value),2)
    elif type == "t_decimal32":
        return round(float(value),2)
    elif type == "t_decimal64":
        return round(float(value),2)
    elif type == "t_unspecified":
        return int(value)


def correctContinuous(value, type):
    #if int(value) == -1:  # This leads to destabilization of the algorithm logically
    #    return 0
    #if int(value) == 1:  # This leads to destabilization of the algorithm logically
    #    return 1
    if type == "t_int" or type == 't_int128' or type == 't_unspecified':
        return int(value * 130)  # TODO: TEMPORARY
    elif type == "t_char16_t":
        return int(value * 130)
    elif type == "t_char":
        return int(value * 130)
    elif type == "t_char32_t":
        return int(value * 130)
    # TODO: REINVENT BOOL OPERATIONS
    elif type == "t_bool":
        return int(value)
    elif type == "t_wchar_t":
        return int(value * 130)
        # TODO: Return different values for the coverage tool
    elif type == "t_float128" or type == "t_double":
        return round(float(2**1022),2)
    elif type == "t_float":
        return round(float(2**1022),2)
    elif type == "t_decimal128":
        return round(float(2**1022),2)
    elif type == "t_decimal32":
        return round(float(2**1022),2)
    elif type == "t_decimal64":
        return round(float(2**1022),2)

def correctContinuousWithOperation(action, type, value):
    #if int(value) == -1:  # This leads to destabilization of the algorithm logically
    #    return 0
    #if int(value) == 1:  # This leads to destabilization of the algorithm logically
    #    return 1
    toBeValue = 0
    if action[0] <= -0.6:
        try:
            toBeValue = int(value) / int(action[1] * 100)
        except:
            toBeValue = int(value)
    elif -0.6 < action[0] <= -0.2:
        toBeValue = int(value) - int(action[1] * 100)
    elif -0.2 < action[0] <= 0.2:
        toBeValue = int(value)
    elif 0.2 < action[0] <= 0.6:
        toBeValue = int(value) + int(action[1] * 100)
    elif action[0] > 0.6:
        toBeValue = int(value) * int(action[1] * 100)
    if toBeValue < -32768:
        return -32785
    elif toBeValue > 32767:
        return 32766
    else:
        return int(toBeValue)



def isNumerical(type):
    if type == "t_int":
        return True
    elif type == "t_char16_t":
        return True
    elif type == "t_char":
        return True
    elif type == "t_char32_t":
        return True
    elif type == "t_bool":
        return False
    elif type == "t_wchar_t":
        return True
    elif type == "t_int128":
        return True
    elif type == "t_float128" or type == "t_double":
        return True
    elif type == "t_float":
        return True
    elif type == "t_decimal128":
        return True
    elif type == "t_decimal32":
        return True
    elif type == "t_decimal64":
        return True
    elif type == "t_unspecified":  # TODO CUZ ECLIPSE IS SHIT FOR STUPID PEOPLE
        return True
    else:
        return False


def resolveMax(type):
    if type == "t_int":
        return 2147483648
    elif type == "t_char16_t":
        return 32768
    elif type == "t_char":
        return 128
    elif type == "t_char32_t":
        return 2147483648
    elif type == "t_bool":
        return 1
    elif type == "t_wchar_t":
        return 65535
    elif type == "t_int128":
        return 9223372036854775807
        # TODO: Return different values for the coverage tool
    elif type == "t_float128" or type == "t_double":
        return float('inf')
    elif type == "t_float":
        return float('inf')
    elif type == "t_decimal128":
        return float('inf')
    elif type == "t_decimal32":
        return float('inf')
    elif type == "t_decimal64":
        return float('inf')


def randomValue(type):
    if "t_int" in type.typeName or "t_char32_t" in type.typeName:
        return random.randint(-2147483648, 2147483648)
    elif "t_char" in type.typeName:
        return random.randint(-127, 128)
    elif "t_int128" in type.typeName:
        return random.randint(-9223372036854775807, 9223372036854775807)
    elif "t_float" in type.typeName or "t_double" in type.typeName:
        return round(random.uniform(sys.float_info.min, sys.float_info.max), 4)


def smallestValue(type):
    if "t_int" in type or "t_char32_t" in type:
        return 1
    elif "t_char" in type:
        return 1
    elif "t_int128" in type:
        return 1
    elif "t_float" in type or "t_double" in type:
        return 0.0001
