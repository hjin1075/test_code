from base.removefile import remove_file
from common.readyaml import ReadYamlData
from common.recordlog import logs
from conf.setting import FILE_PATH

read = ReadYamlData()


# 暂时废弃
class BaseUtil:

    def setup_class(self):
        """每次测试用例执行前操作一次"""
        read.clear_yaml_data('extract.yaml')
        remove_file(FILE_PATH['TEMP'], ['json', 'txt'])
        remove_file(FILE_PATH['TMR'], ['html'])

    def setup(self):
        logs.info('接口测试用例执行开始'.center(60, '-'))

    def teardown(self):
        logs.info('接口测试用例执行结束'.center(60, '-'))

    def teardowm_class(self):
        pass

    def test_aa(self):
        pass
