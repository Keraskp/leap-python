#!/home/keras/miniconda3/envs/leap/bin/python2.7
import Leap, sys, time, socket

# Create Socket
# c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# port = 12345
# print("Enter the IP address of the server: ")
# ip=raw_input()
# try:
#     c.connect((ip,port))
# except:
#     print("Server not running")
#     exit(0)
# print("Connected to port %s" %(port))

State = 0

class LeapMotionListen(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names=['STATE_INVALID','STATE_START','STATE_UPDATE','STATE_END']
    
    def on_init(self,controller):
        print("Initialized")

    def on_connect(self,controller):
        print("Connected")

    def on_disconnect(self,controller):
        print("Disconnected")

    def on_exit(self,controller):
        print("Exited")

    def on_frame(self,controller):
        pass
    
    def on_frame(self, controller): 
        frame = controller.frame()   
        
        hand = frame.hands.frontmost
        arm = hand.arm
        wrist_y = arm.wrist_position.y

        front_y = frame.pointables.frontmost.tip_position.y
        left_y = frame.pointables.leftmost.tip_position.y 
        right_y = frame.pointables.rightmost.tip_position.y
        
        aclr = 0 #0 - 255
        aclr = 255 - int(((wrist_y-150)/200)*255) if (wrist_y>=150 and wrist_y<=350) else 0
        if_idle = 1
        if(len(str(aclr))==1):
            aclr = '00' + str(aclr)
        if(len(str(aclr))==2):
            aclr = '0' + str(aclr)
        
        if(wrist_y-front_y>60):
            if_idle = 0
            State = 1
            #c.send('1'.encode('utf-8'))
            # print(Move[1])

        elif(wrist_y-front_y<-60):
            if_idle = 0
            State = 2
            # c.send('2'.encode('utf-8'))
            # print(Move[2])

        elif(left_y-right_y<-50):
            if_idle = 0
            State = 3
            #c.send('3'.encode('utf-8'))
            # print(Move[3])

        elif(left_y-right_y>50):
            if_idle = 0
            State = 4
            #c.send('4'.encode('utf-8'))
            # print(Move[4])
        else :
            State = 0 
        
        Msg = 'S'+str(State)+'A'+str(aclr)+ ";"
        # c.send(Msg.encode('utf-8'))
        print(Msg)
       
    
def Main():
    listener = LeapMotionListen()
    controller = Leap.Controller() 
    controller.add_listener(listener)
    print("Press Enter to quit")
    
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    Main()



####################### DOCUMENTATION ##########################

'''
Useless APIs :
frame.fingers 
frame.finger
frame.pointable
frame.pointales
frame.hands
frame.hands.frontmost.arm
'''

'''
Usesful APIs:
frame.pointable[i].tip_position
'''

'''
 APIs under frame :
'current_frames_per_second', 
'deserialize', 
'finger', 
'fingers', 
'gesture', 
'gestures', 
'hand', 
'hands', 
'id',
'images',
'interaction_box', 
'invalid', 
'is_valid', 
'pointable', 
'pointables', 
'rotation_angle', 
'rotation_axis', 
'rotation_matrix', 
'rotation_probability', 
'scale_factor', 
'scale_probability', 
'serialize', 
'serialize_length', 
'this', 
'timestamp', 
'tool', 
'tools', 
'tracked_quad', 
'translation', 
'translation_probability'
'''

'''
Type of finger
            0 = TYPE_THUMB
            1 = TYPE_INDEX
            2 = TYPE_MIDDLE
            3 = TYPE_RING
            4 = TYPE_PINKY
'''

#############################################################