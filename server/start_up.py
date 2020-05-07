import os,logging,traceback
from flask import Flask,render_template
from threading import current_thread
from server import conf

# 参考：https://www.cnblogs.com/haolujun/p/9778939.html
# gc.freeze() #调用gc.freeze()必须在fork子进程之前，在gunicorn的这个地方调用正好合适，freeze把截止到当前的所有对象放入持久化区域，不进行回收，从而model占用的内存不会被copy-on-write。
# app = Flask(__name__,static_folder="./web/static",template_folder="./web/templates")
from server.web_processor.ocr_new_web_processor import OcrNewWebProcessor

app = Flask(__name__,root_path=os.path.join(os.getcwd(),"web"))
app.jinja_env.globals.update(zip=zip)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
logger = logging.getLogger(__name__)

def _logger():
    return logging.getLogger("WebServer")

@app.errorhandler(500)
def internal_server_error_500(e):
    print("异常发生：")
    traceback.print_exc()
    _logger().error("====================================异常堆栈为====================================", exc_info=True)
    _logger().info("==================================================================================")

@app.route("/")
def index():
    version = 1
    return render_template('index.html',version=version)

def init_log():
    level = logging.DEBUG,
    _format = "%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d行 %(message)s"

    print("设置日志等级：",level)

    logging.basicConfig(
        format=_format,
        level=level,
        handlers=[logging.StreamHandler()])


def startup(app):
    conf.init_arguments()
    init_log()

    _logger().debug('启动模式：%s,子进程:%s,父进程:%s,线程:%r', conf.MODE,os.getpid(), os.getppid(), current_thread())
    #TODO
    # ocr_utils.init_single(conf.MODE)

    # 注册所有的处理器
    regist_processor(app)
    logger.info("启动完毕！")

# 配置所有的处理器
def regist_processor(app):
    # 目前只有3个处理器
    processors = [OcrNewWebProcessor("ocr_new")]
    for _p in processors:

        _logger().info("--------------")
        _logger().info("注册处理器：%s",_p.name)

        app.add_url_rule(rule=_p.get_web_index_url(),
                         endpoint=_p.name+"_index",
                         view_func=_p.web_index,
                         methods=["GET"])
        _logger().info("注册了网页的Web处理函数：%s",_p.get_web_index_url())

        app.add_url_rule(rule=_p.get_web_post_url(),
                         endpoint=_p.name+"_post",
                         view_func=_p.web_post,
                         methods=["POST"])
        _logger().info("注册了网页Post处理函数：%s", _p.get_web_post_url())

        app.add_url_rule(rule=_p.get_resful_url(),
                         endpoint=_p.name+"_restful",
                         view_func=_p.restful,
                         methods=["POST"])
        _logger().info("注册了Restful Json处理函数：%s", _p.get_resful_url())


print("启动服务器...")
startup(app)