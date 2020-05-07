#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Title   : 图片工具类
@File    :   image_utils.py    
@Author  : vincent
@Time    : 2020/5/7 5:50 下午
@Version : 1.0 
"""

import cv2
import numpy as np
import logging
from tools.tuning import RotateProcessor

logger = logging.getLogger(__name__)


def split_two(img):
    """
    一张图片拆成两张 TODO 阈值设定
    :param img:
    :return:
    """
    h, w = img.shape[:2]
    positons = split_image_vertical(img)
    if positons and len(positons)>0:
        max_cnt = 0
        max_pos = None
        for pos in positons:
            if pos[1] > max_cnt:
                max_pos = pos
                max_cnt = pos[1]
        split_pos = (max_pos[0]*2+ max_pos[1])//2
    else:
        split_pos = w // 2
    logger.info("图像分割点：%r", split_pos)
    # 切图 [y0: y1, x0: x1]
    img1 = img[0:h-1,0:split_pos]
    img2 = img[0:h-1,split_pos:w-1]

    rotate_processor = RotateProcessor()
    _, img1_rotate = rotate_processor.process(img1)
    _, img2_rotate = rotate_processor.process(img2)
    return img1_rotate,img2_rotate


def split_image_vertical(origin_img):
    """
        竖直图片，返回图片分割点的横向相对位置
    :param origin_img:
    :return:
    """
    # 灰度图
    image = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)

    # 将图片二值化
    ret_val, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    # 扩大黑色面积，使效果更明显
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # 形态学处理，定义矩形结构
    # 膨胀 TODO 是否要膨胀
    dilation = cv2.dilate(binary, kernel)
    # 水平投影
    horizon_result = getVProjection(dilation)

    positions = []
    # 判断连续多个 小于 的数值的中间值
    sp_start = 0  # 空格开始坐标
    sp_len = 0
    average_a = np.mean(horizon_result)
    median_a = np.median(horizon_result)
    thresh = average_a / 2
    for j in range(len(horizon_result)):
        # 如果个数和高度一样高，说明是竖线，暂不考虑分割
        # 如果有连续空格终止，则分割，没有的话则继续寻找
        # 连续10个像素为空则默认拆分,开头空格不拆分
        pix = horizon_result[j]
        if pix < thresh:
            if sp_len == 0:
                # 重新计数
                sp_start = j
            sp_len += 1
        else:
            # 出现大于的，保存之前数值重新计算
            if sp_len > 30:
                positions.append((sp_start,sp_len))
            sp_len = 0
    return positions


def getVProjection(image):
    """
        获取垂直投影的每一列白色像素个数
    :param image:
    :return:
    """
    # 图像高与宽
    (h, w) = image.shape
    # 长度与图像宽度一致的数组
    w_arr = [0] * w
    # 循环统计每一列白色像素的个数
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_arr[x] += 1
    return w_arr


if __name__ == '__main__':
    im =cv2.imread("data/1.jpg")
    img1,img2 = split_two(im)
    cv2.imwrite("data/output_1.jpg",img1 )
    cv2.imwrite("data/output_2.jpg",img2 )