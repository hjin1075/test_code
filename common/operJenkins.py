import json
import re
import jenkins
# ������Ҫ��װ��pip install python-jenkins
from conf.operationConfig import OperationConfig

class OperJenkins:
    """��ȡJenkins�������ɵĲ��Ա���"""
    conf = OperationConfig()

    def __init__(self):
        self.__config = {
            'url':self.conf.get_section_jenkins('url'),
            'username': self.conf.get_section_jenkins('username'),
            'password': self.conf.get_section_jenkins('password'),
            'timeout': int(self.conf.get_section_jenkins('timeout'))
        }
        self.__server = jenkins.Jenkins(**self.__config)
        # ��ȡ��Jenkins�ϵ���Ŀ��
        self.job_name = self.conf.get_section_jenkins('job_name')

    def get_report_link(self):
        """��ȡ���������"""
        console_log = self.get_console_log()
        report_line = re.search(r'http://127.0.0.1:8088/job/jjapi/(.*?)allure',console_log).group(0)
        return report_line

    def get_job_number(self):
        """��ȡjenkins job������"""
        build_number = self.__server.get_job_info(self.job_name).get('lastBuild').get('number')
        return build_number

    def get_build_job_stauts(self):
        """��ȡ������ɵ�״̬"""
        build_num = self.get_job_number()
        job_status = self.__server.get_job_info(self.job_name, build_num).get('result')
        return job_status

    def get_console_log(self):
        """��ȡ����̨��־"""
        console_log = self.__server.get_build_console_output(self.job_name, self.get_job_number())
        return console_log

    def get_job_description(self):
        """����job������Ϣ"""
        description = self.__server.get_job_info(self.job_name).get('description')
        url = self.__server.get_job_info(self.job_name).get('url')
        return description, url

    def get_build_report(self):
        """����n�ι����Ĳ��Ա���"""
        report = self.__server.get_build_test_report(self.job_name, self.get_job_number())
        return report