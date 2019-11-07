import re


def exclude_special_char(data):
    result = re.sub(r'[-~—\\|+=\[\]*?;]', '', data.strip())
    if not result == "" and not result == " ":
        return result
    else:
        return False
