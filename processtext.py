# !-*- encoding=utf-8 -*-
import jieba


def split_word(text):
    return ' '.join(jieba.cut(text, cut_all=False))


def remove_stop_words(stoplist, words):
    """去除停用词"""
    if not isinstance(words, list):
        raise TypeError('The input of stop_words must be type of str.')

    return [word for word in words if word not in stoplist]


def get_key_word(text, stop_word_file=None):
    import jieba.analyse
    if not stop_word_file:
        jieba.analyse.set_stop_words(stop_word_file)

    tags = jieba.analyse.extract_tags(text, topK=30)
    return ' '.join(tags)


if __name__ == '__main__':
    print get_key_word('我来到北京清华大学', 'stopword.txt')
