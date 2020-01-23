__author__ = 'mnowotka'

# ----------------------------------------------------------------------------------------------------------------------

NUMBER_FILTERS = ['exact', 'range', 'gt', 'gte', 'lt', 'lte', 'in', 'isnull']
FLAG_FILTERS = ['exact', 'isnull']
CHAR_FILTERS = ['exact', 'iexact', 'contains', 'icontains', 'istartswith', 'startswith', 'endswith', 'iendswith',
                'search', 'regex', 'iregex', 'isnull', 'in']
DATE_FILTERS = ['exact', 'year', 'month', 'day', 'week_day', 'isnull']
STANDARD_RDKIT_COLORS = {16: (0.8, 0.8, 0), 1: (0.55, 0.55, 0.55), 35: (0.5, 0.3, 0.1), 17: (0, 0.8, 0),
                         0: (0.5, 0.5, 0.5), 7: (0, 0, 1), 8: (1, 0, 0), 9: (0.2, 0.8, 0.8), 15: (1, 0.5, 0)}

# ----------------------------------------------------------------------------------------------------------------------


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# ----------------------------------------------------------------------------------------------------------------------


def list_flatten(l, a=None):
    if a is None:
        a = []
    for i in l:
        if isinstance(i, list):
            list_flatten(i, a)
        else:
            a.append(i)
    return a

# ----------------------------------------------------------------------------------------------------------------------


def unpack_request_params(params):
    ret = []
    for x in params:
        first, second = x
        if type(second) == list and len(second) == 1 and isinstance(second[0], str):
            ret.append((first, second[0]))
        else:
            ret.append(x)
    return ret

# ----------------------------------------------------------------------------------------------------------------------