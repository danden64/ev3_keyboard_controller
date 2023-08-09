import ev3_dc as ev3
from time import sleep
from keyboard import is_pressed

def init_motors(motors: list):
    for motor in motors:
        if motor != None:
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

def drive_while_held(keybind: str, motor: ev3.Motor, speed: int, direction: int=1):
    if is_pressed(keybind):
        drive_motor(motor, speed, direction)

def format_ID(brickID: str):
    ID = ''
    for i in range(5):
        ID += brickID[2*i:2*(i+1)] + ':'
    ID += brickID[10:12]
    return ID



def main():
    while True:
        try:
            brickID = '0016533f36a3'
            robot = ev3.EV3(protocol=ev3.BLUETOOTH, host=format_ID(brickID))
            motors = []
            try:   
                a = ev3.Motor(ev3.PORT_A, ev3_obj=robot)
                motors.append(a)
            except:
                pass
            try:
                b = ev3.Motor(ev3.PORT_B, ev3_obj=robot)
                motors.append(b)
            except:
                pass
            try:
                c = ev3.Motor(ev3.PORT_C, ev3_obj=robot)
                motors.append(c)
            except:
                pass
            try:
                d = ev3.Motor(ev3.PORT_D, ev3_obj=robot)
                motors.append(d)
            except:
                pass
            init_motors(motors)
            ev3.Sound(ev3_obj=robot).tone(440, duration=0.1, volume=10)
            print(robot)

            while not is_pressed('esc'):
                
                # ////////////////////
                # WRITE YOUR CODE HERE
                # ////////////////////
                
                sleep(0.01)


            try:
                for motor in motors:
                    motor.stop()
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
                raise e
            exit()


if __name__ == "__main__":
    main()
