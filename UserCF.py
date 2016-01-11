import sys
import operator
import math

W = {}

def LoadData():
  #train = {userId:[iterm1, item2...]} 训练数据
  #W = {u:{v:value}} 用户间相似度
  #item_users = {item, [user1,user2...]}倒排表
  #N(u) = {u:value} 用户u喜欢的Item
  test = {}
  train = {}
  TrainFile = 'u2.base'
  TestFile = 'u2.test'

  with open(TrainFile,'r') as file_object:
    for line in file_object:
      (userId, itemId, rating, _) = line.strip().split('\t')
      train.setdefault(userId,[])
      if userId not in train:
        train[userId] = itemId
      else:
        train[userId].append(itemId)

  with open(TestFile,'r') as test_object:
    for line in test_object:
      (userId, itemId, rating, _) = line.strip().split('\t')
      test.setdefault(userId,[])
      if userId not in test:
        test[userId] = itemId
      else:
        test[userId].append(itemId)

  return train, test


def UserSimilarityS(train):
  # 倒排表
  item_users = {}
  for u,items in train.items():
    for i in items:
      if i not in item_users.keys():
        item_users[i] = list()
      item_users[i].append(u)

  #计算用户间共同评分的物品
  C = {}
  N = {}
  for item, users in item_users.items():
    for u in users:
      C.setdefault(u,{})
      N.setdefault(u,0)
      N[u] += 1
      for v in users:
        if u==v:
          continue
        C[u].setdefault(v,0)
        C[u][v] += 1

  #计算相似性矩阵W

  for u,related_users in C.items():
    W.setdefault(u,{})
    for v,cuv in related_users.items():
      W[u][v] = cuv / math.sqrt(N[u] * N[v])

def RecommendN(user, train, N):
  rank = {}
  rank.setdefault(user,{})
  interacted_items = train[user]
  for v,wuv in sorted(W[user].items(), key=operator.itemgetter(1), reverse=True)[0:160]:
    for i in train[v]:
      if i in interacted_items:

        continue
      rank[user].setdefault(i,0)
       #设置用户至少对一个Item感兴趣
      rvi = 1
      rank[user][i] += wuv * rvi
  n_rank = sorted(rank[user].items(), key=operator.itemgetter(1), reverse=True)[:N]

  return n_rank

#召回率
def Recall(train, test, N):
  hit = 0
  all = 0
  for user in test.keys():
    tui = test[user]
    n_rank = RecommendN(user, train, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += len(tui)
  return hit/(all * 1.0)
#准确率
def Precision(train, test, N):
  hit = 0
  all = 0
  for user in test.keys():
    tui = test[user]
    n_rank = RecommendN(user, train, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += N
  return hit/(all * 1.0)



if __name__ == '__main__':
  train, test  = LoadData()
  UserSimilarityS(train)

  recall = Recall(train, test, 5)
  precision = Precision(train, test, 5)

  print ('test recall: ', recall)
  print ('test precision: ', precision)
