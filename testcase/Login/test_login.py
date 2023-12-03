import pytest

from base.apiutil import RequestBase
from common.readyaml import get_testcase_yaml
from common.sendrequest import SendRequest

class TestLogin:

    # 修改之前的方法
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
    @pytest.mark.parametrize('params', get_testcase_yaml("./testcase/debugApi/addUser.yaml"))
    def test_case01(self,params):
        RequestBase().specification_yaml(params)
