__all__ = ['TAG_TUPLE_STRING_PARSERS']

import re


TAG_TUPLE_STRING_PARSERS = []


def pep440(tag_str):
    """
    Parse tag_str in accordance with PEP440.

    https://www.python.org/dev/peps/pep-0440/
    """
    # Strip common non-numeric numbers from beginning of string
    tag_str = tag_str.lstrip('v')
    # Pull epoch from tag string
    epoch = 0
    if '!' in tag_str:
        index = tag_str.index('!')
        epoch = int(tag_str[:index])
        tag_str = tag_str[index + 1:]
    version_list = [epoch]
    for chunk in tag_str.split('.'):
        try:
            version_list.append(int(chunk))
        except ValueError:
            return None  # Drop support for a/b/rc/post/dev releases
            match = re.match('^(\d+)([ab]|rc){1}(\d+)$', chunk)
            if match:
                version_list.append(int(match.group(1)))
                version_list.append(int(match.group(3)))
                continue
            match = re.match('^post(\d+)$', chunk)
            if match:
                version_list.append(int(match.group(1)))
                continue
            match = re.match('^dev(\d+)$', chunk)
            if match:
                version_list.append(int(match.group(1)))
                continue
            version_list.append(0)
    return tuple(version_list[1:])  # Drop epoch
TAG_TUPLE_STRING_PARSERS.append(pep440)

