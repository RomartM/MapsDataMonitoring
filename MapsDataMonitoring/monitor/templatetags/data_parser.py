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





