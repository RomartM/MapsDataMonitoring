from django import template

register = template.Library()


@register.filter
def to_title(text):
    return str(text).title().replace('_', ' ')


@register.filter
def with_end_char(text, char):
    return str("").join([text, char])


@register.filter
def what_type(data):
    return str(type(data)).split('\'')[1]


@register.filter
def index_wrap(data, index):
    return data[index]


@register.filter
def data_to_html(data):
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
    return str(text).title().replace('_', ' ')


def with_end_char_ex(text, char):
    return str("").join([text, char])


def to_str(string):
    temp = "<span>%s</span>"
    if not any(i in "://?=+" for i in string):
        return temp % string
    else:
        return string


def to_int(integer):
    return "<span>%s</span>" % str(integer)


def to_float(fl):
    return "<span>%s</span>" % str(fl)


def to_bool(bol):
    return "<span>%s</span>" % "Yes" if bol else "No"


def to_dict(dictionary):
    temp = ""
    for i in dictionary:
        data_type = type(dictionary[i])
        temp = temp + "".join(["<li>", to_title_ex(with_end_char_ex(to_str(i), ":"))])
        if data_type == str:
            temp = temp + "".join(["<span class=\"value str\">", to_str(dictionary[i]), "</span>", "</li>"])
        elif data_type == list:
            temp = temp + "".join(["<span class=\"data lst \">", to_list(dictionary[i]), "</span>", "</li>"])
        elif data_type == dict:
            temp = temp + "".join(["<span class=\"data dict \">", to_dict(dictionary[i]), "</span>", "</li>"])
        elif data_type == int:
            temp = temp + "".join(["<span class=\"value int\">", to_int(dictionary[i]), "</span>", "</li>"])
        elif data_type == float:
            temp = temp + "".join(["<span class=\"value fl\">", to_float(dictionary[i]), "</span>", "</li>"])
        elif data_type == bool:
            temp = temp + "".join(["<span class=\"value bool\">", to_bool(dictionary[i]), "</span>", "</li>"])
    return "<ul>%s</ul>" % str(temp)


def to_list(lst):
    temp = ""
    for i in lst:
        data_type = type(i)
        if data_type == str:
            temp = temp + "".join(["<li><span class=\"value str\">", to_str(i), "</span></li>"])
        elif data_type == list:
            temp = temp + "".join(["<li><span class=\"data lst \">", to_list(i), "</span></li>"])
        elif data_type == dict:
            temp = temp + "".join(["<li><span class=\"data dict \">", to_dict(i), "</span></li>"])
        elif data_type == int:
            temp = temp + "".join(["<li><span class=\"value int\">", to_int(i), "</span></li>"])
        elif data_type == float:
            temp = temp + "".join(["<li><span class=\"value fl\">", to_float(i), "</span></li>"])
        elif data_type == bool:
            temp = temp + "".join(["<li><span class=\"value bool\">", to_bool(i), "</span></li>"])
    return "<ol>%s</ol>" % str(temp)


@register.filter
def data_to_html_diff(data_1, data_2):
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
    temp = "<span>%s - %s</span>"
    if (not any(i in "://?=+" for i in string_1)) and (not any(i in "://?=+" for i in string_2)):
        if string_1 != string_2:
            return temp % ("<span class=\"strike\">%s</span>" % string_1,
                           "<span class=\"new\">%s</span>" % string_2)
        return temp % (string_1, string_2)
    else:
        return "".join([string_1, " - ", string_2])


def to_int_diff(integer_1, integer_2):
    temp = "<span>%s - %s</span>"
    if integer_1 != integer_2:
        return temp % ("<span class=\"strike\">%s</span>" % integer_1,
                       "<span class=\"new\">%s</span>" % integer_2)
    return temp % (str(integer_1), str(integer_2))


def to_float_diff(fl_1, fl_2):
    temp = "<span>%s - %s</span>"
    if fl_1 != fl_2:
        return temp % ("<span class=\"strike\">%s</span>" % fl_1,
                       "<span class=\"new\">%s</span>" % fl_2)
    return temp % (str(fl_1), str(fl_2))


def to_bool_diff(bol_1, bol_2):
    temp = "<span>%s - %s</span>"
    if bol_1 != bol_2:
        return temp % ("<span class=\"strike\">%s</span>" % "Yes" if bol_1 else "No",
                       "<span class=\"new\">%s</span>" % "Yes" if bol_2 else "No")
    return temp % ("Yes" if bol_1 else "No", "Yes" if bol_2 else "No")


def to_dict_diff(dictionary_1, dictionary_2):
    temp = ""
    for i, j in zip(dictionary_1, dictionary_2):
        data_type_1 = type(dictionary_1[i])
        data_type_2 = type(dictionary_2[j])
        temp = temp + "".join(["<li>", to_title_ex(with_end_char_ex(to_str(i), ":"))])
        if data_type_1 == str and data_type_2 == str:
            temp = temp + "".join(["<span class=\"value str\">", to_str_diff(dictionary_1[i], dictionary_2[j]), "</span>", "</li>"])
        elif data_type_1 == list and data_type_2 == list:
            temp = temp + "".join(["<span class=\"data lst \">", to_list_diff(dictionary_1[i], dictionary_2[j]), "</span>", "</li>"])
        elif data_type_1 == dict and data_type_2 == dict:
            temp = temp + "".join(["<span class=\"data dict \">", to_dict_diff(dictionary_1[i], dictionary_2[j]), "</span>", "</li>"])
        elif data_type_1 == int and data_type_2 == int:
            temp = temp + "".join(["<span class=\"value int\">", to_int_diff(dictionary_1[i], dictionary_2[j]), "</span>", "</li>"])
        elif data_type_1 == float and data_type_2 == float:
            temp = temp + "".join(["<span class=\"value fl\">", to_float_diff(dictionary_1[i], dictionary_2[j]), "</span>", "</li>"])
        elif data_type_1 == bool and data_type_2 == bool:
            temp = temp + "".join(["<span class=\"value bool\">", to_bool_diff(dictionary_1[i], dictionary_2[j]), "</span>", "</li>"])
        else:
            temp = temp + "<span class=\"strike\">%s</span>  <span class=\"new\">%s</span>" % (data_to_html(dictionary_1[i]), data_to_html(dictionary_2[j]))
    return "<ul>%s</ul>" % str(temp)


def to_list_diff(lst_1, lst_2):
    temp = ""
    for i, j in zip(lst_1, lst_2):
        data_type_1 = type(i)
        data_type_2 = type(j)
        if data_type_1 == str and data_type_2 == str:
            temp = temp + "".join(["<li><span class=\"value str\">", to_str_diff(i, j), "</span></li>"])
        elif data_type_1 == list and data_type_2 == list:
            temp = temp + "".join(["<li><span class=\"data lst \">", to_list_diff(i, j), "</span></li>"])
        elif data_type_1 == dict and data_type_2 == dict:
            temp = temp + "".join(["<li><span class=\"data dict \">", to_dict_diff(i, j), "</span></li>"])
        elif data_type_1 == int and data_type_2 == int:
            temp = temp + "".join(["<li><span class=\"value int\">", to_int_diff(i, j), "</span></li>"])
        elif data_type_1 == float and data_type_2 == float:
            temp = temp + "".join(["<li><span class=\"value fl\">", to_float_diff(i, j), "</span></li>"])
        elif data_type_1 == bool and data_type_2 == bool:
            temp = temp + "".join(["<li><span class=\"value bool\">", to_bool_diff(i, j), "</span></li>"])
        else:
            temp = temp + "<span class=\"strike\">%s</span>  <span class=\"new\">%s</span>" % (data_to_html(i), data_to_html(j))
    return "<ol>%s</ol>" % str(temp)




