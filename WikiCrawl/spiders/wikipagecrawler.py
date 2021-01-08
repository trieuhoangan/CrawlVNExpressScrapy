# -*- coding: utf-8 -*-
import scrapy
import pymysql
import pymysql.cursors
import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
def checkExist(url, list):
    for element in list:
        if url == element:
            return True
    return False
class WikipagecrawlerSpider(scrapy.Spider):
    name = 'wikipagecrawler'
    allowed_domains = ['vi.wikipedia.org']
    domain = "https://vi.wikipedia.org"
    start_urls = ['https://vi.wikipedia.org/wiki/H%E1%BB%93_Ch%C3%AD_Minh']
    inline_urls = []
    inline_url_id = 0
    def parse(self, response):
        titles = response.css("h1.firstHeading::text").extract()
        title = titles[0]
        container = response.css("div.mw-parser-output")
        if container!= None: 
            inline_url = container.css("p a::attr(href)").extract()
            
            # if self.inline_url_id == 0:
            #     with open("inline_url.txt",encoding='utf-8',mode='w') as writer:
            #         # for url in self.inline_urls:
            #         #     writer.write(url+"\n")
            #         writer.write(str(all))
            for url in inline_url:
                if url[0]!="#" and "index.php" not in url:
                    full_url = self.domain+url
                    if checkExist(full_url,self.inline_urls) == False:
                        self.inline_urls.append(full_url)
            connection = pymysql.connect(host='localhost',
                                user='root',
                                password='12345678',
                                db='wiki_db',
                                charset='utf8',
                                cursorclass=pymysql.cursors.DictCursor)
            print(response.url,"\n")
            try:
                with connection.cursor() as cursor:
                    sql = "select title from raw_page where title='{}'".format(title)
                    cursor.execute(sql)
                    if cursor.fetchone() == None:
                        content = response.css("div.mw-parser-output").extract()
                        all = ""
                        for line in content:
                            all = all + line
                        all = all.replace("'",'-')
                        sql = "insert into raw_page (fullurl,title,html) value ('{}','{}','{}')".format(response.url,title,all)
                        cursor.execute(sql)
                    connection.commit()
            finally:
                connection.close()
        
        yield response.follow(self.inline_urls[self.inline_url_id],callback = self.parse)
        self.inline_url_id = self.inline_url_id+1
    # def second_parse(self, response):
    #     pass

