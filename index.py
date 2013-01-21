#!/usr/bin/python
# -*- coding:utf-8 -*-

import cgi,sys,os,MySQLdb,random
from config import *
try:
    db=MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWD,db=MYSQL_DB,charset='utf8')
except:
    sys.exit(1)
cursor=db.cursor()
cursor.execute("SELECT COUNT(id) from photos;")
SIZE=cursor.fetchall()[0][0]
print "Content-Type: text/html; charset=utf-8\r\n"
print '''
<!DOCTYPE HTML>
<html><head>
<META HTTP-EQUIV="Content-Type" content="text/html; charset=utf-8">
<META NAME="Title" CONTENT="Who's nicer?">
<META NAME="Description" CONTENT="Facemesh clone">
<META NAME="Document-state" CONTENT="Dynamic">
<META NAME="author" content="M_Messiah">
<script src=\"jquery-1.8.3.min.js\" type=\"text/javascript\"></script>
<script>
function choose(name1,name2) {
    $.ajax({
        type: "POST",
        url:"index.py",
        data : {choice : name1, unchoice : name2},
        success: function(data){
            $('#result').html(data);
        }});
    };
</script>
<title>Who's nicer?</title>
</head>
''' 
print "<body>"
form = cgi.FieldStorage()
print "<div align=\"center\" id='result'>"
if 'choice' in form:
    ID = [int(form['choice'].value),int(form['unchoice'].value)]
    #print "Your choice is: <br> %d rather than %d"%(ID[0],ID[1])
    rate=range(2)
    for i in range(2):
        cursor.execute("SELECT rate from photos WHERE id=%d" % ID[i])
        rate[i]=cursor.fetchall()[0][0]
    newrate=range(2)
    for i in range(2):
        e=1.0/(1+pow(10,(rate[1-i]-rate[i])/400))
        newrate[i]=rate[i]+10*(1-i-e)
    for i in range(2):
        cursor.execute("UPDATE photos SET rate='%5.2f' WHERE id=%d" % (newrate[i],ID[i]))
        db.commit()
    
print "<h1>Who is nicer?</h1><br>"
img=[random.randint(1,SIZE) for i in range(2)]
photo=range(2)
ID=img
for i in range(2):
    cursor.execute("SELECT file from photos WHERE id=%d"%ID[i])
    photo[i]=cursor.fetchall()[0][0]
for i in range(2):
    print "<img style=\"margin:20px;\" width=300px onclick=\"choose('%s','%s');\" src=\"/pictures/%s\"></img>"%(ID[i],ID[1-i],photo[i])

print "</span></body></html>"
db.close()
