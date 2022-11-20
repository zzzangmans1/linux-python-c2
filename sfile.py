# 파일 전송 서버
from socket import *
import os, sys

if __name__ == '__main__' :
    
    sSocket = socket(AF_INET, SOCK_STREAM)
    sSocket.bind(('', 4040))
    sSocket.listen(1)
    print('서버에서 파일 받을 준비 완료되었습니다.')
    connectionSock, addr = sSocket.accept()

    print(str(addr),'에서 접속했습니다')

    filename = connectionSock.recv(1024) #클라이언트한테 파일이름(이진 바이트 스트림 형태)을 전달 받는다
    print('받은 데이터 : ', filename.decode('utf-8')) #파일 이름을 일반 문자열로 변환한다
    data_transferred = 0

    if not os.path.exists(filename):
        print("no file")
        sys.exit()
    filename[0] = '2'
    print("파일 %s 전송 시작" %filename)
    with open(filename, 'rb') as f:
        try:
            data = f.read(1024) #1024바이트 읽는다
            while data: #데이터가 없을 때까지
                data_transferred += connectionSock.send(data) #1024바이트 보내고 크기 저장
                data = f.read(1024) #1024바이트 읽음
        except Exception as ex:
            print(ex)
    print("전송완료 %s, 전송량 %d" %(filename, data_transferred))
    
