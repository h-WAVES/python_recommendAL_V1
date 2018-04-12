#!usr/bin/env python
#_*_ coding:utf-8 _*_

#!usr/bin/env python
#_*_ coding:utf-8 _*_


#通过访问字典实现遍历
from pymongo import MongoClient



class get_matrix(object):
    Client=MongoClient('192.168.1.xx',27017)
    db=Client.user
    def get_eight(self):
        data1=self.db.testUser.find({})
        dic={}
        reverse={}
        for x in data1:
            #  构建入度
            rank = {y:1 for y in x["hate_poi_list"]}
            dic[x["nickName"]]=rank
            #   构建出度
            for z in x["hate_poi_list"]:
                 reverse.setdefault(z,set()).add(x['nickName'])
                 out_dic=reverse
                 #构建出度
                 for k,v in out_dic.items():
                     v=list(v)  #v为set类型
                     if len(v)<=1:
                        dic[k]={v[0]:1}
                     else:
                         temp={v1:1 for  v1 in v}
                         dic[k]=temp


        print(dic)
        # print(reverse)






if __name__=="__main__":
   get_matrix().get_eight()




