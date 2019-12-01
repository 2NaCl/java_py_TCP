# -*- coding: UTF-8 -*-
from socket import *
from time import ctime
import jieba
from jieba import posseg
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, cross_validate


material_userdict = 'material_userdict.txt'
device_userdict = 'device_userdict.txt'
worker_userdict = 'worker_userdict.txt'
question_file = 'questions.txt'

#model_file = 'forest'
model_file = 'forest_test'

question_row = 'questions'
question_cut_row = 'questions_cut'

POS = ['mmm', 'mmd', 'mmw', 'm']

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

jieba.load_userdict(material_userdict)
jieba.load_userdict(device_userdict)
jieba.load_userdict(worker_userdict)


def cut(string):
    return ' '.join(jieba.cut(string))


questions = pd.read_csv(question_file, sep='\t', encoding='utf-8')


questions[question_cut_row] = questions[question_row].apply(cut)



import pickle

with open(model_file, 'rb') as training_model:
    model = pickle.load(training_model)


def abstract_str(test_string):
    seg = jieba.posseg.cut(test_string)
    l = []
    for i in seg:
        l.append((str(i.word), str(i.flag)))
        tcpCliSock.send(((str(i.word) + ',' + str(i.flag) + " ").encode()))
    print(l)
    # print(l[0][0])
    fin_str = ''
    variable = ''

    for j in range(len(l)):
        if l[j][1] == POS[0]:
            fin_str += POS[0]
            variable = l[j][0]
        elif l[j][1] == POS[1]:
            fin_str += POS[1]
            variable = l[j][0]
        elif l[j][1] == POS[2]:
            fin_str += POS[2]
        else:
            fin_str += l[j][0]
    return fin_str, variable


def vectorized_str(test_string):
    test_cut = cut(test_string)
    test_feature = vectorizer.transform([test_cut]).toarray()
    return test_feature


vectorizer = CountVectorizer()
data_features = vectorizer.fit_transform(questions[question_cut_row]).toarray()

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('把客户端启动一下啊')
    tcpCliSock, addr = tcpSerSock.accept()
    print('ip:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ).decode()
        if not data:
            break
        print('get client data:%s\n[%s]' % (data, ctime()))
        test_string = data
        a_s, variable = abstract_str(test_string)
        v_s = vectorized_str(a_s)
        result = model.predict(v_s)
        result = str(result) + '\n' + str(variable)
        send_str=('server send data:%s\n[%s]' % (result, ctime()))
        tcpCliSock.send(result.encode())
        if data == 'session_close':
            break
    tcpCliSock.close
tcpSerSock.close
# test_string='000000009000111870编码物料的库存数量'
# 000000009000111870物料的在BOM中的使用情况
