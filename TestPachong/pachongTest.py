import urllib.request
import mysql.connector
from Tools.scripts.treesync import raw_input
import bs4
from bs4 import BeautifulSoup

#爬取的网页地址
response = urllib.request.urlopen('https://jn.fang.lianjia.com/loupan/lixia/nht1/#lixia')
buff = response.read()
#编码方式
html = buff.decode("utf-8")
html_doc =html
soup = BeautifulSoup(html_doc,'html.parser')
#数据库操作
conn = mysql.connector.connect(user='root', password='root', database='mydb_one')
cursor = conn.cursor()
#存放的表及字段
sql="""insert into ll_pachong(LL_NAME,LL_PRICE,LL_XH) VALUES """
number=0
try:
   # 执行sql语句
   print('-----------------------------------------------------------------------')
   cursor.execute('select * from ll_pachong ')
   values = cursor.fetchall()
   print('输出结果：', values)
   #获取需要的内容并存入mysql数据库
   for link in soup.select('.resblock-list-wrapper'):
       for ul in link.select('.resblock-desc-wrapper'):
           number=number+1
           nam=(ul.select('.name'))[0].get_text()
           price=(ul.select('.number'))[0].get_text()
           cursor.execute("insert into ll_pachong(LL_NAME,LL_PRICE,LL_XH) VALUES ('"+nam+"','"+price+"','"+str(number)+"')")
           print((ul.select('.name'))[0].get_text())
           print((ul.select('.number'))[0].get_text())

   # 提交到数据库执行
   conn.commit()
except Exception as e:
    raise e
    # 发生错误时回滚
    conn.rollback()

cursor.close()
conn.close()