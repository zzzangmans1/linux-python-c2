import socket, threading

def binder(cScoket, cAddr):
    try:
        while True:
            data = cScoket.recv(1024)
            msg = data.decode()
            print(cAddr," : ", msg)

            msg = input("input command>> ")
            if msg == 'exit':
                break
            data = msg.encode()
            cSocket.send(data)

    except socket.error as erm:
        print("클라이언트와 접속 종료", erm)
    finally:
        print(cAddr, '과의 접속이 정상 종료되었습니다.')
        cScoket.close()

if __name__ == '__main__' :
    # 소켓 생성
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.bind(('', 4444))
    sSocket.listen()
    print('서버가 시작하였습니다.')
    try:
        while True:
            cSocket, cAddr = sSocket.accept()
            th = threading.Thread(target=binder, args= (cSocket, cAddr))
            th.start()
    except:
        print('서버가 종료되었습니다.')
    finally:
        sSocket.close()
