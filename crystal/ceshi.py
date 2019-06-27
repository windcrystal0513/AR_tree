# -*- coding: utf-8 -*-
import pymysql
import igraph
d={
                        "log_id": 2794890503604904799,
                        "direction": 2,
                        "words_result_num": 8,
                        "words_result": [
                            {
                            "location": {
                                "width": 122,
                                "top": 352,
                                "left": 424,
                                "height": 34
                            },
                            "words": "数据结"
                            },
                            {
                            "location": {
                                "width": 125,
                                "top": 293,
                                "left": 308,
                                "height": 35
                            },
                            "words": "函数"
                            },
                            {
                            "location": {
                                "width": 157,
                                "top": 231,
                                "left": 72,
                                "height": 36
                            },
                            "words": "计算机视觉"
                            },
                            {
                            "location": {
                                "width": 67,
                                "top": 169,
                                "left": 365,
                                "height": 35
                            },
                            "words": "算"
                            },
                            {
                            "location": {
                                "width": 126,
                                "top": 107,
                                "left": 218,
                                "height": 33
                            },
                            "words": "这是C言的"
                            }
                        ]
                        }

db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")

alltopic=[]
alltopicid=[]
cursor = db.cursor()
sql = "SELECT * FROM domain \
          "
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        alltopic.append(row[1])
        alltopicid.append(row[0])
except:
        print("Error: unable to fetch data")

print(alltopic)
# for i in alltopic:
#     print(i)
# print(alltopicid)
print(len(alltopic))

num_topic=[]
num_edge=[]
for i in alltopicid:
    edge = []
    topic = []

    # SQL 查询语句
    sql = "SELECT t2.topic_name, t1.topic_name FROM dependency, topic as t1, topic as t2 \
          WHERE dependency.end_topic_id=t1.topic_id and dependency.start_topic_id=t2.topic_id and dependency.domain_id='%s' " % (i)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            row = list(row)
            edge.append(row)  # edge是一门课所有认知关系的列表
            if str(row[0]) not in topic:
                topic.append(str(row[0]))  # topic是一门课所有主题的列表
            if str(row[1]) not in topic:
                topic.append(str(row[1]))
        num_topic.append(len(topic))
        num_edge.append(len(edge))
    except:
        print("Error: unable to fetch data")
# print(topic)
print(num_topic)
for i in num_topic:
    print(i)
print(num_edge)
for i in num_edge:
    print(i)

num_topicreal=[]

for i in alltopicid:
    topic1 = []
    sql = "SELECT * FROM topic \
          WHERE domain_id='%s' " % (i)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if str(row[0]) not in topic1:
                topic1.append(str(row[0]))  # topic是一门课所有主题的列表
        num_topicreal.append(len(topic1))
    except:
        print("Error: unable to fetch data")

print(num_topicreal)
for i in num_topicreal:
    print(i)