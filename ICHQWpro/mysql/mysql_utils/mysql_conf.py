# -*- coding:utf-8 -*-

# MySQL连接池的配置
MySQLS = {
    'me': {
        "maxconnections": 0,  # 连接池允许的最大连接数，0和None表示不限制连接数
        "mincached": 2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        "maxcached": 0,  # 链接池中最多闲置的链接，0和None不限制
        "maxusage": 1,  # 一个链接最多被重复使用的次数，None表示无限制
        "blocking": True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123',
        'db': 'spidernew',
        'port': 3306,
        'charset': 'utf8',
    }
}
