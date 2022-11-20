# 파일 전송 클라이언트
from socket import *
import sys, argparse, subprocess

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='python3 cfile.py -f [file name] -i [ip]')
    
    # 입력받을 인자값 등록 required 필수면 True
    parser.add_argument('-f',required=True, help='-f 파일 이름을 입력해주세요')
    parser.add_argument('-i',required=True, help='-i 접속할 아이피를 입력해주세요')

    # 입력 받은 인자값을 args에 저장
    args = parser.parse_args()

    filename = args.f # 서버에서 읽을 파일이름
    ip = args.i
    
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect((ip, 4040))

    print('파일 이름 : ',filename)
    print('연결에 성공했습니다.')
    clientSock.sendall(filename.encode('utf-8'))

    data = clientSock.recv(1024)
    data_transferred = 0
    if not data:
        print('파일 %s 가 서버에 존재하지 않음' %filename)
        sys.exit()
    
    filename = 'screen1.png' # 저장할 파일이름
    with open(filename, 'wb') as f: #현재dir에 filename으로 파일을 받는다
        try:
            while data: #데이터가 있을 때까지
                f.write(data) #1024바이트 쓴다
                data_transferred += len(data)
                data = clientSock.recv(1024) #1024바이트를 받아 온다
        except Exception as ex:
            print(ex)
    filename = 'eog ' + filename
    print('파일 %s 받기 완료. 전송량 %d' %(filename, data_transferred))
    subprocess.run(filename, shell=True)
