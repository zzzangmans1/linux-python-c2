# 파일 전송 클라이언트
from socket import *
import os, sys, argparse, subprocess

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='python3 cfile.py -file=[file name]')
    
    # 입력받을 인자값 등록 required 필수면 True
    parser.add_argument('-file',required=True, help='-file=파일 이름을 입력해주세요')

    # 입력 받은 인자값을 args에 저장
    args = parser.parse_args()

    filename = args.file
    
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('127.0.0.1', 4040))

    print('연결에 성공했습니다.')
    clientSock.sendall(filename.encode('utf-8'))

    data = clientSock.recv(1024)
    data_transferred = 0

    if not data:
        print('파일 %s 가 서버에 존재하지 않음' %filename)
        sys.exit()

    nowdir = os.getcwd()
    with open(nowdir+"\\"+filename, 'wb') as f: #현재dir에 filename으로 파일을 받는다
        try:
            while data: #데이터가 있을 때까지
                f.write(data) #1024바이트 쓴다
                data_transferred += len(data)
                data = clientSock.recv(1024) #1024바이트를 받아 온다
        except Exception as ex:
            print(ex)
    print('파일 %s 받기 완료. 전송량 %d' %(filename, data_transferred))
    subprocess.Popen('eog '+ filename, shell=True)
