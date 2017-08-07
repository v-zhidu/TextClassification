#!-*- encoding=utf-8 -*-
from __future__ import unicode_literals
from browser import Browser
from spider_logging import SpiderLogging
from bs4 import BeautifulSoup
import httplib
from raven_db import get_session

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class CrawlTopic(object):
    """
    话题抓取类
    """

    def __init__(self):
        self._browser = Browser()
        self._logger = SpiderLogging(CrawlTopic.__name__).logger

    def find_wiki_html(self, url):
        """获取wiki话题, 只取一个
        """
        response = self._browser.get(url)

        self._logger.debug('解析数据......')
        if response is not None:
            try:
                contents = response.read()
            except httplib.IncompleteRead as e:
                raise e
            return self.find_wiki_category(contents)

    def find_wiki_category(self, html):
        """
        根节点目录的解析方法，在topics页获取所有父级话题以及链接
        """
        self._logger.debug('查找所有根话题...')
        soup = BeautifulSoup(html, 'lxml')

        categories = []
        for tag in soup.find_all('div', class_='mw-normal-catlinks'):
            for string in tag.strings:
                categories.append(string)

        return categories[2]

    def parse_json(self, folder_name):
        import os
        import json
        from model import Document
        session = get_session()
        try:
            for file in os.listdir(folder_name):
                self._logger.info('process: ' + file)
                with open(os.path.join(folder_name, file), 'r') as f:
                    for line in f.readlines():
                        try:
                            if line[0] == '{':
                                d = json.loads(line)
                                # print d['title']
                                new_doc = Document(title=self.convert(d['title']),
                                                   file_name=file,
                                                   content=self.convert(
                                                       d['text']),
                                                   category='', type=3)
                                session.add(new_doc)
                        except Exception as e:
                            self._logger.error(e)
                    session.commit()
        except Exception as e:
            self._logger.error(e)
            session.rollback()
        finally:
            session.close()
            f.close()

    @staticmethod
    def convert(text):
        return text.strip().replace("\n", " ").decode()


if __name__ == '__main__':
    bot = CrawlTopic()
    # text = bot.find_wiki_html('https://zh.wikipedia.org/wiki?curid=118')
    # print text
    bot.parse_json('/Users/duzhiqiang/Code/nlp/wiki_set/AB')
