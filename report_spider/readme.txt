依托库：
python 2.7
scrapy 1.3.3

运行方法：
1.自建同名scrapy工程
2.用report_spider整个文件夹进行覆盖
3.cd至report_spider根目录下
4.bash setup.py
5.python crawl.py

说明：
1.保存文件夹为’/var/lib/spider_save/时间(eg:20170401)/学校简称(eg:合肥工业大学->HFUT)
/学院号(eg:中国科学技术大学计算机学院->USTC001)’
2.每一天的文件被单独保存在一个文件夹中
3.每次运行crawl.py会清空上一次(当日)爬取的所有内容
4.不要改文件名，否则路径不对