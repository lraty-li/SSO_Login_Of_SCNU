from AutoSign import Login
from bs4 import BeautifulSoup
import re
import copy
TargetUrl="https://sso.scnu.edu.cn/AccountService/openapi/auth?response_type=code&redirect_url=https%3A%2F%2Fssp.scnu.edu.cn%2FLogBySso.aspx&client_id=79808d49dae212d7dcd12d7e0d25173b"
url="https://ssp.scnu.edu.cn/"
HitCard="https://ssp.scnu.edu.cn/opt_yq_jkdk.aspx?"#fid=55
appurl="https://sso.scnu.edu.cn/AccountService/openapi/onekeyapp.html?app_id=18"
FormData1={
"__EVENTTARGET":"" ,
"__EVENTARGUMENT":"", 
"__VIEWSTATE":"",
"__VIEWSTATEGENERATOR": "",

"__EVENTVALIDATION":"",
}
FormData2={
    "ctl00$cph_right$e_ok": "on",
    "ctl00$cph_right$ok_submit": "开始填报",
}

FormData3={
"ctl00$cph_right$e_location": "广州市白云区",
"ctl00$cph_right$e_health$0": "无不适",
"ctl00$cph_right$e_temp": "36.5",
"ctl00$cph_right$e_travel":"华南师范大学",
"ctl00$cph_right$e_describe": "",
"ctl00$cph_right$e_submit": "提交保存",
}

s=Login(TargetUrl)
print("Login Done,to ssp")

#确认登录

res6=s.get(appurl)
HomePage=BeautifulSoup(res6.content.decode(),'lxml')
TargetKey=HomePage.find(name='a',attrs={"href":re.compile(r'key=')})['href']
#搜到key就自己组装，省点时间
KeyCor=TargetKey.index('key=')
TargetKey=TargetKey[KeyCor:TargetKey.index('&',KeyCor,TargetKey.index('fid'))]
#想尽量不写死，但是真的有必要？写得太烂了吧
HitCard=HitCard+TargetKey+'&fid=55'#反手写死

#获取那坨东西
def GetShit(Page,id):
    kksk=Page.find(name='input',attrs={"id":id})
    if kksk:
        return Page.find(name='input',attrs={"id":id})['value']

res7=s.post(HitCard)
AggrePage=BeautifulSoup(res7.content.decode(),'lxml')

FormData1['__VIEWSTATE']=GetShit(AggrePage,"__VIEWSTATE")
FormData1['__VIEWSTATEGENERATOR']=GetShit(AggrePage,"__VIEWSTATEGENERATOR")
FormData1['__EVENTVALIDATION']=GetShit(AggrePage,"__EVENTVALIDATION")


FormData=copy.copy(FormData1)
#我是傻逼
FormData.update(FormData3)
res8=s.post(HitCard,data=FormData)
DonePage=BeautifulSoup(res8.content.decode(),'lxml')
# 打开打卡界面（提交一次,开始打卡
kksk=DonePage.find(name='span',attrs={"id":"cph_right_e_msg"})
#搜索“打卡成功”
print("如果成功了，会显示东西:",kksk)

