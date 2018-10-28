# -*- coding: utf-8 -*-
import scrapy
import re
import pymysql.cursors
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
i = 0
j = 0
#numbers = open("D:\\Python\tutorial\number.txt",'r')
#i = numbers.read
#numbers.close
#numbers = open("D:\\Python\tutorial\chapter.txt",'r')
#j = numbers.read
#numbers.close

class AliceSpider(scrapy.Spider):
    
    name = "alice"
    def start_requests(self):
        urls = [
            'https://vnexpress.net/tin-tuc/thoi-su',
            'https://vnexpress.net/tin-tuc/the-gioi',
            'https://kinhdoanh.vnexpress.net/',
            'https://giaitri.vnexpress.net/',
            'https://thethao.vnexpress.net',
            'https://vnexpress.net/tin-tuc/phap-luat',
            'https://vnexpress.net/tin-tuc/giao-duc',
            'https://suckhoe.vnexpress.net',
            'https://doisong.vnexpress.net/',
            'https://dulich.vnexpress.net',
            'https://vnexpress.net/tin-tuc/khoa-hoc',
            'https://sohoa.vnexpress.net/',
            'https://vnexpress.net/tin-tuc/oto-xe-may',
            'https://vnexpress.net/tin-tuc/cong-dong',
            'https://vnexpress.net/tin-tuc/tam-su',
            'https://vnexpress.net/tin-tuc/cuoi',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):	
        if i < 50:
            savefile = "savelinks.txt"
            updatefile = 'update.txt'
            listofVB = response.css('h3.title_news a.icon_commend::attr(href)').extract()
            opensavefile = open(savefile,'w+',encoding = 'utf-8',errors ='replace')
            for link in listofVB:
                yield response.follow(link, callback = self.parse_VB)
                opensavefile.write(link)
                if(i == 1):
                    openupdatefile = open(updatefile,'w',encoding = 'utf-8', errors = 'replace')
                    openupdatefile.write(link)
                    openupdatefile.close
            global j
            Pages = response.css('div[id*=pagination] a::attr(href)')
            if j==0:
                nextPage = Pages[1].extract()
            
            if j==1:
                nextPage = Pages[3].extract()
            
            if j>1:
                nextPage = Pages[4].extract()

            j = j+1
            if "http" not in nextPage:
                nextPage = "https://vnexpress.net"+nextPage
            yield response.follow(nextPage,callback = self.parse)
        
    def parse_VB(self, response):
        global i
        if i < 50:
        #VB_container = response.css('div.cldivContentDocVN').extract()
        #filee = response.css("title::text").extract_first().strip()
        #filename = str(filee)+".txt"
            # a = str(i)
            VB_container = response.css("article.content_detail")
            if bool(VB_container)==False:
                VB_container = response.css("div.fck_detail")
            title = response.css("h1.title_news_detail::text").extract_first()
            cleanr = re.compile('<.*?>',flags=re.DOTALL)
            title = re.sub(cleanr,'',title)
            valid_file_name_character = re.compile('[\\~#%&*{}/:<>?|\"-]')
            title = re.sub(valid_file_name_character,'',title)
            title = title.replace('\n','')
            title = title.strip()
            filename ='news/'+title+".txt"
            f = open(filename,'w',encoding='utf-8')
            VB_saver = str(VB_container.extract_first())
            VB_saver = VB_saver.replace('\r','')
            VB_saver = VB_saver.replace('\xa0','')
            VB_saver = VB_saver.replace('&nbsp','')
            VB_saver = VB_saver.strip()
            print("saving document")
            Cat = re.sub(cleanr,'',VB_saver)
            Cat = Cat.strip()
            # n = len(Cat)
            f.write(Cat)
            i = i +1
            f.close

            connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12345678',
                             db='Alice',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
            sentences = Cat.split('.')
            numberOfSentence = int(len(sentences))

            try:
                with connection.cursor() as cursor:
                    sql = "SELECT `title` FROM `newspaper` WHERE `title`=%s"
                    cursor.execute(sql, (title))
                    result = cursor.fetchone()
                    if bool(result)==False:
                    # Create a new record
                        sql = "INSERT INTO `newspaper` (`title`, `content`,`sentences`) VALUES (%s, %s, %s)"
                        cursor.execute(sql, (title,Cat,numberOfSentence))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

                # with connection.cursor() as cursor:
                #     # Read a single record
                    
                    
                #     result = cursor.fetchone()
                #     print(result)
            finally:
                connection.close()
            # numbers = open("number.txt",'w')
            # numbers.write(i)
            # numbers.close
            # numbers = open("chapter.txt",'w')
            # numbers.write(j)
            # numbers.close            
        

        