#!/home/keras/miniconda3/envs/leap3/bin/python3
import socket
import signal
import sys
import subprocess
import logging
# import serial
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)

class LeapServer:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.ip = socket.gethostbyname(self.host)
        self.port = 3000

        self.s.bind((self.ip, self.port))
        self.s.listen(5)

        # self.serial = serial.Serial('/dev/ttyACM0',9600)
        # self.serial.timeout = 1

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    
    def handler(self, signum, frame):
        sys.stdout.flush()
        logging.info("SERVER SHUTDOWN")
        self.s.close()
        exit(0)

    def close_server(self, signum, frame):
        logging.info("SERVER SHUTDOWN")
        self.c.send("DISCONNECTED".encode('utf-8'))
        self.c.close()
        exit(0)
    
    def run(self):
        subprocess.call('clear', shell=True)
        logging.info(f"Server Started")
        logging.info(f"Local IP: 127.0.0.1:{self.port}")
        logging.info(f"Network IP: {self.get_ip()}:{self.port}")
        flag = 0
        while True:
            signal.signal(signal.SIGINT, self.handler)
            self.c, self.addr = self.s.accept()
            logging.info(f"Client Connection: ({self.addr[0]},{self.addr[1]})")

            flag = 0
            while True:
                if flag:
                    break

                data = self.c.recv(7)
                msg = data.decode('utf-8')
                if msg == '':
                    self.c.close()
                    flag = 1
                    break
                # self.serial.write(msg.encode('utf-8'))
                # time.sleep(0.5)
                logging.info(msg)
                signal.signal(signal.SIGINT, self.close_server)

                
if __name__ == "__main__":
    server = LeapServer()
    server.run()