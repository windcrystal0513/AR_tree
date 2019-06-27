# -*- coding: utf-8 -*-
import pymysql
import igraph
import networkx


# 创建一个空对象
G=igraph.Graph(directed=True)
# g = igraph.Graph(directed=True)
g=networkx.DiGraph()
# 添加网络中的点
# v=[1,2,3,4]
# g.add_vertices(v)

# 添加网络中的边
# e=[(1,2),(2,3)]
g.add_edge(5,2)
g.add_edge(2,3)
g.add_edge(1,4)
# print(g.vs['name'])
G=g
print(u)
print(G.vs['name'])
