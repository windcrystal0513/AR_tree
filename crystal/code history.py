# list = ['C语言标准库', '字面常量', '变量', '注释', 'Objective-C', 'GCC', 'Go', 'C标准函式库', 'Fork','函数调用','函数', 'C语言', 'C字串函式库', 'C#', 'C11',
#             'Clang', 'C++', 'C_POSIX_library', 'ANSI_C', '顺序结构', '头文件',  '系统调用',  '指针变量', '指针', '控制语句',
#             '数据类型', '运算符', '表达式', '转义字符', '程序测试', '程序结构', '关键字', '字符编码','字符串','字符', '标识符', '输入输出', '预处理指令', '宏定义', '基本语法', '位运算',
#             'typedef', '位域', '结构体', '循环结构', '选择结构', '共用体', '链表', '进位计数制',  '数组',  '内存管理']

# 第一版以左上角为原点的代码
# def location(request):
#
#     if request.method == "GET":
#         strs = []
#         d = json.loads(request.GET["OCR_result"])
#     # file = open("D:\AR research\\fenci\jieba-master\jieba\\test2.json", encoding='utf-8').read()
#     #     d = json.loads(file)
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
#             result = item.get('words')
#             for index in range(len(list)):
#                 result1 = result.find(list[index])
#                 if result1 >= 0:
#                     if strs.count(list[index]) == 0:
#                         strs.append(list[index])
#         # top1 = d['words_result'][0]['location']['top']
#         # top2 = d['words_result'][line_num - 1]['location']['top'] + \
#         #        d['words_result'][line_num - 1]['location']['height']
#         result = {}
#         key = 'border'
#         result[key] = {}
#         result[key]['top'] = top_min
#         result[key]['left'] = left_min
#         result[key]['down'] = top_max
#         result[key]['right'] = left_max
#         result['results'] = []
#         num = 0
#         top_temp = 0
#         left_temp = 0
#         for i in strs:
#
#             num1 = len(i)
#             for item in d['words_result']:
#                 strss=item.get('words','NA')
#                 result2=strss.find(i)
#                 if result2>=0:
#                     num2=len(strss)
#                     top=item['location'].get('top')-top_min
#                     height=item['location'].get('height')
#                     left=item['location'].get('left')+(result2/num2)*item['location'].get('width')-left_min
#                     width=item['location'].get('width')*num1/num2
#                     if top_temp!=top or round(left_temp)!=round(left):
#                         num += 1
#                         top_temp=top
#                         left_temp=left
#                         results = {}
#                         results['words'] = i
#                         results['location'] = {}
#                         results['location']['top'] = top
#                         results['location']['height'] = height
#                         results['location']['left'] = left
#                         results['location']['width'] = width
#                         result['results'].append(results)
#                         break
#         key = 'result_num'
#         result[key] = str(num)
#         return HttpResponse(json.dumps(result), content_type="application/json")

# 第二版固定2和3两个方向的代码
# def location(request):
#
#     if request.method == "GET":
#         strs = []
#         d = json.loads(request.GET["OCR_result"])
#         w=int(request.GET["width"])
#         h=int(request.GET["height"])
#         line_num = 0
#         if d['direction']==2:
#             left_min = d['words_result'][0]['location']['left']
#             left_max = d['words_result'][0]['location']['left'] + d['words_result'][0]['location']['width']
#             for item in d['words_result']:
#                 line_num += 1
#                 if left_min > item['location']['left']:
#                     left_min = item['location']['left']
#                 if left_max < item['location']['left'] + item['location']['width']:
#                     left_max = item['location']['left'] + item['location']['width']
#                 result3 = item.get('words')
#                 for index in range(len(list)):
#                     result1 = result3.find(list[index])
#                     if result1 >= 0:
#                         if strs.count(list[index]) == 0:
#                             strs.append(list[index])
#             top1 = d['words_result'][0]['location']['top']+d['words_result'][0]['location']['height']
#             top2 = d['words_result'][line_num - 1]['location']['top']
#             result = {}
#             key = 'border'
#             result[key] = {}
#             result[key]['top'] = h-top1
#             result[key]['right'] = w-left_min
#             result[key]['down'] = h-top2
#             result[key]['left'] = w-left_max
#             result['results'] = []
#
#             num = 0
#             top_temp=0
#             left_temp=0
#             for i in strs:
#
#                 num1 = len(i)
#                 for item in d['words_result']:
#                     strss=item.get('words','NA')
#                     result2=strss.find(i)
#                     if result2>=0:
#                         num2=len(strss)
#                         top=h-item['location'].get('top')-item['location'].get('height')
#                         height=item['location'].get('height')
#                         width = item['location'].get('width') * num1 / num2
#                         left=w-item['location'].get('left')-item['location'].get('width')+(result2/num2)*item['location'].get('width')
#                         if top_temp!=top or round(left_temp)!=round(left):
#                             num += 1
#                             top_temp=top
#                             left_temp=left
#                             results = {}
#                             results['words'] = i
#                             results['location'] = {}
#                             results['location']['top'] = top-h+top1
#                             results['location']['height'] = height
#                             results['location']['left'] = left-w+left_max
#                             results['location']['width'] = width
#                             result['results'].append(results)
#                             break
#             key = 'result_num'
#             result[key] = str(num)
#         elif d['direction'] == 3:
#             top_min = d['words_result'][0]['location']['top']
#             top_max = d['words_result'][0]['location']['top'] + d['words_result'][0]['location']['height']
#             for item in d['words_result']:
#                 line_num += 1
#                 if top_min > item['location']['top']:
#                     top_min = item['location']['top']
#                 if top_max < item['location']['top'] + item['location']['height']:
#                     top_max = item['location']['top'] + item['location']['height']
#                 result3 = item.get('words')
#                 for index in range(len(list)):
#                     result1 = result3.find(list[index])
#                     if result1 >= 0:
#                         if strs.count(list[index]) == 0:
#                             strs.append(list[index])
#             left_max = d['words_result'][0]['location']['left'] + d['words_result'][0]['location']['width']
#             left_min = d['words_result'][line_num - 1]['location']['left']
#             result = {}
#             key = 'border'
#             result[key] = {}
#             result[key]['top'] = h - top_max
#             result[key]['right'] = w-left_min
#             result[key]['down'] = h - top_min
#             result[key]['left'] = w-left_max
#             result['results'] = []
#
#             num = 0
#             top_temp = 0
#             left_temp = 0
#             for i in strs:
#
#                 num1 = len(i)
#                 for item in d['words_result']:
#                     strss = item.get('words', 'NA')
#                     result2 = strss.find(i)
#                     if result2 >= 0:
#                         num2 = len(strss)
#                         top = h - item['location'].get('top') - (result2 / num2) *item['location'].get('height')-item['location'].get('height')* num1 / num2
#                         height = item['location'].get('height')* num1 / num2
#                         width = item['location'].get('width')
#                         left = w-item['location'].get('left')-item['location'].get('width')
#                         if left_temp != left or round(top_temp) != round(top+height):
#                             num += 1
#                             top_temp = top+height
#                             left_temp = left
#                             results = {}
#                             results['words'] = i
#                             results['location'] = {}
#                             results['location']['top'] = top - h + top_max
#                             results['location']['height'] = height
#                             results['location']['left'] = left - w+left_max
#                             results['location']['width'] = width
#                             result['results'].append(results)
#                             break
#             key='result_num'
#             result[key]=str(num)
#         # elif d['direction'] == 3:
#         #     top_min = d['words_result'][0]['location']['top']
#         #     top_max = d['words_result'][0]['location']['top'] + d['words_result'][0]['location']['height']
#         #     for item in d['words_result']:
#         #         line_num += 1
#         #         if top_min > item['location']['top']:
#         #             top_min = item['location']['top']
#         #         if top_max < item['location']['top'] + item['location']['height']:
#         #             top_max = item['location']['top'] + item['location']['height']
#         #         result3 = item.get('words')
#         #         for index in range(len(list)):
#         #             result1 = result3.find(list[index])
#         #             if result1 >= 0:
#         #                 if strs.count(list[index]) == 0:
#         #                     strs.append(list[index])
#         #     left_max = d['words_result'][0]['location']['left'] + d['words_result'][0]['location']['width']
#         #     left_min = d['words_result'][line_num - 1]['location']['left']
#         #     result = {}
#         #     key = 'border'
#         #     result[key] = {}
#         #     result[key]['top'] = h - left_max
#         #     result[key]['right'] = top_max
#         #     result[key]['down'] = h - left_min
#         #     result[key]['left'] = top_min
#         #     result['results'] = []
#         #
#         #     num = 0
#         #     top_temp = 0
#         #     left_temp = 0
#         #     for i in strs:
#         #
#         #         num1 = len(i)
#         #         for item in d['words_result']:
#         #             strss = item.get('words', 'NA')
#         #             result2 = strss.find(i)
#         #             if result2 >= 0:
#         #                 num2 = len(strss)
#         #                 top = h - item['location'].get('left') - item['location'].get('width')
#         #                 height = item['location'].get('width')
#         #                 width = item['location'].get('height') * num1 / num2
#         #                 left = item['location'].get('top') + (result2 / num2) * item['location'].get('height')
#         #                 if top_temp != top or round(left_temp) != round(left):
#         #                     num += 1
#         #                     top_temp = top
#         #                     left_temp = round(left)
#         #                     results = {}
#         #                     results['words'] = i
#         #                     results['location'] = {}
#         #                     results['location']['top'] = top - h + left_max
#         #                     results['location']['height'] = height
#         #                     results['location']['left'] = left - top_min
#         #                     results['location']['width'] = width
#         #                     result['results'].append(results)
#         #                     break
#         #     key='result_num'
#         #     result[key]=str(num)
#         return HttpResponse(json.dumps(result), content_type="application/json")


#识别C语言一门课程最终版
# def location(request):
#
#     if request.method == "GET":
#         strs = []
#         d = json.loads(request.GET["OCR_result"])
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
#             result = item.get('words')
#             result_temp=-1           #用来排除头几个字相同的2个长短不一的关键词被同时识别
#             for index in range(len(list)):
#                 result1 = result.find(list[index])    #判断这行话中有没有list列表中的关键词
#                 if result1 >= 0:
#                     if result_temp!=result1:
#                         result_temp=result1
#                         if strs.count(list[index]) == 0:
#                             strs.append(list[index])
#
#         result = {}
#         key = 'border'          #识别出的所有文字的外框坐标
#         result[key] = {}
#         result[key]['top'] = top_min
#         result[key]['left'] = left_min
#         result[key]['down'] = top_max
#         result[key]['right'] = left_max
#         result['results'] = []
#         num = 0
#        #开始计算位置
#         for i in strs:
#
#             num1 = len(i)    #关键词的长度
#             for item in d['words_result']:
#                 strss=item.get('words','NA')
#                 result2=strss.find(i)
#                 if result2>=0:
#                     num2=len(strss)   #一行文字的长度
#                     if direction==0:
#                         top = item['location'].get('top') - top_min
#                         left = item['location'].get('left') + (result2 / num2) * item['location'].get(
#                             'width') - left_min
#                         width = item['location'].get('width') * num1 / num2
#                         height = item['location'].get('height')
#                     elif direction==1:
#                         top = item['location'].get('top') + (((num2-result2-num1)) / num2) * item['location'].get('height') - top_min
#                         left = item['location'].get('left') - left_min
#                         height = item['location'].get('height') * num1 / num2
#                         width = item['location'].get('width')
#                     elif direction==2:
#                         top = item['location'].get('top') - top_min
#                         left = item['location'].get('left') + ((num2-result2-num1)/ num2) * item['location'].get(
#                             'width') - left_min
#                         width = item['location'].get('width') * num1 / num2
#                         height = item['location'].get('height')
#                     elif direction==3:
#                         top = item['location'].get('top') + (result2 / num2) * item['location'].get('height') - top_min
#                         left = item['location'].get('left') - left_min
#                         height = item['location'].get('height') * num1 / num2
#                         width = item['location'].get('width')
#
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
#         return HttpResponse(json.dumps(result), content_type="application/json")



#识别C语言一门课程最终版
# def getAllInByTopicName(request):
#     if request.method == "GET":
#         name=request.GET["topic"]
#         domainName = urllib.request.quote("C语言")
#         topicName = urllib.request.quote(name)
#         url = "http://yotta.xjtushilei.com:8083/topic/getCompleteTopicByNameAndDomainName?domainName="+domainName+"&topicName="+topicName
#         req = urllib.request.Request(url)
#         request=urllib.request.urlopen(req)
#         r = request.read().decode('utf-8')
#         r = json.loads(r)
#         for item in r['data']['children']:
#             for items in item["children"]:
#                 if items.get('facetLayer') == 2:
#                     for itemss in items['children']:
#                         e = str(itemss.get('assembleContent'))
#                         ste = e.replace('\n', ' ')
#
#                         ste = ste.replace('&nbsp', ' ')
#                         ste = ste.replace('K&amp', ' ')
#                         ste = ste.replace(';', ' ')
#                         ste = re.sub(u"\\(.*?\\)|\\<.*?>|\\[.*?]", "", ste)
#                         ste = ste.strip()
#                         ste = ste[0:20]
#                         itemss['assembleContent'] = ste
#                 else:
#                     e = str(items.get('assembleContent'))
#                     ste = e.replace('\n', ' ')
#
#                     ste = ste.replace('&nbsp', ' ')
#                     ste = ste.replace('K&amp', ' ')
#                     ste = ste.replace(';', ' ')
#                     ste = re.sub(u"\\(.*?\\)|\\<.*?>|\\[.*?]", "", ste)
#                     ste = ste.strip()
#                     ste = ste[0:20]
#                     items['assembleContent'] = ste
#         r=json.dumps(r)
#
#         return HttpResponse(r, content_type="application/json")