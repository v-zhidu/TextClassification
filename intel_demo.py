# !-*- encoding=utf-8 -*-
"""
    nlp.intel_demo.py
    ~~~~~~~~~~~~~~~~~~

    文本分类器demo

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
import logging
import os

import gensim
from model import DocumentFeature
from dao import add_doc_features

DICTIONARY_SAVE_PATH = 'data/wordids.txt'
TOPIC_SAVE_PATH = 'data/lda'


class DocumentClassifier(object):
    """文本分类demo"""

    def __init__(self):
        from dao import get_all_doc_by_type, get_stop_words
        logging.info('获取训练和测试数据集...')
        self._training_set = get_all_doc_by_type(1)
        self._testing_set = get_all_doc_by_type(2)
        logging.info('训练集文档数量：%d, 测试集文档数量：%d', len(
            self._training_set), len(self._testing_set))
        logging.info('获取停用词列表...')
        self._stoplist = get_stop_words()
        logging.info('停用词数量：%d', len(self._stoplist))
        logging.info('获取字典词列表...')
        if os.path.exists(DICTIONARY_SAVE_PATH):
            self._id2word = self.get_word_mapping_from_file()
        else:
            self._id2word = None
        logging.info('获取上次生成主题模型...')
        if os.path.exists(TOPIC_SAVE_PATH):
            self._ldaModel = gensim.models.ldamodel.LdaModel.load(
                TOPIC_SAVE_PATH, mmap='r')
        else:
            self._ldaModel = None

    def training_topic_model(self, num_topics=100):
        """训练主题模型"""
        docs = [self.pre_process_text(doc.content)
                for doc in self._training_set]

        self._id2word = self.get_word_mapping(docs)
        self.save_word_mapping()
        corpus = self.get_corpus(docs)
        logging.info('训练主题模型...')
        self._ldaModel = gensim.models.ldamodel.LdaModel(
            corpus=corpus, id2word=self._id2word, num_topics=num_topics, update_every=1,
            chunksize=1000, passes=150)

        logging.info('保存主题模型')
        self._ldaModel.save(TOPIC_SAVE_PATH)

    def traning_classifier_model(self, classifierType='NB'):
        """训练分类器模型"""
        from nltk import NaiveBayesClassifier
        import random

        if classifierType == 'NB':
            logging.info('训练朴素贝叶斯分类模型...')
            logging.info('获取训练数据集特征...')
            vectors = self.get_doc_feature(self._training_set).values()
            random.shuffle(vectors)

            return NaiveBayesClassifier.train(vectors)
        else:
            return None

    def evalute_result(self, set_type=1):
        """评估结果"""
        from nltk import classify

        if set_type == 2:
            test_set = self._testing_set
        else:
            test_set = self._training_set

        classifier = self.traning_classifier_model()
        logging.info('获取测试数据集特征...')
        features = self.get_doc_feature(test_set)

        self.save_doc_feature(features, set_type)

        logging.info('获取分类结果...')
        logging.info('测试数据集准确：%4.2f', classify.accuracy(
            classifier, features.values()))

    def prediction(self, doc_set=None):
        """预测结果"""
        if doc_set is None:
            doc_set = self._testing_set
        else:
            doc_set = self._training_set

        classifier = self.traning_classifier_model()
        logging.info('获取待预测数据集特征...')
        vectors = self.get_doc_feature(doc_set)

        logging.info('获取分类结果...')
        for id, vec in vectors.iteritems():
            cat = classifier.classify(vec[0])
            logging.info('%d %s %s',
                         id, cat, vec[1])

    def get_doc_feature(self, documents):
        """获取文本特征"""
        docs = {}
        for doc in documents:
            tokens = self.pre_process_text(doc.content)
            bow = self.doc2bow(tokens)
            vec = {}
            for topic_id, value in self._ldaModel.get_document_topics(bow, minimum_probability=-0.3):
                vec[str(topic_id)] = value
            # for cat in doc.category.split(','):
            #     docs.append((vec, cat))
            docs[doc.id] = (vec, doc.category)

        logging.info('获取到 %d 特征', len(docs))
        return docs

    def save_doc_feature(self, features, set_type):
        """保存文本特征值"""
        doc_features = []
        for doc_id, feature in features.iteritems():
            values = []
            for k, v in feature[0].iteritems():
                k_v = str(k) + ':' + str(v)
                values.append(k_v)

            entity = DocumentFeature(doc_id=doc_id, category=feature[1],
                                     features=','.join(values), type=set_type)
            doc_features.append(entity)
        add_doc_features(doc_features, set_type)

    def doc2bow(self, tokens):
        """生成词袋"""
        return self._id2word.doc2bow(tokens)

    def get_corpus(self, documents):
        """生成语料库"""
        return [self._id2word.doc2bow(doc) for doc in documents]

    def get_word_mapping(self, documents):
        """获取词典"""
        return gensim.corpora.Dictionary(documents)

    def get_word_mapping_from_file(self):
        """获取词典"""
        return gensim.corpora.Dictionary.load_from_text(DICTIONARY_SAVE_PATH)

    def update_word_mapping(self, documents):
        """更新词典"""
        if not isinstance(documents, list):
            raise TypeError(
                'The input of update_word_mapping must be type of list.')
        self._id2word.add_documents(documents)

    def save_word_mapping(self):
        """保存辞典"""
        self._id2word.save_as_text(DICTIONARY_SAVE_PATH, sort_by_word=True)

    def pre_process_text(self, raw):
        """文本预处理方法"""
        words = self._split_words_en(raw)
        words = self._remove_stop_words(words)
        # words = self._remove_once_words(words)
        # print len(words)

        return words

    def _remove_stop_words(self, words):
        """去除停用词"""
        if not isinstance(words, list):
            raise TypeError('The input of stop_words must be type of str.')

        return [word for word in words if word not in self._stoplist]

    def _remove_once_words(self, words):
        """去除只出现一次的词"""
        from collections import defaultdict
        frequency = defaultdict(int)

        for word in words:
            for token in word:
                frequency[token] += 1

        return [token for token in words if frequency[token] > 1]

    def _split_words_en(self, raw):
        """英文分词方法"""
        if not isinstance(raw, str):
            raise TypeError('The input of split_words_en must be type of str.')

        from nltk import word_tokenize
        return word_tokenize(raw)


def convertVectorToJson(feature):

    features = feature.split(',')
    dic = {}
    for item in features:
        a = item.split(':')
        id = 'features' + '_' + str(int(a[0]) - 1)
        value = float(a[1])
        dic[id] = {'dataType': 40, 'dataValue': value}

    import json
    result = {"inputs": [dic]}
    print json.dumps(result).strip()


if __name__ == '__main__':
    a = DocumentClassifier()
    # # a.training_topic_model(num_topics=50)
    a.evalute_result(set_type=2)
    # a.prediction()

    # a = '42:7.93650793651e-05,48:7.93650793651e-05,43:0.00809938578164,49:0.0124282454026,24:7.93650793651e-05,25:7.93650793651e-05,26:7.93650793651e-05,27:7.93650793651e-05,20:7.93650793651e-05,21:7.93650793651e-05,22:0.00953697239086,23:7.93650793651e-05,46:7.93650793651e-05,47:0.0335312876747,44:0.00454713235275,45:0.0240246888284,28:7.93650793651e-05,29:0.168734592184,40:0.0563747496378,41:0.078978547499,1:0.015220388411,0:0.0302963330859,3:0.0306456208837,2:0.00409057905185,5:0.0365942838451,4:7.93650793651e-05,7:7.93650793651e-05,6:0.33103409675,9:7.93650793651e-05,8:7.93650793651e-05,39:7.93650793651e-05,38:7.93650793651e-05,11:7.93650793651e-05,10:0.00489242537909,13:0.00772858156081,12:0.0142484811895,15:0.00404761904762,14:7.93650793651e-05,17:0.00414897647495,16:0.0350995952486,19:7.93650793651e-05,18:7.93650793651e-05,31:7.93650793651e-05,30:7.93650793651e-05,37:7.93650793651e-05,36:7.93650793651e-05,35:7.93650793651e-05,34:0.0834751950978,33:7.93650793651e-05,32:7.93650793651e-05'

    # convertVectorToJson(a)
