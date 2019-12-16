import xbox

def rc():
    maxSpeed=1
    while True:
        if robot.controller.getConnectionStatus():
            if robot.controller.dpadUp():
                maxSpeed=min(1,maxSpeed+0.1)
                time.sleep(0.2)
            elif robot.controller.dpadDown():
                maxSpeed=max(0.5,maxSpeed-0.1)
                time.sleep(0.2)
            if robot.controller.Y():
                robot.reverse=robot.reverse^1
                time.sleep(0.2)

            if robot.controller.rightTrigger():
                if robot.controller.leftX() < -0.2:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.rightTrigger()*abs(1-abs(robot.controller.leftX()))),(max(maxSpeed,0.8)*robot.controller.rightTrigger()))
                elif robot.controller.leftX() > 0.2:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.rightTrigger()),(max(maxSpeed,0.8)*robot.controller.rightTrigger()*abs(1-abs(robot.controller.leftX()))))
                else:
                    robot.forward((maxSpeed*robot.controller.rightTrigger()),(maxSpeed*robot.controller.rightTrigger()))

            elif robot.controller.leftTrigger():
                if robot.controller.leftX() > 0.2:
                    robot.forward((max(maxSpeed,0.8)*-robot.controller.leftTrigger()*abs(1-abs(robot.controller.leftX()))),(max(maxSpeed,0.8)*-robot.controller.leftTrigger()))
                elif robot.controller.leftX() < -0.2:
                    robot.forward((max(maxSpeed,0.8)*-robot.controller.leftTrigger()),(max(maxSpeed,0.8)*-robot.controller.leftTrigger()*abs(1-abs(robot.controller.leftX()))))
                else:
                    robot.forward((maxSpeed*-robot.controller.leftTrigger()),(maxSpeed*-robot.controller.leftTrigger()))
            elif robot.controller.leftBumper():
                robot.turn((-0.9))
            elif robot.controller.rightBumper():
                robot.turn((0.9))
            else:
                if abs(robot.controller.leftY()-robot.controller.rightY())<0.5:
                    robot.forward((maxSpeed*robot.controller.leftY()),(maxSpeed*robot.controller.rightY()))
                else:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.leftY()),(max(maxSpeed,0.8)*robot.controller.rightY()))
        else:
            robot.stop()

        #print(robot.ultraFrontRight.distance())
        a = robot.ultraFrontLeftSide.distance()
        if a < 14:
               pass
               #print("Got 1")
               #robot.stop()
               #time.sleep(1)
        print(a)

        if robot.controller.X():
            robot.stop()
            break
