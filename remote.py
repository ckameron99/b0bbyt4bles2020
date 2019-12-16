import xbox

def rc():
    maxSpeed=1
    while True:
        if robot.controller.getConnectionStatus():
            if robot.controller.dPadUpButton():
                maxSpeed=min(1,maxSpeed+0.1)
                time.sleep(0.2)
            elif robot.controller.dPadDownButton():
                maxSpeed=max(0.5,maxSpeed-0.1)
                time.sleep(0.2)
            if robot.controller.yButton():
                robot.reverse=robot.reverse^1
                time.sleep(0.2)

            if robot.controller.rightTriggerLocation():
                if robot.controller.leftXButton() < -0.2:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.rightTriggerLocation()*abs(1-abs(robot.controller.leftXButton()))),(max(maxSpeed,0.8)*robot.controller.rightTriggerLocation()))
                elif robot.controller.leftXButton() > 0.2:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.rightTriggerLocation()),(max(maxSpeed,0.8)*robot.controller.rightTriggerLocation()*abs(1-abs(robot.controller.leftXButton()))))
                else:
                    robot.forward((maxSpeed*robot.controller.rightTriggerLocation()),(maxSpeed*robot.controller.rightTriggerLocation()))

            elif robot.controller.leftTriggerLocation():
                if robot.controller.leftXButton() > 0.2:
                    robot.forward((max(maxSpeed,0.8)*-robot.controller.leftTriggerLocation()*abs(1-abs(robot.controller.leftXButton()))),(max(maxSpeed,0.8)*-robot.controller.leftTriggerLocation()))
                elif robot.controller.leftXButton() < -0.2:
                    robot.forward((max(maxSpeed,0.8)*-robot.controller.leftTriggerLocation()),(max(maxSpeed,0.8)*-robot.controller.leftTriggerLocation()*abs(1-abs(robot.controller.leftXButton()))))
                else:
                    robot.forward((maxSpeed*-robot.controller.leftTriggerLocation()),(maxSpeed*-robot.controller.leftTriggerLocation()))
            elif robot.controller.leftBumperButton():
                robot.turn((-0.9))
            elif robot.controller.rightBumperButtonr():
                robot.turn((0.9))
            else:
                if abs(robot.controller.leftY()-robot.controller.rightYButton())<0.5:
                    robot.forward((maxSpeed*robot.controller.leftYButton()),(maxSpeed*robot.controller.rightYButton()))
                else:
                    robot.forward((max(maxSpeed,0.8)*robot.controller.leftYButton()),(max(maxSpeed,0.8)*robot.controller.rightYButton()))
        else:
            robot.stop()

        if robot.controller.xButton():
            robot.stop()
            break
