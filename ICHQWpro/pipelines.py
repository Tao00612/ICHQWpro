from ICHQWpro.mysql.mysql_utils.mysql_conf import MySQLS
from ICHQWpro.mysql.mysql_utils.mysql_conn import MysqlPooledDB


class Pipeline:

    def open_spider(self, spider):
        print('开始')
        self.count = 0
        self.conn, self.cursor = MysqlPooledDB(MySQLS['me']).connect()

    def count_num(self):
        if self.count % 100 == 0:
            print(f'已经爬取{self.count}条数据')

    def process_item(self, item, spider):
        item = dict(item)
        sql = """
            insert into hqic(%s) values(%s)
        """
        fields = ','.join(item)
        value = ','.join(['%%(%s)s' % key for key in item])
        try:
            self.count_num()
            self.cursor.execute(sql % (fields, value), item)
            self.conn.commit()
            self.count += 1
        except Exception as e:
            print(e)
            self.cursor.rollback()
        return item

    def close_spider(self, spider):

        self.cursor.close()
        self.conn.close()
