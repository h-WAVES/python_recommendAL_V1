#!usr/bin/env python
#_*_ coding:utf-8 _*_
import jieba,math
import jieba.analyse
import pandas as pd

class jieba_text():
    #1、jieba tfidf keywords
    def jieba_ana(self,text):
        #jieba add word_dict
        jieba.add_word("市辖区")
        #jieba.load_userdict(file_name) # file_name为自定义词典的路径 同dict.txt
        total=len(list(jieba.cut(text)))
        print(total)
        get_cnt=math.ceil(total*0.1)  #向上取整
        print('jieba总数{},取出数据{}'.format(total,get_cnt))
        # 1. jieba.analyse.extract_tags
        tfidf_keywords = jieba.analyse.extract_tags(text, topK=20,withWeight=False)#,allowPOS=('a','n','ns')\allowPOS=('a','v','vd')
        # print ('jiebaTFIDF关键词{}'.format(tfidf_keywords))
        return tfidf_keywords
        # 2. jieba.analyse.textran
        #textrank_keywords=jieba.analyse.textrank(text, topK=100, withWeight=False)
        # print ('jiebaTEXTRANK关键词{}'.format(textrank_keywords))
        # return textrank_keywords
        # help(jieba.analyse.textrank)
    #2、tfidf  topK
    def jieba_tfidf_all(self,text):
        tfidf_all= jieba.analyse.extract_tags(text, topK=1000,withWeight=False)
        return tfidf_all
    #3、基于jieba  textrank
    def jieba_textrank(self,text):
        textrank_keywords=jieba.analyse.textrank(text, topK=20, withWeight=False)
        return textrank_keywords
    #4、 jieba.cut分割,精准模式
    def jieba_cut(self,text):
        word_corpos=jieba.cut(text)
        return word_corpos
    #5、jieba.analyse.textrank 提取词性nt
    def jieba_rank_allowPOS(self,text):
        rank_allowPOS=jieba.analyse.textrank(text, topK=20, withWeight=False,allowPOS=('nt'))
        return rank_allowPOS
     #6、jieba.analyse.textrank 提取词性vn
    def jieba_tfidf_allowPOS(self,text):
        tfidf_allowPOS=jieba.analyse.tfidf(text, topK=20, withWeight=False,allowPOS=('vn'))
        return tfidf_allowPOS
    #7、 人工剔除停用词
    def jieba_stopword(self,text):
        #1、默认的停用词表
        # stopword_text='D:\\office3\\python\\anaconda3\\3.4.3\\Lib\\site-packages\\textrank4zh\\stopwords.txt'
        #2、全部的省市区县的停用词表，在英文后加了对应的停用词
        stopword_text='C:\\Users\\lenovo\\Desktop\\停用词文件\\stopwords_source_506 _all_city.txt'
        jieba.add_word('长江中游')
        stop = [line.strip() for line in open(stopword_text,'r',encoding='UTF-8').readlines() ]
        #加载自定义词库
        # jieba.load_userdict('C:\\Users\\lenovo\\Desktop\\停用词文件\\dict_1.txt')
        word_1=jieba.cut(text,cut_all=False)
        ret = []
        for i in word_1:
            if i not in stop and len(i)!=0:  # !=0处理的是''空字符
                ret.append(i)
        return  ret
     #人工剔除停用词，并将类似湖','海','寺'等两次写入
    def jieba_stopword_1(self,text):
        #1、默认的停用词表
        # stopword_text='D:\\office3\\python\\anaconda3\\3.4.3\\Lib\\site-packages\\textrank4zh\\stopwords.txt'
        #2、全部的省市区县的停用词表，在英文后加了对应的停用词
        stopword_text='C:\\Users\\lenovo\\Desktop\\停用词文件\\stopwords_source_506 _all_city.txt'
        jieba.add_word('长江中游')
        stop = [line.strip() for line in open(stopword_text,'r',encoding='UTF-8').readlines() ]
        #加载自定义词库
        # jieba.load_userdict('C:\\Users\\lenovo\\Desktop\\停用词文件\\dict_1.txt')
        word_1=jieba.cut(text,cut_all=False)
        ret = []
        for i in word_1:
            if i not in stop and len(i)!=0: #!=0处理的是''空字符
                ret.append(i)
        # print(ret)

        #写入关键词后缀，
        data=pd.read_csv('C:\\Users\\lenovo\\Desktop\\handle_data_01.txt',sep='\n')
        words=[]
        for i in data.drop_duplicates(['word'])['word']:#去重处理259个词
            words.append(i)
        # words=['湖','海','寺','博物馆','遗址','祠堂','庙','旧址','清真寺','纪念馆','乐园','温泉','教堂']
        for word in words:
            j=0
            while j < len(ret):
                # print('j={}'.format(j))
                if ret[j].startswith( word,len(ret[j])-len(word))and len(word)!=len(ret[j]):
                    # print('j={}'.format(j))
                    # ret.insert(ret.index(ret[j])+1,ret[j].split(word)[0])
                    # ret.insert(ret.index(ret[j].split(word)[0]),word)
                    ret.insert(j+1,ret[j].split(word)[0])
                    ret.insert(j+2,word)
                    j=j+3
                    # print('j+2={}'.format(j))
                    # print(ret)
                else:
                    j+=1
                    # print(ret)
        # print(ret)



        return  ret









# a=jieba_text()
# text='asdasdsdfdsfff'
# a.jieba_ana(text)