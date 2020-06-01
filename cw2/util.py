import collections
import datetime


def deep_update(base_dict: dict, update_dict: dict) -> dict:
    """Updates the base dictionary with corresponding values from the update dictionary, including nested collections. Not updated values are kept as is.

    Arguments:
        base_dict {dict} -- dictionary to be updated
        update_dict {dict} -- dictianry holding update values

    Returns:
        dict -- dictanry with updated values
    """
    for key, value in update_dict.items():
        # Update Recursively
        if isinstance(value, collections.Mapping):
            branch = deep_update(base_dict.get(key, {}), value)
            base_dict[key] = branch
        else:
            base_dict[key] = update_dict[key]
    return base_dict


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, collections.MutableSequence):
            keys = map(lambda i: new_key + "_" + str(i), range(len(v)))
            items.extend(zip(keys, v))
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_dict_to_tuple_keys(d: collections.MutableMapping):
    flat_dict = {}
    for k, v in d.items():
        if isinstance(v, collections.MutableMapping):
            sub_dict = flatten_dict_to_tuple_keys(v)
            flat_dict.update({(k, *sk): sv for sk, sv in sub_dict.items()})

        elif isinstance(v, collections.MutableSequence):
            flat_dict[(k,)] = v

    return flat_dict


def insert_deep_dictionary(d: collections.MutableMapping, t: tuple, value):
    if type(t) is tuple:
        if len(t) == 1:  # tuple contains only one key
            d[t[0]] = value
        else:  # tuple contains more than one key
            if t[0] not in d:
                d[t[0]] = dict()
            insert_deep_dictionary(d[t[0]], t[1:], value)
    else:
        d[t] = value


def format_time(time_in_secs: float) -> str:
    return str(datetime.timedelta(seconds=time_in_secs))


def shorten_param(_param_name):
    name_parts = _param_name.split('.')
    shortened_parts = '.'.join(map(lambda s: s[:3], name_parts[:-1]))
    shortened_leaf = ''.join(map(lambda s: s[0], name_parts[-1].split('_')))
    if shortened_parts:
        return shortened_parts + '.' + shortened_leaf
    else:
        return shortened_leaf