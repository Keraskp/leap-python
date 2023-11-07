#!/home/keras/miniconda3/envs/leap/bin/python2.7
import Leap
import sys
import socket
import logging
import subprocess
import numpy as np
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)


class LeapMotionListen(Leap.Listener):
    def on_init(self, controller):
        subprocess.call('clear', shell=True)
        logging.info("Socket Initialized")
        self.columns = ['hands',
                        'fingers',
                        'R_hand',
                        'R_palmpos_x',
                        'R_palmpos_y',
                        'R_palmpos_z',
                        'R_palmvel_x',
                        'R_palmvel_y',
                        'R_palmvel_z',
                        'R_pitch',
                        'R_roll',
                        'R_yaw',
                        'R_arm_dir_x',
                        'R_arm_dir_y',
                        'R_arm_dir_z',
                        'R_wristpos_x',
                        'R_wristpos_y',
                        'R_wristpos_z',
                        'L_hand',
                        'L_palmpos_x',
                        'L_palmpos_y',
                        'L_palmpos_z',
                        'L_palmvel_x',
                        'L_palmvel_y',
                        'L_palmvel_z',
                        'L_pitch',
                        'L_roll',
                        'L_yaw',
                        'L_arm_dir_x',
                        'L_arm_dir_y',
                        'L_arm_dir_z',
                        'L_wristpos_x',
                        'L_wristpos_y',
                        'L_wristpos_z',
                        'gesture']

        self.gesture = 4
        self.gestures = {0: 'idle', 1: 'forward',
                         2: 'backward', 3: 'left', 4: 'right', 5: 'stop'}
        self.RAD_TO_DEG = 57.2957801819
        self.data = []

    def on_connect(self, controller):
        pass

    def on_disconnect(self, controller):
        logging.critical("Disconnected")

    def on_exit(self, controller):
        self.data = np.asarray(self.data)
        df = pd.DataFrame(data=self.data, columns=self.columns)
        # df.to_csv('dataset.csv', mode='a', index=False, header=False)
        df.to_csv('leap_data.csv', index=False, header=False, mode='a')
        # print(df)
        # print(self.data)
        logging.info("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        frame_data = [len(frame.hands), len(frame.fingers)]

        right_data = [0] * 16
        left_data = [0] * 16

        for hand in frame.hands:
            hand_data = self.get_hand_data(hand)
            if hand.is_right:
                right_data = hand_data
            else:
                left_data = hand_data

        frame_data.extend(right_data)
        frame_data.extend(left_data)
        frame_data.append(self.gesture)
        self.data.append(frame_data)

    def get_hand_data(self, hand):
        hand_data = [1,
                     hand.direction.pitch * self.RAD_TO_DEG,
                     hand.palm_normal.roll * self.RAD_TO_DEG,
                     hand.direction.yaw * self.RAD_TO_DEG,
                     hand.palm_position.x,
                     hand.palm_position.y,
                     hand.palm_position.z,
                     hand.palm_velocity.x,
                     hand.palm_velocity.y,
                     hand.palm_velocity.z,
                     hand.arm.direction.x,
                     hand.arm.direction.y,
                     hand.arm.direction.z,
                     hand.arm.wrist_position.x,
                     hand.arm.wrist_position.y,
                     hand.arm.wrist_position.z]
        return hand_data


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
