#!/home/keras/miniconda3/envs/leap/bin/python2.7
import Leap
import sys
import socket
import logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)

class LeapMotionListen(Leap.Listener):
    def on_init(self, controller):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = raw_input("Enter server IP: ")
        self.port = 3000
        logging.info("Socket Initialized")

    def on_connect(self, controller):
        try:
            self.c.connect((self.ip, self.port))
        except:
            logging.info("Server not running")
            exit(0)
        logging.info("Connected to server at port %s" % (self.port))

    def on_disconnect(self, controller):
        logging.critical("Disconnected")

    def on_exit(self, controller):
        self.c.close()
        logging.info("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        state = 0
        hand = frame.hands.frontmost
        arm = hand.arm
        wrist_y = arm.wrist_position.y

        front_y = frame.pointables.frontmost.tip_position.y
        left_y = frame.pointables.leftmost.tip_position.y
        right_y = frame.pointables.rightmost.tip_position.y

        aclr = 255 - int(((wrist_y-150)/200)*255) if (wrist_y >=
                                                      150 and wrist_y <= 350) else 0
        if (len(str(aclr)) == 1):
            aclr = '00' + str(aclr)
        if (len(str(aclr)) == 2):
            aclr = '0' + str(aclr)

        if (wrist_y-front_y > 60):
            state = 1
        elif (wrist_y-front_y < -60):
            state = 2
        elif (left_y-right_y < -50):
            state = 3
        elif (left_y-right_y > 50):
            state = 4
        else:
            state = 0

        msg = 'S'+str(state)+'A'+str(aclr) + ";"
        try:
            self.c.send(msg.encode('utf-8'))
        except:
            self.c.close()


def main():
    listener = LeapMotionListen()
    controller = Leap.Controller()
    controller.add_listener(listener)
    logging.info("Press Enter to quit")

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
