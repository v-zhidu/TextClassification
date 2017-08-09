# !-*- encoding=utf-8 -*-
"""
    nlp.dao.py
    ~~~~~~~~~~~~~~~~~~

    数据库操作方法

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
import logging

from model import StopWord, Document, DocumentFeature
from raven_db import get_session

session = get_session()


def get_stop_words():
    """获取停用题列表"""
    return [x.word for x in session.query(StopWord.word).all()]


def get_all_doc_by_type(doc_type):
    """获取所有文档"""
    return session.query(Document.id, Document.content, Document.category).filter(Document.type == doc_type).all()


def get_all_doc_by_type_size(doc_type, limit=100):
    """获取所有文档"""
    return session.query(Document.file_name).filter(Document.type == doc_type and Document.category == ' ').limit(limit).all()


def add_doc_features(features, set_type):
    """保存文档特征数据"""
    if len(features) > 0:
        try:
            trunate_doc_feature(set_type)
            session.add_all(features)
            session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()
        finally:
            session.close()


def trunate_doc_feature(set_type):
    try:
        session.query(DocumentFeature).filter(
            DocumentFeature.type == set_type).delete()
        session.commit()
    except Exception as e:
        logging.error(e)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    wiki = get_all_doc_by_type_size(3, 10)
    print wiki[0][0]
