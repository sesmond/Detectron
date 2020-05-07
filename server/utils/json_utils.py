import json
import logging
from json import JSONDecodeError

logger = logging.getLogger(__name__)


def json_deserialize(json_data, obj):
    """
    反序列化为自定义对象
    :param json_data:
    :param obj:
    :return:
    """
    logger.debug("Got json data:%d bytes", len(json_data))
    try:
        data = json_data.decode('utf-8')
        data = data.replace('\r\n', '')
        data = data.replace('\n', '')
        data = json.loads(data)
    except JSONDecodeError as e:
        logger.error(data)
        logger.error("JSon数据格式错误")
        raise Exception("JSon数据格式错误:" + str(e))
    dic2class(data, obj)


def obj_2json(obj):
    pass


def dic2class(py_data, obj):
    for name in [name for name in dir(obj) if not name.startswith('_')]:
        if name not in py_data:
            setattr(obj, name, None)
        else:
            value = getattr(obj, name)
            setattr(obj, name, set_value(value, py_data[name]))


def set_value(value, py_data):
    if str(type(value)).__contains__('.'):
        # value 为自定义类
        dic2class(py_data, value)
    elif str(type(value)) == "<class 'list'>":
        # value为列表
        if value.__len__() == 0:
            # value列表中没有元素，无法确认类型
            value = py_data
        else:
            # value列表中有元素，以第一个元素类型为准
            child_value_type = type(value[0])
            value.clear()
            for child_py_data in py_data:
                child_value = child_value_type()
                child_value = set_value(child_value, child_py_data)
                value.append(child_value)
    else:
        value = py_data
    return value