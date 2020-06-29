#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 23:16:11 2020

@author: jeong-wonlyeol
"""
from flask import Flask, request, Response , render_template
import urllib.request 
import json
from collections import Counter
import ssl
import pandas as pd 
import pymysql
import textmining as TM 
import time

global t
class Database():
    def __init__(self):
        self.db= pymysql.connect(host='localhost',
                                  user='root',
                                  password='1234',
                                  db='mysql',
                                  )
        
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)



    def deleteData (self):
        a = " delete from textdata WHERE d < NOW() - INTERVAL 30 DAY"
        self.cursor.execute(a)

    def extractData(self,condition):
    
        query = "SELECT t FROM textdata where t like '%"+condition+"%'"
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        result = pd.DataFrame(myresult)
        
        self.commit()
        return result
    def commit(self):
        self.db.commit()


app = Flask(__name__)

key="AIzaSyA-MC1nPXEeEgIiNTLn70-7r_Y3ys23ClY"


def tagCount(tag):
    delete = '1,2,3,4,5,6,7,8,9,0,b,c,con,you,call,cant,chance,change,come,cop,could,day,dont,dozen,even,everyone,know,right,f,find,first,feel,fuck,g,give,get,go,good,guy,h,happen,hope,ill,im,ive,leave,let,li,like,live,long,look,lot,made,make,man,many,may,month,much,na,name,need,never,new,number,one,part,people,please,really,said,say,see,shit,somebody,someone,start,still,stop,take,tell,time,th,thank,thing,think,today,tr,tweet,two,u,use,w,watch,water,want,way,word,would,woman,write,yall,year,youre'
    delete = delete.split(',')

    list_preprocessed = [a for a in tag if a not in delete]
    counter = Counter(list_preprocessed) # 추가된 리스트를 누적하여 센다
    counter.update(list_preprocessed)
    a = counter.most_common(n=20) # 빈도수가 높은 10개의 키워드를 출력한다
    return a




def video_data(vname):
    t = time.time()
    context = ssl._create_unverified_context()
    dataV=urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet&id="+vname+"&key="+key,context=context).read()
    t2 = time.time()
    print(t2-t)
    if t2-t > 10:
        return "Three is no videos like you input!"    
    try:
        return json.loads(dataV)['items'][0]["snippet"]["tags"]

    except IndexError:
        value = "This Video have no tags! or just system is slow, please try again!"

        return value


@app.route('/showList', methods=['POST'])
def showList():
    
    value = request.form['URL']
    
    
    value = value.replace("https://","")
    value = value.replace("www.youtube.com/watch?v=","")

    if value == "":
        return "thre is no input variables"
    tag = video_data(value)
    
    if str(type(tag)) == "class<'str'>":
        return tag
    
    
    keyword = tagCount(tag)[0][0]
    
  
    db = Database()
    data = db.extractData(keyword)

    find = TM.listupKeyword(TM.preprocessing(data))
    


    return render_template('showList.html', testdata=find)


@app.route('/')
def root_response():
    db = Database()
    db.deleteData()
    db.commit()
    return render_template("home.html" )


if __name__ == '__main__':
    app.run(debug = True)#import mysql.connector





    