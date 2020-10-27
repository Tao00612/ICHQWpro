import scrapy
from ICHQWpro.mysql.mysql_utils.mysql_conf import MySQLS
from ICHQWpro.mysql.mysql_utils.mysql_conn import MysqlPooledDB


class IchqSpider(scrapy.Spider):
    name = 'ichq'
    # allowed_domains = ['www.xx.com']
    # start_urls = ['https://ibsv3.hqew.com/']

    def get_data(self):
        sql = """
            select model from szlc GROUP BY model;
        """
        self.conn, self.cursor = MysqlPooledDB(MySQLS['me']).connect()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def start_requests(self):
        word_list = self.get_data()
        for word in word_list:
            word = word['model']
            url = 'https://s.hqew.com/' + word + '.html'
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response,**kwargs):
        tr_list = response.xpath('//div[@id="resultList"]/div/table/tbody/tr[contains(@sid,"s")]')
        if tr_list:
            for tr in tr_list:
                item = {}
                item['com_name'] = tr.xpath('./td[@class="j-company-td"]/p/a/@cname').extract_first()
                item['com_name_url'] = tr.xpath('./td[@class="j-company-td"]/p/a/@href').extract_first()
                item['model'] = tr.xpath('./td[@class="td-model"]/div/a[1]/text()').extract_first()
                item['amount'] = tr.xpath('./td[@class="td-stockNum"]/p[1]/text()').extract_first()
                item['brand'] = tr.xpath('./td[@class="td-brand"]/div/@title').extract_first()
                item['batch_num'] = tr.xpath('./td[8]/p/text()').extract_first()
                item['package'] = tr.xpath('./td[9]/p/text()').extract_first()
                item['parameter'] = tr.xpath('./td[@class="td-param"]/div/@title').extract_first()
                item['depot'] = tr.xpath('./td[last()-2]/p/text()').extract_first()
                item['desc_ic'] = tr.xpath('./td[last()-1]/div/@title').extract_first()
                yield item

            # 翻页
            next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
            if next_url:
                next_url = response.urljoin(next_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )
        else:
            print('查无结果')