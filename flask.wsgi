# 아파치에서 플라스크를 실행하기 위한 WSGI 파일입니다.
import sys
sys.path.insert(0, '/path/to/cloned/repo')
from flask_app import app as application
