import re


def convert_numeric_string(numeric):
    try:
        num = float(numeric)
        return num
    except ValueError:
        numeric_pattern = re.compile(r'((0(\.\d+)?)|([1-9]\d*(\.\d+)?))')
        match = re.search(numeric_pattern, numeric)
        if match:
            return int(match[0])
    except TypeError:
        return None