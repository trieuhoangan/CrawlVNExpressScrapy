# CrawlVNExpressScrapy

1. Required 
  a) Python 3
  b) MySQL Server
2. Install 
  1. open cmd then run these
    - pip install scrapy
    - pip install re
    - pip install PyMySQL
  2. create database by running the file named "createDatabase.sql" in mysql and congif the database connection in tutorial/spiders/Alice.py at line 102
  3. open cmd in main folder and run : scrapy crawl alice
  4. config limit number of content in tutorial/spiders/Alice.py at line 9
