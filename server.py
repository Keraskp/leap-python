#!/home/keras/miniconda3/envs/leap3/bin/python3
import socket, signal, sys
# import serial
import time
import subprocess


s = socket.socket()	
host = 'localhost'
ip=socket.gethostbyname(host)	
Move = {'0':'Idle','1':'Forward','2':'Backward', '3':'Left', 
            '4':'Right', '5': 'Anti-Clockwise', '6':'Clockwise'}
port = 3000

# serialcomm = serial.Serial('/dev/ttyACM0',9600)
# serialcomm.timeout = 1

s.bind((ip, port))


s.listen(5)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def handler(signum,frame):
    sys.stdout.flush()
    print("\nSERVER SHUTDOWN")
    s.close()
    exit(0)

def close_server(signum,frame):
    print("\nSERVER SHUTDOWN")
    c.send("1".encode('utf-8'))
    c.close()
    exit(0)

subprocess.call('clear', shell=True)
print("SERVER STARTED".center(50,'-'))
print("\nserver ip: %s  port: %s" %(get_ip(),port))

flag = 0

while True:

    signal.signal(signal.SIGINT, handler)
    c, addr = s.accept()	
    print ('client connected with address: ', addr )
    flag = 0
    
    full_msg = ''
    while True:
        if flag:
            break

        data = c.recv(7) #Buffer of size 1 byte is used to recieve filter excess data in buffer.
        msg=data.decode('utf-8')
        if(msg==''):
            c.close()
            flag = 1
            break
        # serialcomm.write(msg.encode('utf-8'))
        # time.sleep(0.5)
        print(msg)
        signal.signal(signal.SIGINT, close_server)
     


     ################I
