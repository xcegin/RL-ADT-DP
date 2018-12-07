import random
import sys
from decimal import Decimal
from math import sin, cos, tan, pi

NOT_VALID = "NOT_VALID"


def resolveMathOperation(numOfAction, value, type):
    if not isNumerical(type):
        return NOT_VALID
    if numOfAction == 0:
        return resolveMin(type)
    elif numOfAction == 1:
        return resolveMax(type)
    elif numOfAction == 2:
        return pi
    elif numOfAction == 3:
        return Decimal(value) + 0.001
    elif numOfAction == 4:
        return Decimal(value) + 0.01
    elif numOfAction == 5:
        return Decimal(value) + 0.1
    elif numOfAction == 6:
        return Decimal(value) + 1
    elif numOfAction == 7:
        return Decimal(value) + 10
    elif numOfAction == 8:
        return Decimal(value) + 100
    elif numOfAction == 9:
        return Decimal(value) - 0.001
    elif numOfAction == 10:
        return Decimal(value) - 0.01
    elif numOfAction == 11:
        return Decimal(value) - 0.1
    elif numOfAction == 12:
        return Decimal(value) - 1
    elif numOfAction == 13:
        return Decimal(value) - 10
    elif numOfAction == 14:
        return Decimal(value) - 100
    elif numOfAction == 15:
        return Decimal(value) * 1.1
    elif numOfAction == 16:
        return Decimal(value) * 1.5
    elif numOfAction == 17:
        return Decimal(value) * 2
    elif numOfAction == 18:
        return Decimal(value) * 5
    elif numOfAction == 19:
        return Decimal(value) * 10
    elif numOfAction == 20:
        return Decimal(value) * 100
    elif numOfAction == 21:
        return Decimal(value) * 1000
    elif numOfAction == 22:
        return Decimal(value) / 1.1
    elif numOfAction == 23:
        return Decimal(value) / 1.5
    elif numOfAction == 24:
        return Decimal(value) / 2
    elif numOfAction == 25:
        return Decimal(value) / 5
    elif numOfAction == 26:
        return Decimal(value) / 10
    elif numOfAction == 27:
        return Decimal(value) / 100
    elif numOfAction == 28:
        return Decimal(value) / 1000
    elif numOfAction == 29:
        return Decimal(value) ** 2
    elif numOfAction == 30:
        return Decimal(value) ** (1 / 2)
    elif numOfAction == 31:
        return sin(Decimal(value))
    elif numOfAction == 32:
        return cos(Decimal(value))
    elif numOfAction == 33:
        return tan(Decimal(value))
    elif numOfAction == 34:
        return 0
    elif numOfAction == 35:
        return 1


def resolveMin(type):
    if type == "t_int":
        return -2147483648
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
        return True
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
