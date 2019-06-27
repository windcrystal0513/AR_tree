# -*- coding: utf-8 -*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'AR_tree.settings'
import json

from collections import OrderedDict

from openapi_codec import OpenAPICodec
from openapi_codec.encode import generate_swagger_object
from coreapi.compat import force_bytes

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator

from rest_framework_swagger.renderers import (
    SwaggerUIRenderer,
    OpenAPIRenderer
)

from AR_tree.swagger  import path_dict

class SwaggerSchemaView(APIView):
    renderer_classes = [
        OpenAPIRenderer,
        SwaggerUIRenderer
    ]

    def load_swagger_json(self, doc):
        """
        加载自定义swagger.json文档
        """
        data = generate_swagger_object(doc)

        # data['paths'].update(path_dict.pop('paths'))
        # data.update(path_dict)
        data['paths'] = path_dict
        return OpenAPICodec().decode(force_bytes(json.dumps(data)))

    def get(self, request):
        generator = SchemaGenerator(title='AR_tree的API',
                                    urlconf='AR_tree.urls')
        schema = generator.get_schema(request=request)
        document = self.load_swagger_json(schema)

        return Response(document)
