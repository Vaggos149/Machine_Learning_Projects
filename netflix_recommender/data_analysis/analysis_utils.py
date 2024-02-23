from itertools import groupby


def split_list(listing, val):
    return [list(group) for k, group in
            groupby(listing, lambda x: x == val) if not k]

