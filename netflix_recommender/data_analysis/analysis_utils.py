from itertools import groupby


def split_list(lst, val):
    return [list(group) for k, group in
            groupby(lst, lambda x: x == val) if not k]

