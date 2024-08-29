import time

import pytest
import allure

from common.dingRobot import send_dd_msg
from common.operJenkins import OperJenkins
from common.readyaml import get_testcase_yaml
from base.apiutil import RequestBase
from common.recordlog import logs
from common.connection import ConnectMysql

"""
-function：每一个函数或方法都会调用
-class：每一个类调用一次，一个类中可以有多个方法
-module：每一个.py文件调用一次，该文件内又有多个function和class
-session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module,整个会话只会运行一次
-autouse：默认为false，不会自动执行，需要手动调用，为true可以自动执行，不需要调用
- yield：前置、后置
"""


@pytest.fixture(autouse=True)
def start_test_and_end():
    logs.info('-------------接口测试开始--------------')
    yield
    logs.info('-------------接口测试结束--------------')


@pytest.fixture(scope='session', autouse=True)
@allure.story("登录")
def system_login():
    login_info_list = get_testcase_yaml('./data/loginName.yaml')
    RequestBase().specification_yaml(login_info_list[0][0],login_info_list[0][1])


@pytest.fixture(scope='session', autouse=True)
def datadb_init():
    """
    后置处理器，比如测试之后的数据清理
    数据库可以预先预置一批本次测试的数据，在测试完成之后将这批数据清理，就不会对系统造成影响，也不会产生脏数据
    :return:
    """
    # conn = ConnectMysql()
    # yield
    # sql = "delete from sys_user where login_name='test999'"
    # conn.delete(sql)
    # allure.attach('将测试数据清空', 'fixture后置', allure.attachment_type.TEXT)

    pass

def pytest_terminal_summary(terminalreporter,exitstatus,config):
    """
     pytest内置的钩子函数，函数名为固定写法不能变更，每次pytest测试完成后，会自动收集测试结果的数据
    :param terminalreporter: 内部使用的终端测试报告对象
    :param exitstatus: 返回给操作系统的返回码
    :param config: pytest配置对象
    :return:
    """
    # 测试用例总数
    case_total = terminalreporter._numcollected
    # 测试用例通过数
    passed = len(terminalreporter.stats.get('passed',[]))
    # 测试用例失败数
    failed = len(terminalreporter.stats.get('failed',[]))
    # 测试用例错误数
    error = len(terminalreporter.stats.get('error',[]))
    # 测试用例跳过数
    skipped = len(terminalreporter.stats.get('skipped',[]))
    # 测试用例执行时长
    duration = time.time() - terminalreporter._sessionstarttime
    # 测试报告的链接
    oper = OperJenkins()
    report = oper.get_report_link()

    # 需要发送的消息
    content = f"""
        各位好，本次xxx项目的接口自动化测试结果：
        测试用例总共：{case_total}个
        通过：{passed}个
        失败：{failed}个
        跳过：{skipped}个
        异常：{error}个
        测试用例时长：{duration}
        点击查看测试报告：{report}
    """
    send_dd_msg(content_str=content)