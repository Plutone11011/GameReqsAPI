import re, operator

OPERATOR_URI_MAPPER = {
    'eq': operator.eq,
    'neq': operator.ne,
    'gt': operator.gt,
    'ge': operator.ge,
    'lt': operator.lt,
    'le': operator.le,
}

# grouping of names of tables's column
SUBSECTIONS_GAME = {
    'info':['id', 'name','description','developer'],
    'minimum_requirements':['id', 'ram_min','cpu_min','gpu_min','OS_min','storage_min'],
    'recommended_requirements':['id', 'ram_rec','cpu_rec','gpu_rec','OS_rec','storage_rec']
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