import ThunderBorg3
from Adafruit_BNO055 import BNO055
import atexit
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class Motion:
    def __init__(self,robot):
        self.robot=robot
        self.robot.front=1 # used for determining which side of the robot is considered the front, intended for use with a controller. 0 is considered the side which the camera is on.
        self.leftSpeed=0
        self.rightSpeed=0
    def forward(self,leftSpeed,rightSpeed=None):
        if rightSpeed is None:
            rightSpeed=leftSpeed
        if not self.reverse:
			self.robot.thunderborg.ZB.SetMotor1(speed1)
			self.robot.thunderborg.ZB.SetMotor2(-speed2)
			self.rightSpeed = speed2
			self.leftSpeed = speed1
		else:
			self.robot.thunderborg.ZB.SetMotor1(-speed2)
			self.robot.thunderborg.ZB.SetMotor2(speed1)
			self.rightSpeed = speed1
			self.leftSpeed = speed2

    def incrementSpeed(self,IncL,IncR): #relativly change the motor speeds
		self.rightSpeed += IncR
		self.leftSpeed += IncL
		self.forward(self.leftSpeed,self.rightSpeed)

    def stop(self):
        self.softStop(0.5) # makes the default stopping method the soft stop method to prevent flipping/damaging the robot, etc

    def softStop(self,timeToStop=0.5):
        DecL = (self.leftSpeed/100) * -1
		DecR = (self.rightSpeed/100) * -1
		for i in range(100): # slows down the speed to 0 within the specified time in increments of 100
			self.incrementSpeed(DecL, DecR)
			time.sleep(timeTo/100)


    def hardStop(self):
        self.forward(0,0) # please try to use stop() or softStor() unless hardStop offers a competitive advantage


    def toggleFront(self): # flips the front of the robot to the other end
        self.robot.front^=1

    def changeFront(self,front): # absolutly sets the front of the robot, can either take in a boolean variable, or a string which contains 'camera' or 'attachment'
        if "camera" in front.lower() or front==0:
            self.robot.front=0
        elif "attachment" in front.lower() or front==1:
            self.robot.front=1

    def getFront(self): # returns a string representation of which side the robot is on, to access a boolean representation, use robot.front
        if self.robot.front:
            return "Camera-side"
        return "Attachment-side"


class Controller:
    def __init__(self,robot):
        self.robot=robot
        for i in range(100): # connecting is unreliable, so when initiating the controller it attempts up to 100 connections
            try:
                self.xbox=xbox.Joystick()
                return
            except:
                time.sleep(0.5)
        raise RuntimeError("Unable to connect to XBox controller after 100 attempts")

    def close(self):
        self.xbox.close()


class Compass:
    def __init__(self,robot):
        self.robot=robot
        self.started=False # prevents fron trying to start the compass several times which would raise an error

    def start(self):
        if not self.started:
            connected=False # allows multiple attempts at connecting as initialization has a suboptimal success rate
            self.bno=BNO055.BNO055(serial_port='/dev/serial0')
            for i in range(10):
				try:
					if not self.bno.begin():
						raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
					else:
						connected = True
						break
				except RuntimeError:
					pass
            if not connected:
                raise RuntimeError("Compass not found after 10 attempts")
            self.SetValues([240, 255, 216, 255, 240, 255, 222, 246, 167, 3, 91, 241, 254, 255, 254, 255, 255, 255, 232, 3, 225, 2]) # initial values to make calibration easier
            while True:
				if self.getHeading() != 0:
					break
				print("Please shake to initialize")
                time.sleep(0.3)
            print("Please place on a flat surface for finnish initialization")
            self.calibrate()
			print("Initialization complete")
			self.started = True

    def calibrate(self):
		for i in range(50):
			print(self.getCalibrationValues())
			time.sleep(0.2)

    def getHeading(self):
        while True:
            try:
                heading=0
                heading, roll, pitch = self.bno.read_euler() # heading is the top down angle, pitch is the angle of elevation and roll is the rotation of the gyroscope around the axis defined by the pitch and heading
            except RuntimeError:
				print("Could not read from compass, repeating attempt")
				continue
			else:
				break
        return heading

    def getCalibrationStatus(self):
		sys, gyro, accel, mag = self.bno.get_calibration_status()
		return True if min([sys,gyro,accel,mag]) == 3 else False # true if the robot is calibrated well

    def getCalibrationValues(self):
        return self.bno.get_calibration_status() # return how well calibrated each aspect of the compass is

    def setCalibrationValues(self,values):
		for i in range(10):
			try:
				self.bno.set_calibration(values)
			except:
				if i == 4:
					raise RuntimeError("Unable to write to compass")


class Lidar:
    def __init__(self):
        self.forwardAngle=0


class Thunderborg:
    def __init__(self,robot):
        self.robot=robot
        self.ZB=ThunderBorg3.ThunderBorg()
        self.initiate()

    def initiate(self):
        self.ZB.init()


class Robot: # ties all other classes together, and allows functions that use several low level components
    def __init__(self):
        self.thunderborg=Thunderborg(self)
        self.controller=Controller(self)
        self.compass=Compass(self)


    def shutdown(self):
		try:
			GPIO.cleanup()
		except:
			pass
		try:
			self.controller.close()
		except:
			pass
		try:
			pass # shut down any cameras
		except:
			pass
		try:
			self.stop()
		except:
			pass
		print("Processes Safely Stopped")
        
    def stop(self):
        self.motion.forward(0)


robot=Robot()
atexit.register(robot.shutdown) #
