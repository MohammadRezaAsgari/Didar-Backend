from collections import OrderedDict

from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from utils.api.responses import success_response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 50
    available_filters = {}

    def get_available_filters(self):
        return self.available_filters

    def get_paginated_response(self, data):
        return success_response(
            data=OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("available_filters", self.get_available_filters()),
                ]
            ),
            status_code=status.HTTP_200_OK,
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{offset_param}=400&{limit_param}=100".format(
                        offset_param=self.offset_query_param, limit_param=self.limit_query_param
                    ),
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{offset_param}=200&{limit_param}=100".format(
                        offset_param=self.offset_query_param, limit_param=self.limit_query_param
                    ),
                },
                "results": schema,
                "available_filters": {
                    "type": "object",
                    "nullable": True,
                    "example": self.available_filters,
                },
            },
        }
