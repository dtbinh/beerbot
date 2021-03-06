# -*- coding: utf-8 -*-
"""

"""
import time
import numpy as np
#from Camera import Camera
from Beerbot import Beerbot


class Control:
    def __init__(self, port, baudrate, camera):
        self.camera = camera
        self.robot = Beerbot()
        print ('Program started')
        self.robot.connect(port,baudrate)
        
        
        #if self.clientID!=-1:
        #    print "Conexion establecida"
        #else:
        #    print "Conexion con el simulador fallida, reinicia el simulador"
        #error,self.motorFL=vrep.simxGetObjectHandle(self.clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
        #error,self.motorFR=vrep.simxGetObjectHandle(self.clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
        #error,self.camera=vrep.simxGetObjectHandle(self.clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)
        #error,self.robot=vrep.simxGetObjectHandle(self.clientID,'Pioneer_p3dx',vrep.simx_opmode_oneshot_wait)

    def getRobotPosition(self):
        "get the position of the robot"
        x = self.camera.robot[0][0]
        y = self.camera.robot[0][1]
        #time.sleep(0.1)
        return x, y

    def getRobotOrientation(self):
        "get the orientation of the robot"
        orientation = self.camera.robot[1]
                
        return orientation*180/3.14159265

    def printRobotLocation(self):
        "print the position and orientation of the robot (x, y, yaw)"
        x = self.camera.robot[0][0]
        y = self.camera.robot[0][1]
        yaw = self.camera.robot[1]
        print "Position: (", x,",", y, ")", "\nYaw:", yaw*180/3.14159265
            
    def getDistanceToTarget (self, x_target, y_target):
        "gets the distance from the robot to a given target"
        x_robot, y_robot = self.getRobotPosition()
        return np.sqrt((x_target-x_robot)**2+(y_target-y_robot)**2)

    def getDifferenceToTargetAngle (self, angle):
        "Gets the difference between the actual orientation and a given orientation"
        difference = angle-self.getRobotOrientation()
        if difference < -180:
            difference+=360
        elif difference > 180:
            difference-=360
        return difference

    def getTargetAngle (self, x_target, y_target):
        "Gets the angle to a point target"
        x_robot, y_robot = self.getRobotPosition()

        x_gap=x_target-x_robot
        y_gap=y_target-y_robot
        l_gap=np.sqrt(x_gap**2+y_gap**2)

        angle=np.arccos(x_gap/l_gap)*180/3.14159265
        if y_gap < 0:
            angle=-angle
        return angle*-1

    def turnToTargetAngle (self, target_angle):
        "Orientates robot to a given angle in the range from -180 to 180"
        while np.abs(self.getDifferenceToTargetAngle(target_angle)) > 5:
            self.camera.process_image()
            amp = self.getDifferenceToTargetAngle(target_angle)
            left_motor=-amp/140
            right_motor=amp/140
            self.robot.move(left_motor,right_motor)
            time.sleep(0.2)            
            print "Angulo actual: ", self.getRobotOrientation()
            print "diferencia: ", amp
        self.robot.move(0,0)
        return 0

    def goToTarget (self, target_x,target_y): # funcion muerta, no usar
        while(self.getDistanceToTarget(target_x, target_y)>0.10):
            self.turnToTargetAngle (self.getTargetAngle(target_x,target_y))
            self.robot.move(0.5,0.5)
            time.sleep(0.2)
            print self.getDistanceToTarget(target_x, target_y)

        print "punto!"
        self.robot.move(0,0)

if __name__ == "__main__":
    import time as t
    from Camera import Camera2
 
    camera = Camera2(1, './CameraCalibration/logitech/calibration_image.npz')
    controller = Control("/dev/rfcomm0", 19200, camera) 
    
    camera.process_image()
        
    #controller.turnToTargetAngle(-90)
        
    controller.printRobotLocation()  

    print "distancia a 90" , controller.getDifferenceToTargetAngle(90)      
    print "distancia a 90" , controller.getDifferenceToTargetAngle(90)      
     
    controller.turnToTargetAngle(-170)     
     
    controller.robot.move(0,0)
    controller.robot.move(0,0)
    controller.robot.move(0,0)
    controller.robot.move(0,0)
    controller.robot.move(0,0)
    controller.robot.move(0,0)
 
 
   
       
    #beerbot.disconnect()
    print "done!"
