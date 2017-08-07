# !-*- encoding=utf-8 -*-
"""
    package.store_corpus.py
    ~~~~~~~~~~~~~~~~~~

    持久化语料库

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
import logging

from nltk.corpus import reuters

from model import Document, StopWord
from raven_db import get_session


class StoreCorpus(object):
    """持久化语料库"""

    def __init__(self):
        self._session = get_session()

    def process_reuters(self):
        """处理reuters语料"""
        logging.info('start to process reuters corpus...')
        try:
            # logging.info('process category...')
            # for cat in reuters.categories():
            #     if not self._session.query(Category).filter(
            #             Category.name == cat).first():
            #         new_cat = Category(name=cat)
            #         self._session.add(new_cat)

            logging.info('process text...')
            for doc in reuters.fileids():
                f = reuters.open(doc)
                if not self._session.query(Document).filter(Document.file_name == doc).first():
                    new_doc = Document(title=str(f.readline()),
                                       file_name=doc,
                                       content=f.read().strip().replace("\n", ""), category=reuters.categories(doc)[0], type=1)
                    self._session.add(new_doc)

            # logging.info('process stop words')
            # with open('/Users/duzhiqiang/nltk_data/corpora/stopwords/english', 'r') as f:
            #     for line in f.readlines():
            #         if not self._session.query(StopWord).filter(StopWord.word == line.strip()).first():
            #             new_stop_word = StopWord(word=line.strip())
            #             self._session.add(new_stop_word)

            # with open('/Users/duzhiqiang/nltk_data/corpora/reuters/stopwords', 'r') as f:
            #     for line in f.readlines():
            #         if not self._session.query(StopWord).filter(StopWord.word == line.strip()).first():
            #             new_stop_word = StopWord(word=line.strip())
            #             self._session.add(new_stop_word)

            self._session.commit()
        except Exception as e:
            logging.error(e)
            self._session.rollback()
        finally:
            self._session.close()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    a = StoreCorpus()
    a.process_reuters()
