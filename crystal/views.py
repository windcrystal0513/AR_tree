# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json
import urllib.request
import re
import pymysql
import igraph
import networkx
# list = ['C语言标准库', '字面常量', '变量', '注释', 'Objective-C', 'GCC', 'Go', 'C标准函式库', 'Fork','函数调用','函数', 'C语言', 'C字串函式库', 'C#', 'C11',
#             'Clang', 'C++', 'C_POSIX_library', 'ANSI_C', '顺序结构', '头文件',  '系统调用',  '指针变量', '指针', '控制语句',
#             '数据类型', '运算符', '表达式', '转义字符', '程序测试', '程序结构', '关键字', '字符编码','字符串','字符', '标识符', '输入输出', '预处理指令', '宏定义', '基本语法', '位运算',
#             'typedef', '位域', '结构体', '循环结构', '选择结构', '共用体', '链表', '进位计数制',  '数组',  '内存管理']
def getDomain(d):
# 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
    strss=[]
    strs=[]
    s=[]
    for item in d['words_result']:
        result = item.get('words')
        s.append(result)#将OCR结果里的每一行文字提取出来成一个list
# 使用cursor()方法获取操作游标
    cursor = db.cursor()
# SQL 查询语句
    sql = "SELECT * FROM topic \
           "                              #遍历数据库所有主题
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for item in s:
                result=item.find(row[3])          #row[3]是topic name
                if result>=0:
                    k=row[3]+str(row[1])          #将主题名与课程ID结合起来，避免一门课程多次识别并计数一个主题，k的形式如 函数412
                    if strs.count(k)==0:
                        strss.append(row[1])      #strss用来统计出现过主题的课程id
                        strs.append(k)
        domainid=max(strss, key=strss.count)      #取strss中出现次数最多的课程id
    except:
        print("Error: unable to fetch data")
    return domainid

    # sql = "SELECT domain_name FROM domain \
    #             WHERE domain_id='%d'" % (domainid)
    # try:
    #     cursor.execute(sql)
    #     results = cursor.fetchone()
    #     results=str(results[0])
    #     print(results)
    # except:
    #     print("Error: unable to fetch data")
    # return results
def isDomain(d):
    db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
    strs = []
    s = []
    for item in d['words_result']:
        result = item.get('words')
        s.append(result)  # 将OCR结果里的每一行文字提取出来成一个list
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "SELECT * FROM domain_copyforar \
               "  # 遍历数据库所有课程
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for item in s:
                result = item.find(row[1])  # row[1]是domain name
                if result >= 0:
                    if strs.count(row[1]) == 0:
                        strs.append(row[1])
    except:
        print("Error: unable to fetch data")
    return strs

def judgeDomainAndGetLocation(request):
    db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
    if request.method == "GET":
        strs = []
        d = json.loads(request.GET["OCR_result"])
        re=isDomain(d)
        if len(re)!=0:             #此页中没有课程有课程信息
            result = {}
            result['result_id']=0
            result['result_num']=len(re)
            result['results']=[]
            result['results'].append(re)

        else:
            domain1 = getDomain(d)  # 判断课程
            s = []
            direction = d["direction"]
            line_num = 0
            left_min = d['words_result'][0]['location']['left']
            left_max = d['words_result'][0]['location']['left'] + d['words_result'][0]['location']['width']
            top_min = d['words_result'][0]['location']['top']
            top_max = d['words_result'][0]['location']['top'] + d['words_result'][0]['location']['height']
            for item in d['words_result']:
                line_num += 1
                if left_min > item['location']['left']:
                    left_min = item['location']['left']
                if left_max < item['location']['left'] + item['location']['width']:
                    left_max = item['location']['left'] + item['location']['width']
                if top_min > item['location']['top']:
                    top_min = item['location']['top']
                if top_max < item['location']['top'] + item['location']['height']:
                    top_max = item['location']['top'] + item['location']['height']
                result = item.get('words')  # 一行里的文字
                s.append(result)  # 将所有内容装入list
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
            # SQL 查询语句
            sql = "SELECT * FROM topic \
                      WHERE domain_id = '%d'" % (domain1)  # 在得到的课程下匹配主题
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for item in s:
                    result_temp = -1  # 用来排除头几个字相同的2个长短不一的关键词被同时识别
                    for row in results:
                        result1 = item.find(row[3])  # 判断这行话中有没有list列表中的关键词
                        if result1 >= 0:
                            if result_temp != result1:  # 如果每一行文字中有2个关键词以同一位置开始，则不匹配第二个
                                result_temp = result1
                                if strs.count(row[3]) == 0:
                                    strs.append(row[3])
            except:
                print("Error: unable to fetch data")
            result={}
            result['result_id'] = 1
            key = 'border'  # 识别出的所有文字的外框坐标
            result[key] = {}
            result[key]['top'] = top_min
            result[key]['left'] = left_min
            result[key]['down'] = top_max
            result[key]['right'] = left_max
            result['results'] = []
            num = 0

            # 开始计算位置
            for i in strs:
                num1 = len(i)  # 关键词的长度
                for item in d['words_result']:
                    strss = item.get('words', 'NA')
                    result2 = strss.find(i)
                    if result2 >= 0:
                        num2 = len(strss)  # 一行文字的长度
                        if direction == 0:
                            top = item['location'].get('top') - top_min
                            left = item['location'].get('left') + (result2 / num2) * item['location'].get(
                                'width') - left_min
                            width = item['location'].get('width') * num1 / num2
                            height = item['location'].get('height')
                        elif direction == 1:
                            top = item['location'].get('top') + (((num2 - result2 - num1)) / num2) * item[
                                'location'].get('height') - top_min
                            left = item['location'].get('left') - left_min
                            height = item['location'].get('height') * num1 / num2
                            width = item['location'].get('width')
                        elif direction == 2:
                            top = item['location'].get('top') - top_min
                            left = item['location'].get('left') + ((num2 - result2 - num1) / num2) * item[
                                'location'].get(
                                'width') - left_min
                            width = item['location'].get('width') * num1 / num2
                            height = item['location'].get('height')
                        elif direction == 3:
                            top = item['location'].get('top') + (result2 / num2) * item['location'].get(
                                'height') - top_min
                            left = item['location'].get('left') - left_min
                            height = item['location'].get('height') * num1 / num2
                            width = item['location'].get('width')
                        num += 1

                        results = {}
                        results['words'] = i
                        results['location'] = {}
                        results['location']['top'] = top
                        results['location']['height'] = height
                        results['location']['left'] = left
                        results['location']['width'] = width
                        result['results'].append(results)
                        break
            key = 'result_num'
            result[key] = str(num)
            key = 'domain_id'
            result[key] = str(domain1)
        return HttpResponse(json.dumps(result), content_type="application/json")
# def location(request):
#     db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
#     if request.method == "GET":
#         strs = []
#         d = json.loads(request.GET["OCR_result"])
#         domain1=getDomain(d)    #判断课程
#         s = []
#         direction=d["direction"]
#         line_num = 0
#         left_min = d['words_result'][0]['location']['left']
#         left_max = d['words_result'][0]['location']['left'] + d['words_result'][0]['location']['width']
#         top_min=d['words_result'][0]['location']['top']
#         top_max=d['words_result'][0]['location']['top'] + d['words_result'][0]['location']['height']
#         for item in d['words_result']:
#             line_num += 1
#             if left_min > item['location']['left']:
#                 left_min = item['location']['left']
#             if left_max < item['location']['left'] + item['location']['width']:
#                 left_max = item['location']['left'] + item['location']['width']
#             if top_min > item['location']['top']:
#                 top_min = item['location']['top']
#             if top_max < item['location']['top'] + item['location']['height']:
#                 top_max = item['location']['top'] + item['location']['height']
#             result = item.get('words')#一行里的文字
#             s.append(result)     #将所有内容装入list
#         # 使用cursor()方法获取操作游标
#         cursor = db.cursor()
#         # SQL 查询语句
#         sql = "SELECT * FROM topic \
#                   WHERE domain_id = '%d'" % (domain1)            #在得到的课程下匹配主题
#         try:
#             cursor.execute(sql)
#             results = cursor.fetchall()
#             for item in s:
#                 result_temp = -1  # 用来排除头几个字相同的2个长短不一的关键词被同时识别
#                 for row in results:
#                     result1 = item.find(row[3])  # 判断这行话中有没有list列表中的关键词
#                     if result1 >= 0:
#                         if result_temp != result1:       #如果每一行文字中有2个关键词以同一位置开始，则不匹配第二个
#                             result_temp = result1
#                             if strs.count(row[3]) == 0:
#                                 strs.append(row[3])
#         except:
#             print("Error: unable to fetch data")
#         result = {}
#         key = 'border'  # 识别出的所有文字的外框坐标
#         result[key] = {}
#         result[key]['top'] = top_min
#         result[key]['left'] = left_min
#         result[key]['down'] = top_max
#         result[key]['right'] = left_max
#         result['results'] = []
#         num = 0
#         # 开始计算位置
#         for i in strs:
#             num1 = len(i)  # 关键词的长度
#             for item in d['words_result']:
#                 strss = item.get('words', 'NA')
#                 result2 = strss.find(i)
#                 if result2 >= 0:
#                     num2 = len(strss)  # 一行文字的长度
#                     if direction == 0:
#                         top = item['location'].get('top') - top_min
#                         left = item['location'].get('left') + (result2 / num2) * item['location'].get(
#                                 'width') - left_min
#                         width = item['location'].get('width') * num1 / num2
#                         height = item['location'].get('height')
#                     elif direction == 1:
#                         top = item['location'].get('top') + (((num2 - result2 - num1)) / num2) * item[
#                                 'location'].get('height') - top_min
#                         left = item['location'].get('left') - left_min
#                         height = item['location'].get('height') * num1 / num2
#                         width = item['location'].get('width')
#                     elif direction == 2:
#                         top = item['location'].get('top') - top_min
#                         left = item['location'].get('left') + ((num2 - result2 - num1) / num2) * item[
#                                 'location'].get(
#                                 'width') - left_min
#                         width = item['location'].get('width') * num1 / num2
#                         height = item['location'].get('height')
#                     elif direction == 3:
#                         top = item['location'].get('top') + (result2 / num2) * item['location'].get(
#                                 'height') - top_min
#                         left = item['location'].get('left') - left_min
#                         height = item['location'].get('height') * num1 / num2
#                         width = item['location'].get('width')
#                     num += 1
#
#                     results = {}
#                     results['words'] = i
#                     results['location'] = {}
#                     results['location']['top'] = top
#                     results['location']['height'] = height
#                     results['location']['left'] = left
#                     results['location']['width'] = width
#                     result['results'].append(results)
#                     break
#         key = 'result_num'
#         result[key] = str(num)
#         key = 'domain_id'
#         result[key] = str(domain1)
#         return HttpResponse(json.dumps(result), content_type="application/json")
def getAllInByTopicNameAndDomainId(request):
    if request.method == "GET":
        name=request.GET["topic"]
        domainid=int(request.GET["domainid"])
        db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        sql = "SELECT domain_name FROM domain \
               WHERE domain_id = %d " % (domainid)         #利用课程id获取课程名称
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            results=str(results[0])                     #获取str格式的课程名
        except:
            print("Error: unable to fetch data")

        domainName = urllib.request.quote(results)
        topicName = urllib.request.quote(name)
        url = 'http://yotta.xjtushilei.com:8083/topic/getCompleteTopicByNameAndDomainName?domainName='+domainName+'&topicName='+topicName
        req=urllib.request.Request(url)
        request=urllib.request.urlopen(req)
        r = request.read().decode('utf-8')
        r = json.loads(r)
        for item in r['data']['children']:
            for items in item["children"]:
                if items.get('facetLayer') == 2:
                    for itemss in items['children']:
                        e = str(itemss.get('assembleContent'))
                        ste = e.replace('\n', ' ')

                        ste = ste.replace('&nbsp', ' ')
                        ste = ste.replace('K&amp', ' ')
                        ste = ste.replace(';', ' ')
                        ste = re.sub(u"\\(.*?\\)|\\<.*?>|\\[.*?]", "", ste)
                        ste = ste.strip()
                        ste = ste[0:20]
                        itemss['assembleContent'] = ste
                else:
                    e = str(items.get('assembleContent'))
                    ste = e.replace('\n', ' ')

                    ste = ste.replace('&nbsp', ' ')
                    ste = ste.replace('K&amp', ' ')
                    ste = ste.replace(';', ' ')
                    ste = re.sub(u"\\(.*?\\)|\\<.*?>|\\[.*?]", "", ste)
                    ste = ste.strip()
                    ste = ste[0:20]
                    items['assembleContent'] = ste
        r=json.dumps(r)
        return HttpResponse(r, content_type="application/json")

def clusterDivided(request):
    db = pymysql.connect("localhost", "root", "123456", "yotta_spring_boot_complete")
    edge = []
    topic = []
    if request.method == "GET":
        domain1 = str(request.GET["domain"])
        print(domain1)

        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT t2.topic_name, t1.topic_name FROM dependency, domain, topic as t1, topic as t2 \
               WHERE dependency.end_topic_id=t1.topic_id and dependency.start_topic_id=t2.topic_id and domain.domain_id=dependency.domain_id and domain.domain_name = '%s' " % (domain1)
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
        except:
            print("Error: unable to fetch data")
        # print("edge:",edge)
        # print("topic",topic)

        # 创建一个空对象
        g = igraph.Graph(directed=True)
        # 添加网络中的点
        g.add_vertices(topic)
        # 添加网络中的边

        g.add_edges(edge)
        # -----------------------其它信息-----------------------------
        # 国家名称
        g.vs['label'] = topic
        # print(g.vs['label'])
        out_num = g.degree(mode='out')  # 得到每个顶点的出度
        in_num = g.degree(mode="in")  # 得到每个顶点的入度
        num = g.degree()  # 得到每个顶点的度
        num1 = []
        for i in num:
            num1.append(i * 10)
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

        # # -----------------------设置参数-----------------------------
        # color_dict={0:'blue',1:'red',2:'green',3:'yellow',4:'pink',5:'black',6:'orange',7:'purple',8:'brown',9:'gray',10:'tan'}
        # # 参数集合。visual_style是一个参数字典，可以动态添加想要个性化设定的参数
        # visual_style = {}
        # # 根据相对面积，设置点的大小
        # visual_style["vertex_size"] = g.vs['daxiao']
        # # # 根据国家实力，设置点的颜色
        # visual_style["vertex_color"] = [color_dict[com] for com in g.vs['com']]
        # # 图尺寸
        # visual_style["bbox"] = (1200, 1200)
        # # 边缘距离
        # visual_style["margin"] = 20
        # # 布局方式
        # visual_style["layout"] = g.layout('fr')
        # # -----------------------画图-----------------------------
        # igraph.plot(g, **visual_style)
        results = {}

        results['communities'] = []
        sum_before = 0
        sum_after = 0
        de = []
        seqe = []
        topic_n = []
        for c, l in community.items():
            G = networkx.DiGraph()
            G.add_nodes_from(l)
            sum = 0  # sum是社团内所有顶点出度和减去入度和的值，sum越大表示整个社团指向其他社团的关系越多，表明此社团越靠前
            edgec = []  # 每个簇内的所有关系列表
            edgecc=[]
            communities = {}
            key = 'commumity' + str(c)
            # print("Community ", c, ": ", l)
            communities[key] = {}
            communities[key]['topic_num'] = len(l)
            topic_n.append(len(l))  # 获取每个簇的主题数目
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
                G.remove_edge(i[0], i[1])
                if networkx.has_path(G, i[0], i[1]) == False:  # 判断去除一条边后G中剩余的边是否有去除的边的2个顶点之间的路径
                    G.add_edge(i[0], i[1])  # 没有路径，则把去掉的边再加回G,否则不加
                    edgecc.append(i)  # edgecc是一个簇内去除三角形边之后的所有边集合
            # print(G.edges)
            sum_before += len(edgec)
            sum_after += len(edgecc)

            # print(edgec)
            communities[key]['edge'] = edgecc
            results['communities'].append(communities)
        # 利用de给所有簇按照sum从大到小排序得到顺序列表seqe
        resultss = {}
        resultss['communities'] = []
        topic_num = []
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
            t = de[0][0]
            seqe.append(t)
            topic_num.append(topic_n[t])
            resultss['communities'].append(results['communities'][t])
            de.remove(de[0])
        # print(seqe)
        resultss['sequence'] = seqe
        resultss['topic_num'] = topic_num
        print(resultss)
        print('sum_before:',sum_before)
        print('sum_after:',sum_after)
        print('totaledgesum:',len(edge))
        return HttpResponse(json.dumps(resultss), content_type="application/json")