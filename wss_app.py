import asyncio
import websockets
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):    # 파일이 변경되었을 때 이벤트를 처리하는 함수.
    def __init__(self, filepath, notify_func, loop):
        self.filepath = filepath
        self.notify_func = notify_func
        self.loop = loop  # 이벤트 루프를 핸들러에 전달합니다.

    def on_modified(self, event):
        if event.src_path == self.filepath:
            # 이벤트 루프에서 coroutine을 안전하게 스케줄링합니다.
            asyncio.run_coroutine_threadsafe(self.notify_func(), self.loop)

async def notify_clients(): # 클라이언트에게 파일 내용을 전송하는 함수
    if clients:
        with open('temp.txt', 'r') as file:
            content = file.read()
        for client in clients:
            await client.send(content)

async def main():
    global clients
    clients = set()
    loop = asyncio.get_running_loop()  # 현재 실행 중인 이벤트 루프를 얻습니다.
    observer = Observer()
    event_handler = FileChangeHandler('./temp.txt', notify_clients, loop)   # temp.txt 파일내용의 변경을 감시합니다.
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    async with websockets.serve(handler, "localhost", 5000):
        await asyncio.Future()  # Run forever

async def handler(websocket, path): # 웹소켓 연결을 처리하는 함수
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

if __name__ == "__main__":
    asyncio.run(main())