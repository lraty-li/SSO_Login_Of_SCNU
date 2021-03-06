
# !/user/bin/env Python3
# -*- coding:utf-8 -*-
 
"""
file：qq_api.py
create time:2019/4/12 15:14
author:Loong Xu
desc: 调用腾讯OCRapi实现文本识别
"""
app_id=""
app_key=""
import base64, hashlib, json, random, string, time#cv2
from PIL import Image
import sys
from urllib import parse, request
 
 
def GetAccessToken(formdata, app_key):
    '''
    获取签名
    :param formdata:请求参数键值对
    :param app_key:应用秘钥
    :return:返回接口调用签名
    '''
    dic = sorted(formdata.items(), key=lambda d: d[0])
    sign = parse.urlencode(dic) + '&app_key=' + app_key
    #???md5方式不对？
    m = hashlib.md5()
    m.update(sign.encode('utf8'))
    return m.hexdigest().upper()
 
 
def RecogniseGeneral(app_id, time_stamp, nonce_str, image, app_key):
    '''
    腾讯OCR通用接口
    :param app_id:应用标识，正整数
    :param time_stamp:请求时间戳（单位秒），正整数
    :param nonce_str: 随机字符串，非空且长度上限32字节
    :param image:原始图片的base64编码
    :return:
    '''
    host = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr'
    formdata = {'app_id': app_id, 'time_stamp': time_stamp, 'nonce_str': nonce_str, 'image': image}
    app_key = app_key
    sign = GetAccessToken(formdata=formdata, app_key=app_key)
    formdata['sign'] = sign

    flag=True
    while flag :
        req = request.Request(method='POST', url=host, data=parse.urlencode(formdata).encode('utf8'))
        try:
            response = request.urlopen(req)
        except Exception as e:
            print("on response = request.urlopen(req)\n",e)
            time.sleep(2)
            continue
        if (response.status == 200):
            json_str = response.read().decode()
            jobj = json.loads(json_str)
            # if(jobj['ret']!=0):
            #     #处理system busy
            #     time.sleep(2)
            #     continue
            try:
                recognise=jobj['data']['item_list'][0]['itemstring']
            except Exception as e:
                print(jobj['msg'])
                print(e)#如果什么都没识别出来，或者系统繁忙，这里会越界
                time.sleep(2)
                continue
            # datas = jobj['data']['item_list']
            # recognise = {}
            # for obj in datas:
            #     recognise[obj['itemstring']] = obj
            return recognise
 
 
def Recognise(img_path):
    # kksk=Image.open(img_path)
    # kksk.show()
    with open(file=img_path, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
    # nonce = ''.join(random.sample(string.digits + string.ascii_letters, 32))
    nonce="kksk"
    stamp = int(time.time())
    recognise = RecogniseGeneral(app_id=app_id, time_stamp=stamp, nonce_str=nonce, image=base64_data,
                                 app_key=app_key) # 替换成自己的app_id,app_key
    # for k, v in recognise.items():
    #     print(k, v)
    return recognise
 
 
# img_path = r'RandomCode.jpg'
# im = Image.open(img_path)
# recognise_dic = Recognise(img_path)
# for k, value in recognise_dic.items():
#     print(k)
#     for v in value['itemcoord']:
#         cv2.rectangle(im, (v['x'], v['y']), (v['x'] + v['width'], v['y'] + v['height']), (255, 0, 0), 4)
# im.show()
# cv2.imshow('img', im)
# cv2.waitKey(0)