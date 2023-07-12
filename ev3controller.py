import ev3_dc as ev3
from time import sleep
from keyboard import is_pressed

def init_motor_settings(*motors: ev3.Motor):
    for motor in motors:
        motor.sync_mode = ev3.ASYNC
        motor.delta_time = 0.01
        motor.ramp_up_time = 0.1
        motor.ramp_down_time = 0.1

def drive_motor(motor: ev3.Motor, speed: int, direction: int=1):
    if speed > 0:
        motor.speed = min(abs(speed), 100)
        motor.start_move(direction=1*direction)
    elif speed < 0:
        motor.speed = min(abs(speed), 100)
        motor.start_move(direction=-1*direction)
    else:
        motor.stop()

def drive_robot(left: ev3.Motor, right: ev3.Motor, leftDirection: int, rightDirection: int, speedDrive: int, speedTurn: int):
    speedLeft = (int(is_pressed('w'))-int(is_pressed('s')))*speedDrive + (int(is_pressed('d'))-int(is_pressed('a')))*speedTurn
    speedRight = (int(is_pressed('w'))-int(is_pressed('s')))*speedDrive + (int(is_pressed('a'))-int(is_pressed('d')))*speedTurn

    drive_motor(left, speedLeft, direction=leftDirection)
    drive_motor(right, speedRight, direction=rightDirection)

def drive_motor_to(motor: ev3.Motor, angle: int, speed: int, brake: bool, keybind: str):
    if is_pressed(keybind):
        motor.start_move_to(angle, speed=speed, brake=brake)

def drive_motor_for(motor: ev3.Motor, time: float, speed: int, direction: int, brake: bool, keybind: str):
    if is_pressed(keybind):
        motor.start_move_for(time, speed=speed, direction=direction, brake=brake)

def main():
    while True:
        try:
            robot = ev3.EV3(protocol=ev3.BLUETOOTH, host='00:16:53:47:94:7e')
            print(robot)
            a = ev3.Motor(ev3.PORT_A, ev3_obj=robot)
            b = ev3.Motor(ev3.PORT_B, ev3_obj=robot)
            c = ev3.Motor(ev3.PORT_C, ev3_obj=robot)
            d = ev3.Motor(ev3.PORT_D, ev3_obj=robot)
            init_motor_settings(a, b, c, d)
            ev3.Sound(ev3_obj=robot).tone(440, duration=0.1, volume=10)
            
            while True:
                drive_robot(left=b, right=c, leftDirection=1, rightDirection=1, speedDrive=80, speedTurn=50)

                #drive_motor_to(motor=d, angle=80, speed=40, brake=True, keybind='q')
                #drive_motor_to(motor=d, angle=0, speed=40, brake=True, keybind='e')

                #drive_motor_for(motor=d, time=1, speed=60, direction=-1, brake=False, keybind='f')

                sleep(0.01)

        except KeyboardInterrupt:
            try:
                a.stop()
                b.stop()
                c.stop()
                d.stop()
                del robot
                print("Ended program successfully")
            except NameError:
                print("Robot could not be terminated properly")
            exit()
        
        except Exception as e:
            if str(e) == "No EV3 device found":
                print("Failed to connect to EV3")
                sleep(1)
            else:
                print('\n' + str(e))
            exit()

if __name__ == "__main__":
    main()
