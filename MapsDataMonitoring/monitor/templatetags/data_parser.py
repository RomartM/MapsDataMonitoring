from django import template
import json

register = template.Library()

# Centralize Template Tags
template_tags = dict([
    ('single_span', '<span>%s</span>'),
    ('double_span', '<span>%s - %s</span>'),
    ('single_strike_span', '<span class=\"strike\">%s</span>'),
    ('single_new_span', '<span class=\"new\">%s</span>'),
    ('single_ol', '<ol>%s</ol>'),
    ('single_ul', '<ul>%s</ul>'),
    ('span_str', '<span class=\"value str\">%s</span></li>'),
    ('span_lst', '<span class=\"data lst \">%s</span></li>'),
    ('span_dict', '<span class=\"data dict \">%s</span></li>'),
    ('span_int', '<span class=\"value int\">%s</span></li>'),
    ('span_fl', '<span class=\"value fl\">%s</span></li>'),
    ('span_bool', '<span class=\"value bool\">%s</span></li>')
])


@register.filter
def to_title(text):
    """
    Description: Convert text to title type and remove underscores
    :param text: raw text
    :return: Converted text
    """
    return str(text).title().replace('_', ' ')


@register.filter
def with_end_char(text, char):
    """
    Description: Append an after character to a text
    :param text: raw text
    :param char: character to put
    :return: Appended Text (e.g. with_end_char("Accounts", ":")-> "Accounts:")
    """
    return str("").join([text, char])


@register.filter
def what_type(data):
    """
    Description: Identify the data type
    :param data: raw data (e.g. list, dict, str..)
    :return: Data type in a string format
    """
    return str(type(data)).split('\'')[1]


@register.filter
def index_wrap(data, index):
    """
    Description: Select an index from an array data
    :param data: array data
    :param index: index (e.g. 1,2,3, account_data,..)
    :return: Data inside the position index
    """
    return data[index]


@register.filter
def data_to_html(data):
    """
    Description: Converts string JSON data into HTML nested list.
    Function intended for templating usage (single data only)
    :param data: String JSON Data
    :return: HTML format JSON data
    """
    e = False
    error_template = "<br/>-Data Source: %s"
    m = ""
    try:
        data = json.loads(data)
    except json.JSONDecodeError as er:
        e = True
        m = m + "".join([error_template % er])
    except TypeError as er:
        e = True
        m = m + "".join([error_template % er])
    if e:
        return m
    return data_to_html_core(data)


def data_to_html_core(data):
    """
    Description: Core bootstrap of parsing string JSON data to HTML data. (Single Data Only)
    Function linked to data_to_html template_tag function
    :param data: String JSON Data
    :return: HTML format JSON data
    """
    data_type = type(data)
    temp = ""
    if data_type == str:
        temp = temp + "".join([to_str(data)])
    elif data_type == list:
        temp = temp + "".join([to_list(data)])
    elif data_type == dict:
        temp = temp + "".join([to_dict(data)])
    elif data_type == int:
        temp = temp + "".join([to_int(data)])
    elif data_type == float:
        temp = temp + "".join([to_float(data)])
    elif data_type == bool:
        temp = temp + "".join([to_bool(data)])
    return temp


def to_title_ex(text):
    """
    Description: Convert text to title type and remove underscores.
    ( Exclusive for core json to html conversion process)
    :param text: raw text
    :return: Converted text
    """
    return str(text).title().replace('_', ' ')


def with_end_char_ex(text, char):
    """
    Description: Append an after character to a text.
    ( Exclusive for core json to html conversion process)
    :param text: raw text
    :param char: character to put
    :return: Appended Text (e.g. with_end_char("Accounts", ":")-> "Accounts:")
    """
    return str("").join([text, char])


def to_str(string):
    """
    Description: Parse string JSON data to html styled data
    and verifies the data is not hyperlink.
    :param string: JSON item string values
    :return: html styled data
    """
    if not any(i in "://?=+" for i in string):
        return template_tags.get('single_span') % string
    else:
        return string


def to_int(integer):
    """
    Description: Parse integer JSON data to html styled data
    :param integer: JSON item integer values
    :return: html styled data
    """
    return template_tags.get('single_span') % str(integer)


def to_float(fl):
    """
    Description: Parse float JSON data to html styled data
    :param fl: JSON item float values
    :return: html styled data
    """
    return template_tags.get('single_span') % str(fl)


def to_bool(bol):
    """
    Description: Parse boolean JSON data to html styled data
    :param bol: JSON item boolean values
    :return: html styled data with humanize format
    """
    return template_tags.get('single_span') % "Yes" if bol else "No"


def to_dict(dictionary):
    """
    Description: Parse dictionary JSON data to html  styled data (Single Data Only)
    :param dictionary: Dictionary Data
    :return: html styled data with humanize format
    """
    temp = ""
    for i in dictionary:
        data_type = type(dictionary[i])
        temp = temp + "".join(["<li>", to_title_ex(with_end_char_ex(to_str(i), ":"))])
        if data_type == str:
            temp = temp + template_tags.get('span_str') % to_str(dictionary[i])
        elif data_type == list:
            temp = temp + template_tags.get('span_lst') % to_list(dictionary[i])
        elif data_type == dict:
            temp = temp + template_tags.get('span_dict') % to_dict(dictionary[i])
        elif data_type == int:
            temp = temp + template_tags.get('span_int') % to_int(dictionary[i])
        elif data_type == float:
            temp = temp + template_tags.get('span_fl') % to_float(dictionary[i])
        elif data_type == bool:
            temp = temp + template_tags.get('span_bool') % to_bool(dictionary[i])
    return "<ul>%s</ul>" % str(temp)


def to_list(lst):
    """
    Description: Parse list JSON data to html styled data (Single Data Only)
    :param lst: List Data
    :return: html styled data with humanized format
    """
    temp = ""
    li = "<li>"
    for i in lst:
        data_type = type(i)
        if data_type == str:
            temp = temp + li + template_tags.get('span_str') % to_str(i)
        elif data_type == list:
            temp = temp + li + template_tags.get('span_lst') % to_list(i)
        elif data_type == dict:
            temp = temp + li + template_tags.get('span_dict') % to_dict(i)
        elif data_type == int:
            temp = temp + li + template_tags.get('span_int') % to_int(i)
        elif data_type == float:
            temp = temp + li + template_tags.get('span_fl') % to_float(i)
        elif data_type == bool:
            temp = temp + li + template_tags.get('span_bool') % to_bool(i)
    return "<ol>%s</ol>" % str(temp)


@register.filter
def data_to_html_diff(data_1, data_2):
    """
    Description: Core bootstrap of parsing double string JSON data to HTML data.
    Integrated with humanized visual data difference.
    :param data_1: Base/Original string JSON data
    :param data_2: Fresh/New string JSON data
    :return: HTML styled data with data difference
    """
    e = False
    error_template = "<br/>-Data %s: %s"
    m = ""
    try:
        data_1 = json.loads(data_1)
    except json.JSONDecodeError as er:
        e = True
        m = m + "".join([error_template % (1, er)])
    except TypeError as er:
        e = True
        m = m + "".join([error_template % (1, er)])
    try:
        data_2 = json.loads(data_2)
    except json.JSONDecodeError as er:
        e = True
        m = m + "".join([error_template % (2, er)])
    except TypeError as er:
        e = True
        m = m + "".join([error_template % (2, er)])
    if e:
        return m
    data_type_1 = type(data_1)
    data_type_2 = type(data_2)
    temp = ""
    if data_type_1 == str and data_type_2 == str:
        temp = temp + "".join([to_str_diff(data_1, data_2)])
    elif data_type_1 == list and data_type_2 == list:
        temp = temp + "".join([to_list_diff(data_1, data_2)])
    elif data_type_1 == dict and data_type_2 == dict:
        temp = temp + "".join([to_dict_diff(data_1, data_2)])
    elif data_type_1 == int and data_type_2 == int:
        temp = temp + "".join([to_int_diff(data_1, data_2)])
    elif data_type_1 == float and data_type_2 == float:
        temp = temp + "".join([to_float_diff(data_1, data_2)])
    elif data_type_1 == bool and data_type_2 == bool:
        temp = temp + "".join([to_bool_diff(data_1, data_2)])
    return temp


def to_str_diff(string_1, string_2):
    """
    Description: Parse two string JSON data to html styled data, verifies data are the same
    and verifies the data is not hyperlink.
    :param string_1: Data_1 string JSON item value
    :param string_2: Data_2 string JSON item value
    :return: HTML styled data
    """
    if (not any(i in "://?=+" for i in string_1)) and (not any(i in "://?=+" for i in string_2)):
        if string_1 != string_2:
            return template_tags.get('double_span') % \
                   (template_tags.get('single_strike_span') % string_1,
                    template_tags.get('single_new_span') % string_2)
        return template_tags.get('single_span') % string_1
    else:
        return "".join([string_1, " - ", string_2])


def to_int_diff(integer_1, integer_2):
    """
    Description: Parse two integer JSON data to html styled data and verifies data are the same.
    :param integer_1: Data_1 integer JSON item value
    :param integer_2: Data_2 integer JSON item value
    :return: HTML styled data
    """
    if integer_1 != integer_2:
        return template_tags.get('double_span') % \
               (template_tags.get('single_strike_span') % integer_1,
                template_tags.get('single_new_span') % integer_2)
    return template_tags.get('single_span') % str(integer_1)


def to_float_diff(fl_1, fl_2):
    """
    Description: Parse two float JSON data to html styled data and verifies data are the same.
    :param fl_1: Data_1 float JSON item value
    :param fl_2: Data_2 float JSON item value
    :return: HTML styled data
    """
    if fl_1 != fl_2:
        return template_tags.get('double_span') % \
               (template_tags.get('single_strike_span') % fl_1,
                template_tags.get('single_new_span') % fl_2)
    return template_tags.get('single_span') % str(fl_1)


def to_bool_diff(bol_1, bol_2):
    """
    Description: Parse two boolean JSON data to html styled data and verifies data are the same.
    :param bol_1: Data_1 boolean JSON item value
    :param bol_2: Data_2 boolean JSON item value
    :return: HTML styled data
    """
    t = "Yes"
    f = "No"
    if bol_1 != bol_2:
        return template_tags.get('double_span') % \
               (template_tags.get('single_strike_span') % t if bol_1 else f,
                template_tags.get('single_new_span') % t if bol_2 else f)
    return template_tags.get('single_span') % t if bol_1 else f


def to_dict_diff(dictionary_1, dictionary_2):
    """
    Description: Parse dictionary JSON data to html styled data
    :param dictionary_1: Data_1 dictionary value
    :param dictionary_2: Data_2 dictionary value
    :return: html styled data with humanize format
    """
    temp = ""
    for i, j in zip(dictionary_1, dictionary_2):
        data_type_1 = type(dictionary_1[i])
        data_type_2 = type(dictionary_2[j])
        temp = temp + "".join(["<li>", to_title_ex(with_end_char_ex(to_str(i), ":"))])
        if data_type_1 == str and data_type_2 == str:
            temp = temp + template_tags.get('span_str') % to_str_diff(dictionary_1[i], dictionary_2[j])
        elif data_type_1 == list and data_type_2 == list:
            temp = temp + template_tags.get('span_lst') % to_list_diff(dictionary_1[i], dictionary_2[j])
        elif data_type_1 == dict and data_type_2 == dict:
            temp = temp + template_tags.get('span_dict') % to_dict_diff(dictionary_1[i], dictionary_2[j])
        elif data_type_1 == int and data_type_2 == int:
            temp = temp + template_tags.get('span_int') % to_int_diff(dictionary_1[i], dictionary_2[j])
        elif data_type_1 == float and data_type_2 == float:
            temp = temp + template_tags.get('span_fl') % to_float_diff(dictionary_1[i], dictionary_2[j])
        elif data_type_1 == bool and data_type_2 == bool:
            temp = temp + template_tags.get('span_bool') % to_bool_diff(dictionary_1[i], dictionary_2[j])
        else:
            temp = temp + (template_tags.get('single_strike_span') + " " + template_tags.get('single_new_span')) \
                   % (data_to_html_core(dictionary_1[i]), data_to_html_core(dictionary_2[j]))
    return template_tags.get('single_ul') % str(temp)


def to_list_diff(lst_1, lst_2):
    """
    Description: Parse list JSON data to html styled data
    :param lst_1: Data_1 list value
    :param lst_2: Data_2 list value
    :return: html styled data with humanize format
    """
    temp = ""
    li = "<li>"
    for i, j in zip(lst_1, lst_2):
        data_type_1 = type(i)
        data_type_2 = type(j)
        if data_type_1 == str and data_type_2 == str:
            temp = temp + li + template_tags.get('span_str') % to_str_diff(i, j)
        elif data_type_1 == list and data_type_2 == list:
            temp = temp + li + template_tags.get('span_lst') % to_list_diff(i, j)
        elif data_type_1 == dict and data_type_2 == dict:
            temp = temp + li + template_tags.get('span_dict') % to_dict_diff(i, j)
        elif data_type_1 == int and data_type_2 == int:
            temp = temp + li + template_tags.get('span_int') % to_int_diff(i, j)
        elif data_type_1 == float and data_type_2 == float:
            temp = temp + li + template_tags.get('span_fl') % to_float_diff(i, j)
        elif data_type_1 == bool and data_type_2 == bool:
            temp = temp + li + template_tags.get('span_bool') % to_bool_diff(i, j)
        else:
            temp = temp + (template_tags.get('single_strike_span') + " " + template_tags.get('single_new_span')) \
                   % (data_to_html_core(i), data_to_html_core(j))
    return template_tags.get('single_ol') % str(temp)




