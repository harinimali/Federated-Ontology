import json
from flask import jsonify
from common.globalconst import *


def json_encode(json_dict=None):
    assert isinstance(json_dict, dict)
    return json.dumps(json_dict)


def json_encode_flask(json_dict=None):
    assert isinstance(json_dict, dict)
    return jsonify(json_dict)


def json_decode(json_str=None):
    assert isinstance(json_str, str)
    return json.loads(json_str)


def respond_json(status_code, **kw):
    myjson = kw
    if status_code == INT_OK:
        myjson['status'] = 'ok'
    elif status_code == INT_QUERY_FAILURE:
        myjson['status'] = 'error'
        myjson['message'] = 'error while querying apache jena api'
    else:
        myjson['status'] = 'error'
        myjson['message'] = 'error'
    myjson['code'] = status_code
    return json_encode_flask(myjson)
