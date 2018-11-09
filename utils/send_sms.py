#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 17:38
# @Author  : Fred Yang
# @File    : send_sms.py
# @Role    : 发送短信/阿里大鱼


from utils import const
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
import uuid
import json


class SmsApi:
    def __init__(self, access_key_id, access_key_secret, REGION=const.REGION, DOMAIN=const.DOMAIN,
                 PRODUCT_NAME=const.PRODUCT_NAME):
        self.acs_client = AcsClient(access_key_id, access_key_secret, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    def send_sms(self, phone_numbers, sign_name, template_code, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        __business_id = uuid.uuid1()
        smsRequest.set_OutId(__business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)
        # 调用短信发送接口，返回json
        sms_response = self.acs_client.do_action_with_exception(smsRequest)

        ##业务处理
        return sms_response


if __name__ == '__main__':
    pass
    # obj = SmsApi(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET)
    #
    # data = "这是短信测试"
    # params = {
    #     "msg": data
    # }
    #
    # data = obj.send_sms(phone_numbers='10000000000', sign_name=const.sign_name, template_code=const.template_code,
    #                     template_param=params)
    #
    # resp = json.loads(data.decode('utf-8'))
    # print(resp)
