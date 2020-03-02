import re


def exclude_special_char(data):
    result = re.sub(r'[-~—\\|=\[\]*?;]', '', data.strip())
    if not result == "" and not result == " ":
        return result
    else:
        return False


def has_match(match):
    groups = match.groups()
    index = 0
    for group in groups:
        if group is not None:
            return index, group.strip()
        index += 1
    return None


def get_empty_output(indexes):
    output = {}
    for item in indexes:
        output[item] = None
    return output
