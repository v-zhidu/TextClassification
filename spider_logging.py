# !-*- encoding=utf-8 -*-
"""
日志配置模块

spider_logging.py create by v-zhidu
"""

import logging


class SpiderLogging(object):
    """
    日志配置类

    spider_logging.py create by v-zhidu
    """

    def __init__(self, name):
        self._logger = logging.getLogger(name)
        self.configure_logging()

    @property
    def logger(self):
        """
        返回logger实例
        """
        return self._logger

    def configure_logging(self):
        """
        配置日志的具体方法
        """
        self._logger.setLevel(logging.INFO)
        self.configure_console_handler()
        self.configure_file_handler()

    def configure_console_handler(self):
        """
        配置控制台handler
        """
        # 设置样式
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(process)d %(thread)d - %(levelname)s - %(message)s')

        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # 添加handler
        self._logger.addHandler(console_handler)

    def configure_file_handler(self):
        """
        配置文件handler
        """
        # 设置样式
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(process)d %(thread)d -  %(levelname)s - %(message)s')

        # 控制台handler
        log_folder = './log/'
        logfile = 'spider.log'
        # 检查文件夹是否存在
        import os

        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        file_handler = logging.FileHandler(
            os.path.join(log_folder, logfile), mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # 添加handler
        self._logger.addHandler(file_handler)


if __name__ == '__main__':
    logger = SpiderLogging('test').logger
    logger.info('this is a info messages.')
    logger.debug('this is a info messages.')
