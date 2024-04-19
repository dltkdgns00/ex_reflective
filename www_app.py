#wsgi_ai.py
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import importlib
import json
import glob
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
from cgi import FieldStorage, parse_header, parse_multipart
import subprocess

def call_function(function_name, function_data):   # 함수 이름과 데이터를 받아서 함수를 호출하고 결과를 반환하는 함수 (Reflective 프로그래밍)
    files = glob.glob("./s0*_*.py")[::-1]   # 파일 목록을 역순으로 정렬

    for file in files:  # 파일 목록을 순회하며
        base_name = os.path.basename(file)
        module_name = base_name.split('.')[0]

        # Import the module
        module = importlib.import_module(module_name)
        # Reload to get the latest version
        module = importlib.reload(module)

        # Check if the module has the desired function
        function_scv_name = "func_"+function_name   # 함수 이름을 func_로 시작하는 형태로 변환
        if not hasattr(module, function_scv_name): continue

        try:
            function = getattr(module, function_scv_name)   # 함수를 가져옴
            return function(function_data)
        except AttributeError as e:
            pass
    # If the function is not found in any of the modules, return None
    return {"data":f"[{function_name}] not defined", "status":"fail"}   # 함수를 찾지 못하면 실패 메시지를 반환

def parse_post_data(environ):   # POST 요청 데이터를 파싱하는 함수
    content_type = environ.get('CONTENT_TYPE', '')
    if content_type.startswith('multipart/form-data'):
        form = FieldStorage(fp=environ['wsgi.input'], environ=environ)
        return {field: form[field].value for field in form.keys()}
    else:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            parsed_data = parse_qs(request_body)
            return {field.decode("utf-8"): parsed_data[field][0].decode("utf-8") for field in parsed_data.keys()}
        except (ValueError, TypeError):
            return {}

def parse_get_data(environ):    # GET 요청 데이터를 파싱하는 함수
    parsed_data = parse_qs(environ['QUERY_STRING'])
    return {field: parsed_data[field][0] for field in parsed_data.keys()}

def application(environ, start_response):   # WSGI 애플리케이션
    data = parse_post_data(environ) if environ['REQUEST_METHOD'].upper() == 'POST' else parse_get_data(environ)

    func = data.get('func', '')
    if func:
        response = call_function(func, data)
    else:
        response = {"data": "AnHive's Roaster Controller Prototype!", "status": "success"}

    output = bytes(json.dumps(response), "utf-8")
    response_headers = [('Content-type', 'application/json'),
                        ('Content-Length', str(len(output)))]
    start_response('200 OK', response_headers)
    return [output]


if __name__ == "__main__":
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()
