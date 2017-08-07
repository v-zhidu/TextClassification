# !-*- encoding=utf-8 -*-
"""
    package.raven_db.py
    ~~~~~~~~~~~~~~~~~~

    A brief description goes here.

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# engine = create_engine(
#     'mysql://raven_root:lxjsy7E7@U@rm-2zei7ynz0psfg7673o.mysql.rds.aliyuncs.com:3306/raven_intel', echo=False)
engine = create_engine(
    'mysql://root:tribes@121.42.244.187:3382/raven_intel', echo=False)
# engine = create_engine(
#     'mysql://root:ideabinder@10.90.0.10:3306/raven-intel?charset=utf8', echo=False, encoding='utf-8')


# 创建DBSession类型:
DBSession = sessionmaker(bind=engine, autoflush=False)


def get_session():
    return DBSession()


Base.metadata.create_all(engine)
