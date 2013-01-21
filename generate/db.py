#!/usr/bin/python
import os, MySQLdb,sys
sys.path.append("/var/www")
from config import *
photos=os.listdir('../pictures/')
photos.sort()
db=MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DB,charset='utf8')
cursor=db.cursor()
for photo in photos:
    sql="INSERT IGNORE INTO photos(file,rate) VALUES ('%s','%d')"%(photo,0)
    cursor.execute(sql)
    db.commit()
db.close()

