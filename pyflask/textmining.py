#%% reading dataframe

import pandas as pd
import re
import time
import nltk
import random
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from collections import Counter
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

#delete meaningless before nltk
def enter(value):
    pattern = '\\n'
    repl = ''
    cleaned_enter = re.sub(pattern,repl,value)
    return cleaned_enter


def delete_http(value):
    pattern = 'https?://(\w|[^\w\s])+'
    repl = ''
    cleaned_result = re.sub(pattern,repl,value)
    return cleaned_result

def delete_pic(value):
    pattern = 'pic.twitter.com/\S+'
    repl = ''
    cleaned_pic = re.sub(pattern,repl,value)
    return cleaned_pic

def delete_rt(value):
    pattern = 'RT'
    repl = ''
    cleaned_rt = re.sub(pattern,repl,value)
    return cleaned_rt

def delete_tag(value):
    pattern = '@\S+[ ]?'
    repl = ''
    cleaned_tag = re.sub(pattern,repl,value)
    return cleaned_tag

def delete_symbol(value):
    pattern = '[^\w\s]'
    repl = ''
    cleaned_symbol = re.sub(pattern,repl,value)
    return cleaned_symbol







#%% #preprocessing with nltk

import nltk
#import random
#import webbrowser
import pandas as pd
#import matplotlib.pyplot as plt
#import csv

#from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#from nltk.stem import PorterStemmer
from collections import Counter
from flask import Flask
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')



# Data Preprocessing
def preprocessing(data): # 텍스트 파일을 토큰화 
    #데이터프레임 여기서 받아야함 
    
    datastring = data.to_string(index=False)
    data= delete_http(datastring)
    data= delete_pic(data)
    data= delete_rt(data)
    data= delete_tag(data) 
    data= delete_symbol(data)
    data= enter(data)

    tokens = [word for sent in nltk.sent_tokenize(datastring)
              for word in nltk.word_tokenize(sent)]
  
    # stopwards 제거 
    stop = stopwords.words('english')
    tokens = [token for token in tokens if token not in stop]

    # 문장부호 제거
    tokens = [word for word in tokens if len(word) >= 3]

    # 소문자화
    tokens = [word.lower() for word in tokens]

    # 표제어 추출
    lmtzr = WordNetLemmatizer()
    tokens = [lmtzr.lemmatize(word) for word in tokens]
    tokens = [lmtzr.lemmatize(word, 'v') for word in tokens]
    preprocessed_text= ' '.join(tokens)
    return preprocessed_text

#data = "The meaning is well known, even if it is not in complete accord with the reality. The restored stream evokes the environment but is not environmental, evokes history but is not historical, and evokes tradition without being traditional. The reality is conflicted. The restoration was huge in scale and high in cost. The cost overruns alone amounted to $34 million out of a total of about $351 million. Annual maintenance costs have been increasing while the overall number of visitors has declined."




def listupKeyword(preprocessed):

    list_preprocessed = preprocessed.split()
    delete = 'con,call,come,could,day,dont,even,know,right,find,first,fuck,http,and,this,get,go,leave,like,long,look,made,make,many,may,name,number,one,part,people,said,see,somebody,time,two,use,water,way,word,this,and,would,woman,write'
    delete = delete.split(',')
    list_preprocessed = [a for a in list_preprocessed if a not in delete]
    counter = Counter(list_preprocessed)
    counter.update(list_preprocessed)
    a = counter.most_common(n=11)


    arr = np.asarray(a)

    arr=[key for key, value in dict(arr).items()]

    return arr
    


# %%


# %%
