from motion.core import RobotControl, Waypoint, InterpreterStates, LedLamp
import time
from math import *

def main():
    lamp = LedLamp("192.168.56.101")
    robot = RobotControl("192.168.56.103")

    if robot.connect():
        lamp.setLamp("1111")

        robot.engage()
        if robot.moveToStart():
            lamp.setLamp("1000")

            robot.manualCartMode()
            print(robot.getActualStateOut(), robot.getRobotMode(), robot.getRobotState())
            
            robot.manualJointMode()
            print(robot.getActualStateOut(), robot.getRobotMode(), robot.getRobotState())

            robot.moveToPointJ([Waypoint([radians(0.0), radians(0.0), radians(70.0), radians(0.0), radians(90.0), radians(0.0)])])
            print(robot.getActualStateOut(), robot.getRobotMode(), robot.getRobotState())


            robot.moveToPointJ([Waypoint([radians(0.0), radians(0.0), radians(70.0), radians(0.0), radians(90.0), radians(0.0)])])
            
            while not(robot.getActualStateOut() is InterpreterStates.PROGRAM_IS_DONE.value):
                print("Robot is move")
                lamp.setLamp("0100")
                time.sleep(2.0)
                robot.pause()
                time.sleep(1.0)
                robot.play()
            else:
                print("Robot in point")
                robot.toolON()
                time.sleep(0.25)

            point1 = Waypoint([0.5, -0.135, 0.3, pi/2, 0.0, pi])
            robot.moveToPointL([point1])

            while not(robot.getActualStateOut() is InterpreterStates.PROGRAM_IS_DONE.value):
                print("Robot is move")
                lamp.setLamp("0100")
                time.sleep(2.0)
                robot.stop()

                if (robot.getActualStateOut() is InterpreterStates.PROGRAM_STOP_S.value):
                    lamp.setLamp("0001")
                    break

            else:
                print("Robot in point")
                robot.toolOFF()
                time.sleep(0.25)
            
            lamp.setLamp("1000")
                
        robot.manualCartMode()
        robot.setCartesianVelocity([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        time.sleep(1.0)

        # robot.manualJointMode()
        # robot.setJointVelocity([-1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        # time.sleep(1.0)



    else:
        lamp.setLamp("0000")

if __name__ == "__main__":
    main()