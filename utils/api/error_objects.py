from enum import Enum


class ErrorObject(dict, Enum):
    # General
    UN_AUTH = {'code': 1001, 'msg': 'UN_AUTH'}
    BAD_REQUEST = {'code': 1002, 'msg': 'BAD_REQUEST'}
    FORBIDDEN = {'code': 1003, 'msg': 'FORBIDDEN'}
    NOT_FOUND = {'code': 1004, 'msg': 'NOT_FOUND'}
    INVALID_METHOD = {'code': 1005, 'msg': 'METHOD_NOT_ALLOWED'}
    NOT_ACCEPTABLE = {'code': 1006, 'msg': 'NOT_ACCEPTABLE'}
    INVALID_PASSWORD = {'code': 1007, 'msg': 'INVALID_PASSWORD'}
    INVALID_TOKEN = {'code': 1008, 'msg': 'INVALID_TOKEN'}
    SERVER_ERROR = {'code': 1009, 'msg': 'SERVER_ERROR'}
    # User app
    USER_ALREADY_EXISTS = {'code': 1101, 'msg': 'USER_ALREADY_EXISTS'}
    USER_NOT_ACTIVE = {'code': 1102, 'msg': 'USER_NOT_ACTIVE'}
    USER_NOT_FOUND = {'code': 1103, 'msg': 'USER_NOT_FOUND'}
    USER_NOT_SET_PASSWORD = {'code': 1104, 'msg': 'USER_NOT_SET_PASSWORD'}
    INSTRUCTOR_NOT_EXISTS = {'code': 1105, 'msg': 'INSTRUCTOR_NOT_EXISTS'}
    # Schedule app
    SCHEDULE_NOT_EXISTS = {'code': 2001, 'msg': 'SCHEDULE_NOT_EXISTS'}
