# coding=utf8
from crystal.views import judgeDomainAndGetLocation, getAllInByTopicNameAndDomainId,clusterDivided

crystal_path = {
    "/crystal/judgeDomainAndGetLocation/": {
        "get": {
            "description": '''判断一段文本中是否含有课程名，有则返回，无则返回关键词及位置\n
                        示例:
                        q:

                            {
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
                                "words": "数据结构"
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
                                "words": "算法"
                                },
                                {
                                "location": {
                                    "width": 126,
                                    "top": 107,
                                    "left": 218,
                                    "height": 33
                                },
                                "words": "这是C语言的"
                                }
                            ]
                            }

                        ''',
            "tags": [
                "AR_tree"
            ],
            "consumes": [
                "application/json"
            ],
            "responses": {
                "200": {
                    "description": "OK"
                }
            },
            "parameters": [
                {
                    "description": "OCR结果",
                    "required": True,
                    "name": "OCR_result",
                    "type": "object",
                }
            ],
            "operationId": "location"
        }
    },
    "/crystal/get_AllInByTopicNameAndDomainId/": {
        "get": {
            "description": '''利用课程id及主题返回主题下所有分面及碎片\n
                        示例:
                        q:
                           函数
                           412 
                        ''',
            "tags": [
                "AR_tree"
            ],
            "responses": {
                "200": {
                    "description": "OK"
                }
            },
            "parameters": [
                {
                    "description": "topic",
                    "required": True,
                    "name": "topic",
                    "type": "object",
                },
                {
                    "description": "domainid",
                    "required": True,
                    "name": "domainid",
                    "type": "object",
                }
            ],
            "operationId": "getAllInByTopicNameAndDomainId"
        }
    },
     "/crystal/clusterDivided/": {
        "get": {
            "description": '''给定课程名将主题划分成不同簇并得到簇之间与簇内的认知关系\n
                        示例:
                        q:
                           数据结构
                        ''',
            "tags": [
                "AR_tree"
            ],
            "responses": {
                "200": {
                    "description": "OK"
                }
            },
            "parameters": [
                {
                    "description": "domain",
                    "required": True,
                    "name": "domain",
                    "type": "object",
                }
            ],
            "operationId": "clusterDivided"
        }
    }

}

path_dict = {}
path_dict.update(crystal_path)
