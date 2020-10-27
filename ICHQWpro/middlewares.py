import requests
import base64
from collections import defaultdict
import random
from twisted.internet import defer
from twisted.internet.error import TimeoutError, ConnectionRefusedError, \
    ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone
from ICHQWpro.get_cookies import get_cookies_dict


class CookieMiddleware:

	def process_request(self, request, spider):
		request.cookies = get_cookies_dict()
		return None


# 随机UA
class RandomUserAgent(object):

	def process_request(self, request, spider):
		ua = random.choice(self.get_UA_list)
		request.headers['User-Agent'] = ua

	@property
	def get_UA_list(self):
		return [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


# 随机IP
class RandomProxy(object):
    EXCEPTIONS_TO_CHANGE = (
        defer.TimeoutError, TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError,
        ConnectionDone)

    def __init__(self):
        self.ip_list = self.get_ip_list()
        self.stats = defaultdict(int)  # 默认值是0    统计次数
        self.max_failed = 1  # 请求最多不超过3次
        print(self.ip_list)

    def get_ip_list(self):
        '''
        ip 池接口
        :return:
        '''
        url = 'http://api.wandoudl.com/api/ip?app_key=fffbcf689ef5ecafaf6607f713f70ed9&pack=216497&num=20&xy=2&type=2&lb=\r\n&mr=1&'
        resp = requests.get(url)
        resp_dict = resp.json()
        ip_dict_list = resp_dict.get("data")
        list_ip = []
        if ip_dict_list != None:
            for ip_dict in ip_dict_list:
                ip_port = '{ip}:{port}'.format(ip=ip_dict.get('ip'), port=str(ip_dict.get('port')))
                list_ip.append(ip_port)
        return list_ip

    def base_code(self, username, password):
        str = '%s:%s' % (username, password)
        encodestr = base64.b64encode(str.encode('utf-8'))
        return '%s' % encodestr.decode()

    def process_request(self, request, spider):
        if len(self.ip_list) == 0:
            print('代理ip以用完,重新获取代理ip......')
            self.ip_list = self.get_ip_list()
        request.headers['Proxy-Authorization'] = 'Basic %s' % (self.base_code('15616122577@163.com', 'Zhang0612'))
        http = request.url.split('//')[0]
        request.meta['proxy'] = http + "//"+random.choice(self.ip_list)
        return None

    def process_response(self, request, response, spider):
        # 第五步： 请求成功
        cur_proxy = request.meta.get('proxy')
        # 判断是否被对方禁封
        if response.status != 200:
            # 给相应的ip失败次数 +1
            self.stats[cur_proxy] += 1
            print("当前ip{}，第{}次出现错误状态码".format(cur_proxy, self.stats[cur_proxy]))
            # 删除这次ip
            self.remove_proxy(cur_proxy)
            del request.meta['proxy']
            # 重新下载这个请求
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        return response

    def remove_proxy(self, proxy):
        proxy = proxy.split('//')[-1]
        if proxy in self.ip_list:
            self.ip_list.remove(proxy)
            print("从代理列表中删除{}".format(proxy))

    def process_exception(self, request, exception, spider):
        print('进入process_exception')
        # 第五步：请求失败
        cur_proxy = request.meta.get('proxy')  # 取出当前代理
        # 如果本次请求使用了代理，并且网络请求报错，认为这个ip出了问题
        if cur_proxy and isinstance(exception, self.EXCEPTIONS_TO_CHANGE):
            print("当前的{}和当前的{}".format(exception, cur_proxy))
            self.remove_proxy(cur_proxy)
            del request.meta['proxy']
            # 重新下载这个请求
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
