import serial
from arm import Arm
from gui_arm import GUIArm
from save_settings import load_settings, save_settings


class SerialTest():
    def write(self, **args):
        pass


if __name__ == '__main__':
    def joystick(): pass


    # !!! when working with arduino uncomment the line below, and select correct COM !!!
    # arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)
    arduino = SerialTest()
    arm = Arm(
        arduino=arduino,
    )

    gui_arm = GUIArm(
        arm=arm,
        fn_joystick=joystick,
        fn_load=load_settings,
        fn_save=save_settings,
    )
    gui_arm.mainloop()
