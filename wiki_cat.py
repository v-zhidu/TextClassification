# encoding=utf-8
from __future__ import unicode_literals
from browser import Browser
from spider_logging import SpiderLogging
from bs4 import BeautifulSoup
import httplib
from raven_db import get_session

import sys

reload(sys)
sys.setdefaultencoding('gbk')


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

    def update_wiki_category(self):
        from dao import get_all_doc_by_type_size
        wikis = get_all_doc_by_type_size(3, 100)
        while len(wikis) > 0:
            for wiki in wikis:
                url = wiki[0]
                cat = self.find_wiki_html(url)
                self._logger.info('process wiki: ' + url)
                if cat:
                    self._logger.info('find category: ' + cat)
            wikis = get_all_doc_by_type_size(3, 100)

    def parse_json(self, folder_name):
        import os
        import json
        from model import Document
        session = get_session()
        try:
            count = 0
            for file in os.listdir(folder_name):
                self._logger.info('process: ' + file)
                with open(os.path.join(folder_name, file), 'r') as f:
                    for line in f.readlines():
                        try:
                            if line[0] == '{':
                                d = json.loads(line)
                                self._logger.info('process wiki: ' + d['url'])
                                new_doc = Document(title=self.convert(d['title']),
                                                   file_name=d['url'],
                                                   content=self.convert(
                                                       d['text']),
                                                   category='', type=3)
                                session.add(new_doc)
                                count += 1
                        except Exception as e:
                            self._logger.error(e)
                    session.commit()
                    self._logger.info('process wiki total: ' + str(count))
        except Exception as e:
            self._logger.error(e)
            session.rollback()
        finally:
            session.close()
            f.close()

    @staticmethod
    def convert(text):
        import opencc
        text = opencc.convert(text, config='t2s.json')

        return text.strip().replace("\n", " ").decode('gbk')


if __name__ == '__main__':
    bot = CrawlTopic()
    # text = bot.find_wiki_html('https://zh.wikipedia.org/wiki?curid=118')
    # print text
    # bot.parse_json('/Users/duzhiqiang/Code/nlp/wiki_set/AA')
    # bot.parse_json('/Users/duzhiqiang/Code/nlp/wiki_set/AB')
    bot.update_wiki_category()
