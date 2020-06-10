import re

SQL_OPERATOR_URI_MAPPER = {
    'eq': '=',
    'neq': '<>',
    'gt': '>',
    'ge': '>=',
    'lt': '<',
    'le': '<=',
}


def convert_numeric_string(numeric: str):
    try:
        num = float(numeric)
        return num
    except ValueError:
        numeric_pattern = re.compile(r'((0(\.\d+)?)|([1-9]\d*(\.\d+)?))')
        match = re.search(numeric_pattern, numeric)
        if match:
            if numeric.upper().find('MB') != -1:
                return float(match[0]) / 1000
            else:
                return float(match[0])
    except TypeError:
        return None
