#!usr/bin/env python
#_*_ coding:utf-8 _*_
"""
obj:从数据库中取出数据，之后构建user与item矩阵，计算皮尔森相关系数，基于协同过滤进行推荐
date:2018-4-12
author:hht
references：https://blog.csdn.net/hhtnan/article/details/79882314
"""
from pymongo import MongoClient
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

############################################第一部分  八纬度矩阵推荐，Collaborative filtering usr,item

class get_matrix(object):
    #连接mongodb数据
    Client=MongoClient('39.106.209.xx',27017)
    db=Client.away
    def get_eight(self):
        data1=self.db.user.find({"_id":{"$ne":["5abf7a47707d6d3d9c7ef50e","5acc89a7707d6d1efbe99ce0"]}})
        #数据演示，(3,8)
        n_users=3
        n_items=8
        train_data_matrix = np.zeros((n_users, n_items))
        for x in data1:
            try:
                for i in range(n_users):
                    for j in range(n_items):
                        train_data_matrix[i,j]=x["eight_dim"][j]["typeValue"]
            except:

                print(x["_id"])

        print(train_data_matrix)
        return train_data_matrix
        # 你可以使用 sklearn 的pairwise_distances函数来计算余弦相似性。注意，因为评价都为正值输出取值应为0到1.

    def predict(slef,ratings,type='user'):

        if type == 'user':

            similarity=pairwise_distances(train_data_matrix, metric='cosine')
            mean_user_rating = ratings.mean(axis=1)
            # #You use np.newaxis so that mean_user_rating has same format as ratings
            ratings_diff = (ratings - mean_user_rating[:, np.newaxis])

            # 方法1  pred=均值+皮尔森相似度
            pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
            #方法二 similarity.dot(ratings_diff)
            # pred = similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
            #方法三 得到和原始矩阵ratings，相似的矩阵
            # pred = similarity.dot(ratings) / np.array([np.abs(similarity).sum(axis=1)]).T

        elif type == 'item':
            #矩阵的转置实现主题的相似度
            similarity= pairwise_distances(train_data_matrix.T, metric='cosine')
            pred = ratings.dot(similarity)/np.array([np.abs(similarity).sum(axis=1)])

        return pred
    def recommend(self,pred):
        #对数据由小到大排序，输出排序的索引，之后输出后面三个索引，即推荐的前三个次序
        axis_1=np.argsort(pred,axis=1)
        print(axis_1)
        # 推荐结果
        print(axis_1[:,-3:])





################################################第二部分  统计标签流行度函数###
    #统计标签流行度
    @staticmethod
    def TagPopularity(records):
        tagfreq = dict()
        for user, item ,tag in records:
            if tag not in tagfreq:
                tagfreq[tag] = 1
            else:
                tagfreq[tag] +=1
        return tagfreq


if __name__=="__main__":
    train_data_matrix=get_matrix().get_eight()
    pred=get_matrix().predict(train_data_matrix, type='user')
    get_matrix().recommend(pred)