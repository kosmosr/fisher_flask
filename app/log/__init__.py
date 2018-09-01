# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/8/5 21:32
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_formater = logging.Formatter(
    ":%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formater)

file_path = os.path.join(os.getcwd(), 'app', 'log')
file_path = os.path.join(file_path, 'app.log')
file_handler = TimedRotatingFileHandler(file_path, when='D')
file_handler.setLevel(logging.DEBUG)
file_handler.suffix = "%Y-%m-%d"
file_handler.setFormatter(console_formater)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
