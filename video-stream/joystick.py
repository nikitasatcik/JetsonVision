import Jetson.GPIO as GPIO
from time import sleep
from pyPS4Controller.controller import Controller

# Define motor pins
MOTOR1_IN1_PIN = 15  # Input Pin 1 for Motor 1
MOTOR1_IN2_PIN = 16  # Input Pin 2 for Motor 1

MOTOR2_IN1_PIN = 21  # Input Pin 1 for Motor 2
MOTOR2_IN2_PIN = 22  # Input Pin 2 for Motor 2

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR1_IN1_PIN, GPIO.OUT)
GPIO.setup(MOTOR1_IN2_PIN, GPIO.OUT)

GPIO.setup(MOTOR2_IN1_PIN, GPIO.OUT)
GPIO.setup(MOTOR2_IN2_PIN, GPIO.OUT)

# Define motor control functions
def set_motor_speed(motor, speed):
    if speed >= 0:
        GPIO.output(motor[0], GPIO.HIGH)
        GPIO.output(motor[1], GPIO.LOW)
    else:
        GPIO.output(motor[0], GPIO.LOW)
        GPIO.output(motor[1], GPIO.HIGH)

# Create a class for controlling motors with the DualShock controller
class MotorController(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_axis(self, axis):
        if axis.name == 'r2':  # Acceleration
            speed = -axis.value * 100  # Reverse value for forward motion
            set_motor_speed((MOTOR1_IN1_PIN, MOTOR1_IN2_PIN), speed)
            set_motor_speed((MOTOR2_IN1_PIN, MOTOR2_IN2_PIN), speed)
        elif axis.name == 'l2':  # Brake
            speed = axis.value * 100
            set_motor_speed((MOTOR1_IN1_PIN, MOTOR1_IN2_PIN), speed)
            set_motor_speed((MOTOR2_IN1_PIN, MOTOR2_IN2_PIN), speed)
        elif axis.name == 'left_stick_x':  # Steering
            steering_speed = axis.value * 50
            set_motor_speed((MOTOR1_IN1_PIN, MOTOR1_IN2_PIN), steering_speed)
            set_motor_speed((MOTOR2_IN1_PIN, MOTOR2_IN2_PIN), -steering_speed)
        elif axis.name == 'right_stick_x':  # Turning right
            turning_speed = axis.value * 50
            set_motor_speed((MOTOR1_IN1_PIN, MOTOR1_IN2_PIN), turning_speed)
            set_motor_speed((MOTOR2_IN1_PIN, MOTOR2_IN2_PIN), turning_speed)

    def on_button_release(self, button):
        set_motor_speed((MOTOR1_IN1_PIN, MOTOR1_IN2_PIN), 0)
        set_motor_speed((MOTOR2_IN1_PIN, MOTOR2_IN2_PIN), 0)

# Create an instance of the MotorController class
controller = MotorController(interface="/dev/input/js0", connecting_using_ds4drv=False)

try:
    controller.listen()
except KeyboardInterrupt:
    pass
finally:
    # Clean up GPIO on exit
    GPIO.cleanup()

    