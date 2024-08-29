import allure
import pytest

from base.apiutil import RequestBase
from base.generateId import c_id, m_id
from common.readyaml import get_testcase_yaml
from common.sendrequest import SendRequest

@allure.feature(next(m_id) + '��¼�ӿ�')
class TestLogin:

    # �޸�֮ǰ�ķ���
    @allure.story(next(c_id) + "��¼01")
    @pytest.mark.parametrize('params', get_testcase_yaml('./login.yaml'))
    def test_case(self, params):
        print(params)
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + str(url)  # ������
        method = params['baseInfo']['method']  # ����ʽ
        header = params['baseInfo']['header']  # ����ͷ
        data = params['baseInfo'][0]['data']  # ������
        send = SendRequest()  # ������װ�����󷽷�
        res = send.run_main(url=new_url, data=data, header=header, method=method)
        print("�ӿ�ʵ�ʷ���ֵ:" + res)

        assert res['msg'] == '��¼�ɹ�'

    # �޸�֮��ķ���
    @allure.story(next(c_id) + "��¼02")
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/debugApi/addUser.yaml"))
    def test_case01(self,base_info,testcase):
        RequestBase().specification_yaml(base_info,testcase)
