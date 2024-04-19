# flask로 작성한 웹 서버와 wsgi로 직접 작성한 웹 서버의 속도를 비교하기 위한 벤치마크 코드
import requests
import time

def benchmark(url, data):
  for _ in range(5):
    # 요청 시작 전 시간을 기록
    start_time = time.time()

    # URL로 HTTP POST 요청 보내기, `data`는 전송할 데이터
    response = requests.post(url, data=data)

    # 요청이 끝난 후의 시간을 기록
    end_time = time.time()

    # 응답 시간을 계산
    elapsed_time = end_time - start_time

    # 응답 시간과 함께 결과 출력
    print(f"POST request to {url} took {elapsed_time:.3f} seconds")
    print(f"HTTP Status Code: {response.status_code}")

# 함수 호출 예시
url = "http://localhost/www"
data = {'func': 'test'}  # POST 요청으로 보낼 데이터
benchmark(url, data)
