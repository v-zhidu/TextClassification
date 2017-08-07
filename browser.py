# !-*- encoding=utf-8 -*-
'''
处理和网络相关的操作模块

browser.py create by v-zhidu
'''

from __future__ import unicode_literals

import socket
import time
import urllib
import urllib2

from spider_logging import SpiderLogging


class Browser(object):
    """
    Summary of class here.

    Longer class information....

    Public Attributes
         An integer count of the eggs we have laid.
    """

    def __init__(self, timeout=10):
        self._headers = {
            'Host': 'www.zhihu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN, zh; q=0.8, en; q=0.6'
        }
        self._logger = SpiderLogging(Browser.__name__).logger

        # 设置代理
        proxy = urllib2.ProxyHandler({'http': '119.57.117.41:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

        # 设置全局超时
        socket.setdefaulttimeout(timeout)

        import httplib
        httplib.HTTPConnection._http_vsn = 10
        httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    @property
    def header(self):
        '''Summary of method here.

        Logger method information

        Args:
             An integer list.
        Returns:
             The sum of an integer list.
        Raises:
             The input args must be int type.
        '''
        return self._headers

    def get(self, url, delay=0):
        """Get方式打开链接

        通过Get方式打开链接，无登陆验证

        Args:
            url: str类型字符串，指向需要获取的链接地址
        Returns:
            返回html页面数据
        Raises:
            TypeError:
            HttpError:
        """
        try:
            if delay:
                time.sleep(delay)

            self._logger.debug('请求地址 %s', url)
            response = urllib2.urlopen(url, data=None)

            return response
        except urllib2.HTTPError as e:
            self._logger.error(
                'HTTPERROR - code=%s, msg=%s, url=%s', e.code, e.message, url)
        except urllib2.URLError as e:
            self._logger.error(
                'URLError - message=%s url=%s', e.reason, url)

    def topic_list(self, url, topic_id, off_set=0, delay=0):
        """Summary of method here.

        Logger method information

        Args:
             An integer list.
        Returns:
             The sum of an integer list.
        Raises:
             The input args must be int type.
        """
        try:
            if delay:
                time.sleep(delay)

            self._headers['content-type'] = 'application/x-www-form-urlencoded charset=UTF-8'

            data = {'method': 'next'}
            data['params'] = '{"topic_id":%s,"offset":%s,"hash_id":""}' % (
                topic_id, off_set)

            data = urllib.urlencode(data)
            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)

            return response
        except urllib2.HTTPError as e:
            self._logger.error(
                'HTTPERROR - code=%s, msg=%s, url=%s', e.code, e.message, url)
        except urllib2.URLError as e:
            self._logger.error(
                'URLError - message=%s url=%s', e.reason, url)


if __name__ == '__main__':
    pass
