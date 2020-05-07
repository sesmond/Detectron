import json

from server.web_processor.web_processor import WebProcessor
from flask import jsonify, request, abort, render_template, Response
import logging, time
from server import conf
from server.vo.request.ocr_request_vo import OcrRequest
from server.vo.response.base_response import BaseResponse
from server.service import detect_service
from server.utils import json_utils

logger = logging.getLogger(__name__)


def validate(ocr_request:OcrRequest):
    """
       请求参数校验
       :return:
       """
    if not ocr_request.detect_model:
        raise ValueError("detect_model 不能为空")
    if not ocr_request.img:
        raise ValueError("img 不能为空")


class OcrNewWebProcessor(WebProcessor):

    def web_post(self):
        pass

    def restful(self):
        logger.info("请求url:%r", self.get_resful_url())

        try:
            ocr_request = OcrRequest()
            start = time.time()
            json_utils.json_deserialize(request.get_data(), ocr_request)
            logger.info("请求参数：%s", ocr_request)
            # 参数校验
            validate(ocr_request)

            result = detect_service.detect(ocr_request)
            logger.debug("识别图片花费[%d]秒", time.time() - start)
            # if success:
            #     result = json.dumps(response, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=False,
            #                         indent=4)
            #     return jsonify(json.loads(result))
            # else:
            return jsonify(result)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("处理图片过程中出现问题：%r", e)
            return jsonify(BaseResponse("9999", str(e)).__dict__)

# ?            return jsonify({'error_code': -1, 'message': str(e)})


