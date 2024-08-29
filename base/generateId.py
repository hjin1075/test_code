def generate_module_id():
    """
    ���ɲ���ģ���ţ�Ϊ�˱�֤allure�����˳����pytest�趨��ִ��˳�򱣳�һ��
    :return:
    """
    for i in range(1,1000):
        module_id = 'M' + str(i).zfill(2) + '_'
        yield module_id

def generate_testcase_id():
    """
    ���ɲ��������ı��
    :return:
    """
    for i in range(1,1000):
        case_id = 'C' + str(i).zfill(2) + '_'
        yield case_id

m_id = generate_module_id()
c_id = generate_testcase_id()