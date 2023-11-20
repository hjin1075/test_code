import requests
from conf.operationConfig import OperationConfig
from conf.setting import LOGIN_HEADER
from common.recordlog import logs
from hashlib import sha1
import hashlib


class Session:
    """获取接口的Session值"""

    def __init__(self):
        self.conf = OperationConfig()

    def encrypt_md5(self, data):
        """md5密码加密"""
        enc_data = hashlib.md5()
        enc_data.update(data.encode(encoding='utf-8'))
        return enc_data.hexdigest()

    def encrypt_sha1(self, data):
        """sha1密码加密"""
        enc_data = sha1()
        enc_data.update(data.encode('utf-8'))
        # hexdigest转换为16进制
        return enc_data.hexdigest()

    def get_session(self, envir):
        """
        获取session值
        :param envir: 环境变量,测试/线上
        :return:
        """
        if envir == 'api_envm':
            url = self.conf.get_section_for_data('api_envm', 'host') + \
                  self.conf.get_section_for_data('api_envm', 'loginurl')
            parames = self.conf.get_section_for_data('api_envm', 'loginparam')
            # parames['password'] = self.encrypt_sha1(parames['password']) #参数加密
            response = requests.session().post(url=url, json=parames, headers=LOGIN_HEADER)
            logs.info(response.cookies)
            return response.cookies.get_dict()



        elif envir == 'release':
            url = self.conf.get_section_for_data('api_release', 'host') + \
                  self.conf.get_section_for_data('api_release', 'loginurl')
            parames = self.conf.get_section_for_data('api_release', 'loginparam')
            session_release = requests.session()
            response = session_release.post(url, parames, LOGIN_HEADER)
            logs.info(response.cookies)
            if response.cookies.get_dict() is not None:
                return response.cookies.get_dict()
            else:
                return None
        else:
            logs.error('session获取错误')
