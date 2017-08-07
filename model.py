# !-*- encoding=utf-8 -*-
"""
    package.model.py
    ~~~~~~~~~~~~~~~~~~

    ORM 实体

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
import time
from sqlalchemy import (Column, DateTime, Integer, MetaData,
                        SmallInteger, String, Table, Text, create_engine, func)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = 't_doc'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    file_name = Column(String(256), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(256))
    type = Column(SmallInteger, nullable=False)
    ctime = Column(DateTime, default=func.now(), nullable=False)


class DocumentFeature(Base):
    __tablename__ = 't_doc_feature'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, nullable=False)
    category = Column(String(256), nullable=False)
    features = Column(Text)
    type = Column(SmallInteger, nullable=False)


class StopWord(Base):
    __tablename__ = 't_stop_word_cn'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(64), unique=True)
