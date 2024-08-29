import allure
import pytest

from base.apiutil import RequestBase
from base.generateId import c_id, m_id
from common.readyaml import get_testcase_yaml
from common.sendrequest import SendRequest

@allure.feature(next(m_id) + '登录接口')
class TestLogin:

    # 修改之前的方法
    @allure.story(next(c_id) + "登录01")
    @pytest.mark.parametrize('params', get_testcase_yaml('./login.yaml'))
    def test_case(self, params):
        print(params)
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + str(url)  # 请求行
        method = params['baseInfo']['method']  # 请求方式
        header = params['baseInfo']['header']  # 请求头
        data = params['baseInfo'][0]['data']  # 请求体
        send = SendRequest()  # 这个类封装了请求方法
        res = send.run_main(url=new_url, data=data, header=header, method=method)
        print("接口实际返回值:" + res)

        assert res['msg'] == '登录成功'

    # 修改之后的方法
    @allure.story(next(c_id) + "登录02")
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/debugApi/addUser.yaml"))
    def test_case01(self,base_info,testcase):
        RequestBase().specification_yaml(base_info,testcase)
