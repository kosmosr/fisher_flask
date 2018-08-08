#!/usr/bin/env python
# encoding: utf-8
"""
@author: zmh
@time: 2018/7/2 16:09
数据库跟踪
初始化  python manage.py db init
创建迁移脚本  python manage.py db migrate
更新数据库  python manage.py db upgrade
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from ext.db import db
from run import server

# 导入需要迁移的数据库模型
# 让python支持命令行工作
manager = Manager(server)

# 使用migrate绑定app和db
migrate = Migrate(server, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

