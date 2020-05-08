#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   :TODO
@File    :   detect_service.py    
@Author  : v
@Time    : 2020/5/7 11:11 下午
@Version : 1.0 
'''
import argparse

from tools import infer_simple, image_utils
from server.conf import cfg
from server.vo.request.ocr_request_vo import OcrRequest
import sys


class TempArgs:
    """
    OCR 请求报文
    """
    output_dir = "data/output"
    thresh = 0.2
    kp_thresh = 1.0
    output_ext = ".jpg"
    out_when_no_box = False


def detect(request: OcrRequest):
    img = image_utils.base64_2_image(request.img)
    dummy_coco_dataset = cfg.dummy_coco_dataset
    model = cfg.model_param
    img1, img2 = image_utils.split_two(img)
    base_name = "test.jpg"
    args = TempArgs()
    args.output_dir="data/output"
    args.thresh = 0.2
    args.kp_thresh= 1.0
    args.output_ext=".jpg"
    args.out_when_no_box = False

    new_img1 = infer_simple.single_process(args, dummy_coco_dataset, img1, base_name + "_1", model)
    new_img2 = infer_simple.single_process(args, dummy_coco_dataset, img2, base_name + "_2", model)
    result_base64 = []
    result_base64.append(image_utils.nparray2base64(new_img1))
    result_base64.append(image_utils.nparray2base64(new_img2))
    return result_base64


if __name__ == '__main__':
    print("")