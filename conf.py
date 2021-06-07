from c import FFParam
import json
conf_content = {}


def set_path(p):
    conf_content['path'] = p


def get_path():
    return conf_content.get('path', '')


def obj_to_dict(obj):
    dic = {}
    for a in filter(lambda x: not x.startswith('__'), dir(obj)):
        attr = getattr(obj, a)
        if not callable(attr):
            dic[a] = attr
    return dic


def dict_to_obj(dic):
    obj = FFParam()
    for a, attr in dic.items():
        setattr(obj, a, attr)
    return obj


def set_ff(ff):
    dic = obj_to_dict(ff)
    conf_content['ff'] = dic


def get_ff():
    dic = conf_content.get('ff')
    if dic:
        return dict_to_obj(dic)


def save():
    json_content = json.dumps(conf_content, ensure_ascii=False)
    print('json', json_content)
    text_file = open("conf.json", "w", encoding='utf-8')
    text_file.write(json_content)
    text_file.close()


def load():
    global conf_content
    with open('conf.json', 'r', encoding='utf-8') as file:
        conf_content = json.loads(file.read())


load()
print(conf_content)
