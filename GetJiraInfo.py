import datetime
import http
import smtplib
import time
import urllib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pyquery import PyQuery as pq


def GetDetailCode(urls):
    headers = {
        "Host": "jira.xxx.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    }
    values = {
        "os_username": "输入用户名",
        "os_password": "输入密码"
    }
    login_url = "http://jira.xxx.com/login.jsp"
    data = urllib.parse.urlencode(values).encode('utf-8')
    # 声明一个CookieJar对象实例来保存cookie
    cookie = http.cookiejar.CookieJar()
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib.request.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib.request.build_opener(handler)
    requestLogin = urllib.request.Request(login_url, data, headers)
    responseLogin = opener.open(requestLogin)
    url = urls
    response = opener.open(url)
    pagecode = response.read().decode("utf-8")
    return pagecode


def GetDetailUrl(html):
    doc = pq(html)
    vlunResult = doc('td.issuekey > a').text().split(' ')
    # print(items.group(1))
    #每个漏洞的url
    for x in vlunResult:
        urls = 'http://jira.xxx.com/browse/' + x
        GetDetailInfo(urls)

#获取详情页面信息
def GetDetailInfo(vlun_url):
    # 解析漏洞详情页面
    detailUrl = GetDetailCode(vlun_url)
    doc = pq(detailUrl)
    # 漏洞名称
    title = doc('#summary-val').text()
    # 提交时间
    subTime = doc('#created-val').text()
    # 开发负责人
    author = doc('#assignee-val').text()
    # 修复状态
    type = doc('#status-val > span').text()
    # 漏洞等级
    bugLevel = doc('#priority-val').text()
    if bugLevel == 'P0' or bugLevel == 'P1':
        bugLevel = '高危'
    elif bugLevel == 'P2':
        bugLevel = '中危'
    elif bugLevel == 'P3':
        bugLevel = '低危'
    elif bugLevel == 'P3':
        bugLevel = '忽略'
    detail = '漏洞名称：'+ title + '\n' + '漏洞地址：' + vlun_url + '\n'+ '漏洞等级：' + bugLevel + '\n'+'提交时间：' + subTime + '\n' + '开发负责人：' + author + '\n' + '修复状态：' + type + '\n' + '==========================================='
    print(detail)
    success(detail)
    send_email_with_pic(detail)

def nextPage(page):

    url = "http://jira.xxxx.com/issues/?nql=text%20~%20%22%E5%AE%89%E5%85%A8%E6%BC%8F%E6%B4%9E%22&Index=" + str(page)
    html = GetDetailCode(url)
    GetDetailUrl(html)

#输出文件
def success(info):
    result_name = str(datetime.datetime.now().month) + '月漏洞.txt'
    with open(result_name, 'a+')as a:
        a.write(info + '\n')

def send_email_with_pic(mail_msg):
    timeNow = str(time.strftime("%Y-%m-%d", time.localtime()))
    sender = '' # 发件人
    password = '' # 发件人密码
    receiver = '' # 收件人
    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['To'] = receiver
    subject = 'XXX安全漏洞提示预警'
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(mail_msg, 'plain', 'utf-8'))

    try:
        smtpObj = smtplib.SMTP('smtp.qq.com')
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        # print('邮件发送成功')
    except smtplib.SMTPException:
        print('Error: 无法发送邮件')

if __name__ == '__main__':
    nextPage(0)
    # range()代表页数，需修改
    for i in range(2):
        i = 1*50
        nextPage(i)





