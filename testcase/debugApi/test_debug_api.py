import allure
import pytest

from common.readyaml import get_testcase_yaml
from base.apiutil import RequestBase
from common.recordlog import logs


@allure.feature('公用接口，供调试使用')
class TestDebugApi:

    def setup_class(self):
        """执行测试类之前，需要做的操作"""
        logs.info('环境初始化....')

    # 场景，allure报告的目录结构
    @allure.story("新增用户")
    # 测试用例执行顺序设置
    @pytest.mark.run(order=1)
    # 参数化，yaml数据驱动
    @pytest.mark.parametrize('case_info', get_testcase_yaml("./testcase/debugApi/addUser.yaml"))
    def test_add_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    @allure.story("修改用户")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('case_info', get_testcase_yaml("./testcase/debugApi/updateUser.yaml"))
    def test_update_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    @allure.story("删除用户")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('case_info', get_testcase_yaml("./testcase/debugApi/deleteUser.yaml"))
    def test_delete_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    @allure.story("查询用户")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('case_info', get_testcase_yaml("./testcase/debugApi/queryUser.yaml"))
    def test_query_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    def teardown_class(self):
        """该测试类的后置操作，如环境清除、数据恢复"""
        logs.info('正在清理测试数据....')
