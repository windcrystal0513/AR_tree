# -*- coding: utf-8 -*-
import pymysql
import igraph
import networkx


db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
edge = []
topicc = []
cursor = db.cursor()
# SQL 查询语句
sql = "SELECT t2.topic_name, t1.topic_name FROM dependency, domain, topic as t1, topic as t2 \
       WHERE dependency.end_topic_id=t1.topic_id and dependency.start_topic_id=t2.topic_id and" \
      " domain.domain_id=dependency.domain_id and domain.domain_name='高等数学(人工)'"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        row = list(row)
        edge.append(row)  # edge是一门课所有认知关系的列表
        if str(row[0]) not in topicc:
            topicc.append(str(row[0]))  # topic是一门课所有主题的列表
        if str(row[1]) not in topicc:
            topicc.append(str(row[1]))

except:
    print("Error: unable to fetch data")
# print("edge:",edge)
#
# print("topic",topic)
num_vtopic=len(topicc)
# 创建一个空对象
g = igraph.Graph(directed=True)
ga=igraph.Graph(directed=True)
# 添加网络中的点
g.add_vertices(topicc)
# 添加网络中的边
ga.add_vertices(topicc)
g.add_edges(edge)
# -----------------------其它信息-----------------------------
# 国家名称
g.vs['label'] = topicc
ga.vs['label']=topicc
# print(g.vs['label'])
out_num = g.degree(mode='out')  # 得到每个顶点的出度
in_num = g.degree(mode="in")  # 得到每个顶点的入度
num = g.degree()  # 得到每个顶点的度
num1 = []
for i in num:
    num1.append(i * 5)
# print(num1)
clo = g.closeness()  # 顶点的接近中心度
g.vs['daxiao'] = num1  # 为了画图时利用节点度大小设置
g.vs['indegree'] = in_num
g.vs['outdegree'] = out_num
g.vs['degree'] = num
g.vs['closeness'] = clo

# igraph.plot(g, **visual_style)
clusters = igraph.Graph.community_walktrap(g).as_clustering()  # 使用walktrap分簇

nodes = [{"name": node["name"]} for node in g.vs]
community = {}
com = []
for node in nodes:

    idx = g.vs.find(name=node["name"]).index
    node["community"] = clusters.membership[idx]
    com.append(node['community'])
    if node["community"] not in community:
        community[node["community"]] = [node["name"]]
    else:
        community[node["community"]].append(node["name"])
# for c,l in community.items():
#     print("Community ", c, ": ", l)

g.vs['com'] = com  # 为了画图时使不同簇不同颜色而设置

# print(community)

# -----------------------设置参数-----------------------------
color_dict={0:'blue',1:'red',2:'green',3:'yellow',4:'pink',5:'black',6:'orange',7:'purple',8:'brown',9:'gray',10:'tan',11:'blue',21:'red',12:'green',13:'yellow',14:'pink',15:'black',16:'orange',17:'purple',18:'brown',19:'gray',20:'tan'}
# 参数集合。visual_style是一个参数字典，可以动态添加想要个性化设定的参数
visual_style = {}
# 根据相对面积，设置点的大小
visual_style["vertex_size"] = g.vs['daxiao']
# # 根据国家实力，设置点的颜色
visual_style["vertex_color"] = [color_dict[com] for com in g.vs['com']]
# 图尺寸
visual_style["bbox"] = (1200, 1200)
# 边缘距离
visual_style["margin"] = 20
# 布局方式
visual_style["layout"] = g.layout('fr')
# -----------------------画图-----------------------------
igraph.plot(g, **visual_style)
results = {}
sum_before=0
sum_after=0
results['communities'] = []
de = []
seqe = []
for c, l in community.items():
    G = networkx.DiGraph()
    G.add_nodes_from(l)
    # print(G.node)
    sum = 0  # sum是社团内所有顶点出度和减去入度和的值，sum越大表示整个社团指向其他社团的关系越多，表明此社团越靠前
    edgec = []  # 每个簇内的所有关系列表
    edgecc=[]
    communities = {}
    key = 'commumity' + str(c)
    # print("Community ", c, ": ", l)
    communities[key] = {}
    communities[key]['topic'] = l  # 选取同属于一个簇的顶点
    seq = g.vs.select(name_in=l)  # 选取属于同一个簇的所有顶点
    # print(seq['degree'])
    # print(seq['indegree'])
    # print(seq['outdegree'])
    for ind in seq['indegree']:
        sum = sum - int(ind)
    for outd in seq['outdegree']:
        sum = sum + int(outd)
    # print(sum)
    de.append((c, sum))  # de是community的编号与sum的值对列表，用来排序各簇的先后关系
    max_clo = max(seq['closeness'])
    # print(max_clo)
    for topic in seq:
        if topic['closeness'] == max_clo:
            # print(topic['name'])
            communities[key]['cluster_name'] = topic['name']  # 获取一个簇中接近中心度最大的顶点作为这个簇的名字
    for row in edge:
        if row[0] in l and row[1] in l:
            edgec.append(row)  # 选取start和end节点全部属于同一个簇的关系
    G.add_edges_from(edgec)
    for i in edgec:
        # print(i)
        G.remove_edge(i[0],i[1])
        if networkx.has_path(G,i[0],i[1])==False:       #判断去除一条边后G中剩余的边是否有去除的边的2个顶点之间的路径
            G.add_edge(i[0],i[1])                 #没有路径，则把去掉的边再加回G,否则不加
            edgecc.append(i)                      #edgecc是一个簇内去除三角形边之后的所有边集合
    print(G.edges)
    ga.add_edges(edgecc)
    sum_before+=len(edgec)
    sum_after+=len(edgecc)

    # print(edgec)
    communities[key]['edge'] = edgecc
    results['communities'].append(communities)
# 利用de给所有簇按照sum从大到小排序得到顺序列表seqe
while len(de) != 0:
    temp = de[0][1]
    n = 0
    while n < len(de):
        if de[n][1] > temp:
            temp = de[n][1]
            templ = de[n]
            de[n] = de[0]
            de[0] = templ
        n = n + 1
    seqe.append(de[0][0])
    de.remove(de[0])
# print(seqe)
results['sequence'] = seqe
print(results)
print('sum_before:',sum_before)
print('sum_after:',sum_after)
print('totaledgesum:',len(edge))
igraph.plot(ga, **visual_style)
topic_cha=[]
topic1 = []
cursor = db.cursor()
sql = "SELECT * FROM topic \
        WHERE domain_id=416 "
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if str(row[3]) not in topic1:
            topic1.append(str(row[3]))  # topic是一门课所有主题的列表
            if str(row[3]) not in topicc:
                topic_cha.append(str(row[3]))
    num_realtopic=len(topic1)
except:
    print("Error: unable to fetch data")
print('real topic sum:',num_realtopic)
print('virtual topic sum:',num_vtopic)

print(topicc)
print(topic_cha)



