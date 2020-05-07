class OcrRequest:
    """
    OCR 请求报文
    """
    # 检测model（ctpn/psenet等）
    detect_model = ''
    # 二值化阈值
    threshold = None
    # 是否返回debug图片
    do_verbose = False
    # 是否做文字矫正
    do_correct = False
    # 是否做版面行分析
    do_layout = False
    # 要识别的图片（base64格式）
    img = ''

    def __str__(self):
        return "detect_model:%s," \
               "threshold:%r," \
               "do_verbose:%r," \
               "do_correct:%r," \
               "do_layout:%r," \
               "img:%r," \
               "" % \
               (self.detect_model,
                self.threshold,
                self.do_verbose,
                self.do_correct,
                self.do_layout,
                len(self.img))

if __name__ == '__main__':
    req  =OcrRequest()
    req.do_layout=False
    # req.detect_model="psenet"

    # print(req.__str__())
    # print(req)
    # logger.info("qingca shu:%s",req)