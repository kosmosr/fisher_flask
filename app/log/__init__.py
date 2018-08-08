# encoding: utf-8
"""
@author: kosmosr
@contact: zmhwft@gmail.com
@time: 2018/8/5 21:32
"""
import logging

logger = logging.getLogger('fisher')
logger.setLevel(logging.DEBUG)

console_formater = logging.Formatter(
    ":%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formater)

logger.addHandler(console_handler)
