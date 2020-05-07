"""
通用返回参数
"""


class BaseResponse:
    def __init__(self,code="0",message="success"):
        self.code = code
        self.message = message
    code = "0"
    message = "success"

    def is_success(self):
        """
        判断返回结果是否为空
        :return:
        """
        if self.code == '0':
            return True
        else:
            return False


if __name__ == '__main__':

    import json
    from flask import jsonify,Flask

    app = Flask(__name__)
    app.run()
    a = BaseResponse("0", "success")
    print(a)
    b = json.dumps(a.__dict__)
    print(b)
    c = json.loads(b)
    bbb = jsonify({"a":123})
    print(bbb)