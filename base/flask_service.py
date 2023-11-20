# -*- coding: utf-8 -*-
import datetime
import string
import time
from hashlib import sha1
from faker import Faker
from conf.setting import DIR_BASE

import flask
import json
import random
from flask import jsonify, make_response, request
from functools import wraps

"""
mock接口服务
"""

# __name__表示当前的python文件名，把该文件当做一个服务
api = flask.Flask(__name__)

api.config.from_object(__name__)
# 定义Flask app时，指定JSON_AS_ASCII的参数设置为False，阻止jsonify将json内容转为ASCII进行返回
api.config['JSON_AS_ASCII'] = False

global_params = {}
faker = Faker()


def read_data(file_path):
    with open(file_path, 'r', encoding='GBK') as f:
        data = f.read()
        return data


def write_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)


def timestamp():
    """获取当前时间戳，10位"""
    t = int(time.time())
    return t


def now_date():
    """获取当前时间标准时间格式"""
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now_time


def timestamp_thirteen():
    """获取当前的时间戳，13位"""
    t = int(time.time()) * 1000
    return t


@api.route('/index', methods=['get'])
def index():
    res = {'msg': '成功访问首页', 'msg_code': 200}
    return json.dumps(res, ensure_ascii=False)


def sha1_encryption(params):
    """参数sha1加密"""
    enc_data = sha1()
    # 获取待输出数据
    enc_data.update(params.encode(encoding="utf-8"))
    return enc_data.hexdigest()


# 设置post表单提交请求头装饰器
def set_headers(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        resp = make_response(func(*args, **kwargs))
        resp.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
        return resp

    return decorated_function


@api.route('/login', methods=['get'])
def set_cookie():
    """设置cookie"""
    resp = make_response("")
    randoms = ''.join([random.choice(string.hexdigits) for i in range(20)])
    cookie_value = sha1_encryption(randoms)
    resp.set_cookie('Cookie', cookie_value, max_age=60 * 60 * 24)
    return resp


@set_headers
@api.route('/dar/user/login', methods=['post'])
def user_login():
    """
    登录接口
    post提交，from-data表单提交方式（key-value），使用flask.request.values.get获取传参
    :return:
    """
    user_info = {
        'user_name': 'test01',
        'passwd': 'admin123'
    }

    user_name = flask.request.form.get('user_name')
    passwd = flask.request.form.get('passwd')
    token = ''.join([random.choice(string.digits) for i in range(19)])
    global_params['token'] = token
    if all([user_name, passwd]):

        if all([user_name == user_info['user_name'], passwd == user_info['passwd']]):
            return jsonify({'msg': '登录成功', 'msg_code': 200, 'error_code': None, 'token': token})
        else:
            return jsonify({'msg': '登录失败,用户名或密码错误', 'msg_code': 9001, 'token': None})
    else:
        res = {'msg': '参数错误', 'msg_code': -1}
    # return json.dumps(res, ensure_ascii=False)
    return jsonify({
        'msg': '参数错误',
        'msg_code': -1
    })


@api.route('/dar/user/addUser', methods=['post'])
def add_user():
    """新增用户接口"""
    add_user_info = {
        'username': 'testadduser',
        'password': 'tset6789890',
        'role_id': '123456789',
        'dates': '2023-12-31',
        'phone': '13800000000',
        'token': global_params['token']
    }
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    role_id = flask.request.form.get('role_id')
    dates = flask.request.form.get('dates')
    phone = flask.request.form.get('phone')
    token = flask.request.form.get('token')
    if username == add_user_info['username'] and password == add_user_info['password'] and role_id == add_user_info[
        'role_id'] and dates == add_user_info['dates'] and phone == add_user_info['phone'] \
            and token == add_user_info['token']:
        return jsonify({'msg': '新增成功', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '新增失败', 'msg_code': 9001})


@api.route('/dar/user/deleteUser', methods=['post'])
def delete_user():
    """删除用户接口"""
    user_id_lst = ['123839387391912', '13679000932223434', '89588181111112343', '331111456562131', '112576886322112',
                   '213457889904300192']
    user_id = flask.request.form.get('user_id')

    if user_id in user_id_lst:
        return jsonify({'msg': '删除成功!', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '删除失败，用户id不存在!', 'msg_code': 9001})


@api.route('/dar/user/updateUser', methods=['post'])
def update_user():
    """修改用户接口"""
    update_user_info = {
        'username': 'testadduser',
        'password': 'tset6789#$123',
        'role_id': '89588181111112343',
        'dates': '2023-12-31',
        'phone': '13800000000'
    }
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    role_id = flask.request.form.get('role_id')
    dates = flask.request.form.get('dates')
    phone = flask.request.form.get('phone')
    if username == update_user_info['username'] and password == update_user_info['password'] and role_id == \
            update_user_info[
                'role_id'] and dates == update_user_info['dates'] and phone == update_user_info['phone']:
        return jsonify({'msg': '更新成功', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '更新失败', 'msg_code': 9001})


@api.route('/dar/user/queryUser', methods=['post'])
def query_user():
    """查询用户接口"""
    query_id_lst = ['123839387391912', '13679000932223434', '89588181111112343', '331111456562131', '112576886322112',
                    '213457889904300192']
    user_id = flask.request.form.get('user_id')

    if user_id in query_id_lst:
        return jsonify({'msg': '查询成功!', 'msg_code': 200, 'error_code': None})
    else:
        return jsonify({'msg': '查询失败，用户id不存在!', 'msg_code': 9001})


@api.route('/dar/user/queryUser', methods=['get'])
def login():
    """
    get提交，url传参，使用flask.request.args.get获取传参
    :return:
    """
    user_id = flask.request.args.get('user_id')
    if user_id:
        if user_id == '123456':
            return jsonify({'user_id': '123456', 'msg_code': 200, 'msg': '查询成功'})
        else:
            return jsonify({'msg_code': -1, 'msg': '用户ID错误'})
    else:
        return jsonify({'msg': '参数错误', 'msg_code': -1})


@api.route('/dar/user/addRole', methods=['post'])
def login_3():
    """
    post提交，json格式传参方式
    :return:
    """
    role_name = flask.request.json.get('role_name')
    organization_id = flask.request.json.get('organization_id')
    if all([role_name, organization_id]):
        if role_name == 'test' and organization_id == '123':
            res = {'msg': '添加成功', 'msg_code': 200}
        else:
            res = {'msg': '添加失败', 'msg_code': -1}
    else:
        res = {'msg': '参数错误', 'msg_code': 1001}
    return jsonify(res)


ids_lst = []

for j in range(5):
    phone = ''.join([random.choice(string.digits) for i in range(11)])
    ids_lst.append(phone)

good_id_list = ['18382788819', '33809635011', '56996760797', '82193785267', '74190550836']
cart_id_list = ['18382788819', '33809635011', '56996760797', '82193785267', '74190550836']
user_id = ''.join([random.choice(string.digits) for i in range(19)])

pro_info = {
    'goodsList': [{
        'goodsId': '18382788819',
        'goods_name': '【2件套】套装秋冬新款仿獭兔毛钉珠皮草毛毛短外套加厚大衣女装',
        'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/bcf848aa71c6389607ae7a84b70f1543.jpeg',
        'unit_price': '￥99.00',
        'original_price': '',
        'goods_count': '233'
    },
        {
            'goodsId': '33809635011',
            'goods_name': '好奇小森林心钻装纸尿裤M22拉拉裤L18/XL14超薄透气裤型尿不湿 1件装',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/176019babfdecffa1d9f98f40b7e99b4.jpeg',
            'unit_price': '￥108.00',
            'original_price': '',
            'goods_count': '521'
        },
        {
            'goodsId': '56996760797',
            'goods_name': '冻干鸡小胸整块增肥营养发腮狗狗零食新手养猫零食幼猫零食100g',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg',
            'unit_price': '￥17.80',
            'original_price': '',
            'goods_count': '1181'
        },
        {
            'goodsId': '82193785267',
            'goods_name': '【自营】ISB伊珊娜意大利水果系列宠物犬猫沐浴露除臭香波护毛素',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg',
            'unit_price': '￥650.00',
            'original_price': '',
            'goods_count': '3000+'
        },
        {
            'goodsId': '74190550836',
            'goods_name': '【新品零0CM嵌入式】海尔电冰箱410L家用法式四门多门官方正品',
            'goods_image': 'https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg',
            'unit_price': '￥5746.00',
            'original_price': '',
            'goods_count': '1000+'
        }
    ],
    'secache': 'c98b29872e8a4b28859db207944ba817',
    'secache_time': timestamp_thirteen(),
    'secache_date': now_date(),
    'reason': '',
    'error_code': '0000',
    'cache': 0,
    'api_info': 'today:21 max:10000 all[90=21+33+36];expires:2030-12-31',
    'translate_language': 'zh-CN',
    'request_id': 'request_id'
}


@api.route('/coupApply/cms/goodsList', methods=['get'])
def product_list():
    """获取商品列表接口"""

    pro_type = request.args.get('msgType')
    if pro_type:
        if pro_type == 'getHandsetListOfCust':
            return jsonify(pro_info)
        else:
            return jsonify({'secache': 'c98b29872e8a4b28859db207944ba817',
                            'secache_time': timestamp_thirteen(),
                            'secache_date': now_date(),
                            'error_code': '4000',
                            'translate_language': 'zh-CN',
                            'goodsList': []})
    else:
        return jsonify({'msg': '参数错误', 'error_code': '9001'})


@api.route('/coupApply/cms/productDetail', methods=['post'])
def product_detail():
    """商品详情接口"""
    data = read_data(DIR_BASE + '/data/mockdata/productDetail.json')
    response = json.loads(data)
    response['secache_date'] = now_date()
    response['goodsId'] = random.choice(['18382788819', '33809635011', '56996760797', '82193785267', '74190550836'])
    pro_id = request.json.get('pro_id')
    page = request.json.get('page')
    size = request.json.get('size')
    if pro_id in ['18382788819', '33809635011', '56996760797', '82193785267', '74190550836']:
        return jsonify(response)
    else:
        return jsonify(
            {'error': '不存在该商品', 'goodsId': '', 'error_code': '4000', 'translate_language': 'zh-CN', 'item': {},
             'secache_date': now_date()})


@api.route('/coupApply/cms/shoppingJoinCart', methods=['post'])
def add_cart():
    """商品加入购物车"""
    goods_id = request.json.get('goods_id')
    count = request.json.get('count')
    price = request.json.get('price')
    if all([goods_id, count, price]):
        if goods_id in good_id_list:
            response = {
                "createTime": now_date(),
                "error": "",
                "error_code": "0000",
                "message": "success",
                "translate_language": "zh-CN",
                "userId": user_id,
                "cartList": [{
                    "cid": random.sample(range(0, 1000), 1)[0],
                    "productId": "18382788819",
                    "price": "99.00",
                    "totalPrice": "239.00",
                    "productName": "【2件套】套装秋冬新款仿獭兔毛钉珠皮草毛毛短外套加厚大衣女装",
                    "productImage": "https://omsproductionimg.yangkeduo.com/images/2017-12-12/bcf848aa71c6389607ae7a84b70f1543.jpeg"
                }, {
                    "cid": random.sample(range(0, 1000), 1)[0],
                    "productId": "33809635011",
                    "price": "108.00",
                    "totalPrice": "347.00",
                    "productName": "好奇小森林心钻装纸尿裤M22拉拉裤L18/XL14超薄透气裤型尿不湿 1件装",
                    "productImage": "https://omsproductionimg.yangkeduo.com/images/2017-12-12/bcf848aa71c6389607ae7a84b70f1543.jpeg"
                }, {
                    "cid": random.sample(range(0, 1000), 1)[0],
                    "productId": "56996760797",
                    "price": "17.80",
                    "totalPrice": "364.80",
                    "productName": "冻干鸡小胸整块增肥营养发腮狗狗零食新手养猫零食幼猫零食100g",
                    "productImage": "https://omsproductionimg.yangkeduo.com/images/2017-12-12/efb5db42397550bffd3211ca6f197498.jpeg"
                }
                ]
            }
            return jsonify(response)
        else:
            return jsonify({
                "createTime": now_date(),
                "error": "商品id不存在",
                "error_code": "4000",
                "message": "",
                "translate_language": "zh-CN",
                "cartList": []
            })
    else:
        return jsonify({'error': '参数错误或缺少必填参数', 'error_code': '9001'})


@api.route('/coupApply/cms/delCart', methods=['post'])
def delete_cart():
    """删除购物车商品"""
    product_id = request.form.get('productId')
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'error': '请求参数类型错误', 'error_code': '7001'})
    elif request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        if product_id:
            if product_id in cart_id_list:
                response = {
                    "createTime": now_date(),
                    "error": "",
                    "error_code": "0000",
                    "message": "success",
                    "translate_language": "zh-CN",
                }
                return jsonify(response)
            else:
                return jsonify({
                    "createTime": now_date(),
                    "error": "购物车id不存在",
                    "error_code": "4000",
                    "message": "",
                    "translate_language": "zh-CN"
                })
        else:
            return jsonify({'error': '参数错误或缺少必填参数', 'error_code': '9001'})


@api.route('/coupApply/cms/placeAnOrder', methods=['post'])
def place_an_order():
    """商品下单接口--提交订单"""
    place_info = {
        "goods_id": '33809635011',
        "number": 3,
        "propertyChildIds": "2:9",
        "inviter_id": 127839112,
        "price": '239.00',
        'freight_insurance': '0.00',
        'discount_code': '002399',
        'consignee_info': {
            'name': '张三',
            'phone': 13800000000,
            'address': '北京市海淀区西三环北路74号院4栋3单元1008'
        }
    }
    goods_id = request.json.get('goods_id')
    number = request.json.get('number')
    propertyChildIds = request.json.get('propertyChildIds')
    inviter_id = request.json.get('inviter_id')
    price = request.json.get('price')
    freight_insurance = request.json.get('freight_insurance')
    discount_code = request.json.get('discount_code')
    consignee_info = request.json.get('consignee_info')
    if all([goods_id, number, propertyChildIds, inviter_id, price, freight_insurance, discount_code, consignee_info]):
        if goods_id in good_id_list:
            order_num = ''.join([random.choice(string.digits) for i in range(21)])

            write_data(DIR_BASE + '/data/mockdata/orderNumber.json', json.dumps({'order_num': order_num,
                                                                                 'user_id': user_id}))
            response = {
                'orderNumber': order_num,
                'userId': user_id,
                'crateTime': now_date(),
                'error': '',
                'error_code': '0000',
                'translate_language': 'zh-CN',
                'message': '提交订单成功'
            }
            return jsonify(response)
        else:
            return jsonify({'error': '商品id不存在', 'error_code': '4000'})

    else:
        return jsonify({'error': '参数错误或必填参数为空', 'error_code': '9001'})


@api.route('/coupApply/cms/shoppingInventory', methods=['post'])
def check_shopping_inventory():
    """校验商品库存"""
    goods_id = request.json.get('goodsId')
    count = request.json.get('count')
    time_stamp = request.json.get('timeStamp')
    if all([goods_id, count]):
        if goods_id in good_id_list:
            if int(count) < 5:
                response = {
                    'createTime': now_date(),
                    'error': '',
                    'error_code': '0000',
                    'translate_language': 'zh-CN',
                    'status': '0'
                }
                return jsonify(response)
            else:
                return jsonify({
                    'createTime': now_date(),
                    'error': '商品库存不足',
                    'error_code': '0000',
                    'translate_language': 'zh-CN',
                    'status': '1'
                })
        else:
            return jsonify({'error': '商品id不存在', 'error_code': '4000'})
    else:
        return jsonify({'msg': '参数错误', 'error_code': '9001'})


@api.route('/coupApply/cms/orderPay', methods=['post'])
def order_pay():
    """订单支付"""
    data = read_data(DIR_BASE + '/data/mockdata/orderNumber.json')
    order_num_json = json.loads(data).get('order_num')
    user_id_json = json.loads(data).get('user_id')
    order_num = request.json.get('orderNumber')
    user_id = request.json.get('userId')
    time_stamp = request.json.get('timeStamp')
    if all([order_num, user_id]):
        if order_num == order_num_json and user_id == user_id_json:
            response = {
                'createTime': now_date(),
                'error': '',
                'error_code': '0000',
                'translate_language': 'zh-CN',
                'message': '订单支付成功'
            }
            return jsonify(response)
        else:
            return jsonify({'error': '订单编号或用户id不存在', 'error_code': '4000'})
    else:
        return jsonify({'msg': '参数错误', 'error_code': '9001'})


@api.route('/coupApply/cms/checkOrderStatus', methods=['post'])
def check_order_status():
    """校验商品订单状态"""
    data = eval(read_data(DIR_BASE + '/data/mockdata/orderNumber.json'))
    order_num = data.get('order_num')
    order_number = request.json.get('orderNumber')
    if order_number == order_num:
        response = {
            'status': '0',
            'queryTime': now_date(),
            'error': '',
            'error_code': '',
            'translate_language': 'zh-CN'
        }
        return jsonify(response)
    else:
        return jsonify({'error': '订单编号不存在', 'error_code': '4000'})


@api.route('/coupApply/cms/checkLogisticsStatus', methods=['post'])
def check_logistics_status():
    """校验商品物流状态"""
    data = eval(read_data(DIR_BASE + '/data/mockdata/orderNumber.json'))
    order_num = data.get('order_num')
    order_number = request.json.get('orderNumber')
    if order_number == order_num:
        response = {
            'status': '1',
            'queryTime': now_date(),
            'error': '',
            'error_code': '',
            'translate_language': 'zh-CN'
        }
        return jsonify(response)
    else:
        return jsonify({'error': '订单编号不存在', 'error_code': '4000'})


if __name__ == '__main__':
    # debug=True，改代码后不用重启，会自动重启
    api.run(host='127.0.0.1', port=8787, debug=True)
    # res = read_data(DIR_BASE + '/data/mockdata/orderNumber.json')
    # res = eval(res)
    # print(res)
