# Reflective 프로그래밍을 위한 테스트 함수들을 정의한 파일
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import subprocess

def resp(msg, status="error"):
    return {"data":msg, "status":status}

# test
def func_test(data):    # 파일명을 출력하는 테스트 함수
    return resp("test:"+__file__, status="success")

def func_gitClone(data):
    try:
        cmd = ["sudo", "git", "clone", "https://github.com/dltkdgns00/dltkdgns00", "/home/pi/dltkdgns00"]
        # cmd = ['/usr/bin/git', 'help']
        # cmd = ['ls', '-la']
        response = subprocess.check_output(cmd).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        pass

    return resp(response, status="success")