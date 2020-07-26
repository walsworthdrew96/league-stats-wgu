from django import template
import os

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def list_item_minus_one(lst, i):
    try:
        newlist = sorted(lst, key=lambda x: x.name)
        # print(f'''lst[{i - 1}]: {lst[i - 1]}''')
        # print(f'''newlist[{i - 1}]: {newlist[i - 1]}''')
        return newlist[i - 1]
    except:
        return None


@register.filter
def champion_ability_q1_is_null(lst, i):
    try:
        newlist = sorted(lst, key=lambda x: x.name)
        return newlist[i - 1].ability_q1 is not None
    except:
        return None


@register.filter
def list_item0(lst, i):
    try:
        newlist = sorted(lst, key=lambda x: x.name)
        return newlist[i]
    except:
        return None


@register.filter
def space_to_underscore(string_value):
    try:
        # print("string_value:", string_value, '->', string_value.replace(' ', '_'))
        return string_value.replace(' ', '_')
    except:
        return None


@register.filter
def get_value_from_dict(dictionary, key):
    try:
        if key:
            # print(f'dictionary[{key}]: {dictionary[key]}')
            return dictionary.get(key)
    except Exception as e:
        print(e)
        return None


@register.filter
def split_list(source_str, split_char):
    try:
        if source_str is not None:
            return source_str.split(split_char)
    except Exception as e:
        print(e)
        return None
