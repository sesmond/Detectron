import os, sys
from configparser import ConfigParser
import logging

################################################################
#
#   定义CTPN、CRNN的共同参数
#
################################################################

# 定义相关的目录，这个是为了方便3个项目集成，所以需要绝对路径，方便import，不是为了找文件，找文件用相对路径就好，是为了python import
CTPN_DRAW = True
CTPN_SAVE = False  # 是否保存识别的坐标
CTPN_EVALUATE = False  # 是否提供评估
CTPN_SPLIT = True  # 是否保留小框(CTPN网络识别结果）
CTPN_PRED_DIR = "data/pred"  # 保存的内容存放的目录
CTPN_TEST_DIR = "data/test"  #

# 启动模式：2种
MODE_TFSERVING = "tfserving"
MODE_SINGLE = "single"

# CRNN常用参数
CRNN_BATCH_SIZE = 128
CRNN_INPUT_SIZE = (32, 1024)
CRNN_SEQ_LENGTH = 256
CRNN_PROCESS_NUM = 2  # 处理CRNN识别的分几个批次

# 通用的调试开关
DEBUG = True

# 全局变量
ctpn_params = None
charset = None
crnn_params = None
psenet_params = None

logger = logging.getLogger(__name__)
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'


class Config:
    def __init__(self, conf_file="ocr.cfg"):
        # 基础配置
        self.model_param = None
        self.dummy_coco_dataset = None


# 定义各类参数
def init_arguments():
    import detectron.core.test_engine as infer_engine
    from detectron.core.config import merge_cfg_from_file
    import detectron.datasets.dummy_datasets as dummy_datasets

    merge_cfg_from_file("../models/config_X101.yaml")
    cfg.model_param = infer_engine.initialize_model_from_cfg("../models/model_final.pkl")
    cfg.dummy_coco_dataset = dummy_datasets.get_coco_dataset()

    logger.info("参数初始化完成,启动模式：%s", 'single')


cfg = Config()

if __name__ == '__main__':
    Config()