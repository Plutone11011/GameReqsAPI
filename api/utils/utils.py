import re
from enum import IntEnum

SQL_OPERATOR_URI_MAPPER = {
    'eq': '=',
    'neq': '<>',
    'gt': '>',
    'ge': '>=',
    'lt': '<',
    'le': '<=',
}

# grouping of names of tables's column
SUBSECTIONS_GAME = {
    'info':['name','description','developer'],
    'minimum_requirements':['ram_min','cpu_min','gpu_min','OS_min','storage_min'],
    'recommended_requirements':['ram_rec','cpu_rec','gpu_rec','OS_rec','storage_rec']
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


class GameEnum(IntEnum):
    NAME = 0,
    DESCRIPTION = 1,
    DEVELOPER = 2,
    RAM_MIN = 3,
    CPU_MIN = 4,
    GPU_MIN = 5,
    OS_MIN = 6,
    STORAGE_MIN = 7,
    RAM_REC = 8,
    CPU_REC = 9,
    GPU_REC = 10,
    OS_REC = 11,
    STORAGE_REC = 12