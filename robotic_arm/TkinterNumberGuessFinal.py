from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import random
from typing import Callable

import pygame
import serial
import time


class App(Tk):
    def __init__(self, fn_joystick: Callable, read_joystick = 5):
        """
        :param fn_joystick: the function that will execute reading and executing joystick instructions
        :type fn_joystick: Callable[]
        :param read_joystick: interval in milliseconds when @fn_joystick will be called
        """

        super().__init__()

        self.fn_joystick = fn_joystick

        self.joint = {
            1: DoubleVar(value=0),
            2: DoubleVar(value=0),
            3: DoubleVar(value=0),
            4: DoubleVar(value=0),
        }

        self.coordinates = [
            DoubleVar(value=0),
            DoubleVar(value=0),
            DoubleVar(value=0),
        ]

        self.control_from_joystick = BooleanVar(value=False)

        self.file_path_label = Label()

        self.configure_window()
        self.draw_header()
        self.draw_grid()
        self.loop_for_controller()

    def loop_for_controller(self):
        if self.control_from_joystick:
            """here will read the position from joystick and change it"""

            pass

        self.after(1000, self.loop_for_controller)  # for those who understand what i did here please forgive me

    def load_from_file(self):
        filename = askopenfilename()
        self.file_path_label.config(text=filename)
        # TODO: implement loading from file

    def save_to_file(self):
        # TODO: implement saving
        pass

    def configure_window(self):
        self.title("Welcome to Number Guess")

        # Set the Windows size...
        self.geometry('900x150')

        # Scale it up, so we can see it better...
        self.tk.call('tk', 'scaling', 1.5)

    def draw_header(self):
        radio_btn_c = Radiobutton(self, text="Calculator", variable=self.control_from_joystick, value=False)
        radio_btn_c.grid(column=0, row=0)
        radio_btn_joystick = Radiobutton(self, text="Joystick", variable=self.control_from_joystick, value=True)
        radio_btn_joystick.grid(column=1, row=0)

        self.file_path_label = Label(self, text="")
        self.file_path_label.grid(column=3, row=0)
        save_btn = Button(self, text="Save", command=self.save_to_file)
        save_btn.grid(column=4, row=0)
        load_btn = Button(self, text="Load from File", command=self.load_from_file)
        load_btn.grid(column=5, row=0)

    def draw_grid(self):
        spinNumber1 = Spinbox(self, from_=0, to=180, textvariable=self.joint[1], )
        spinNumber1.grid(column=0, row=1)
        spinNumber2 = Spinbox(self, from_=0, to=180, textvariable=self.joint[2], )
        spinNumber2.grid(column=1, row=1)
        spinNumber3 = Spinbox(self, from_=0, to=180, textvariable=self.joint[3], )
        spinNumber3.grid(column=2, row=1)
        spinNumber4 = Spinbox(self, from_=0, to=180, textvariable=self.joint[4], )
        spinNumber4.grid(column=3, row=1)

        btn_joint = Button(self, text="MOVE", )
        btn_joint.grid(column=5, row=1)

        # TODO: change the axial limits (when will know actual dimensions)
        spinNumberX = Spinbox(self, from_=10, to=300, textvariable=self.coordinates[0], )
        spinNumberX.grid(column=0, row=2)
        spinNumberY = Spinbox(self, from_=10, to=300, textvariable=self.coordinates[1], )
        spinNumberY.grid(column=1, row=2)
        spinNumberZ = Spinbox(self, from_=10, to=300, textvariable=self.coordinates[2], )
        spinNumberZ.grid(column=2, row=2)

        btn_joint = Button(self, text="MOVE", )
        btn_joint.grid(column=5, row=2)

    # def draw_grid_


if __name__ == "__main__":
    app = App()
    app.mainloop()







#
# import pygame

#
# pygame.init()
# pygame.joystick.init()
# controller = pygame.joystick.Joystick(0)
# controller.init()
#
# arduino = serial.Serial(port='COM9', baudrate=9600, timeout=1)
# time.sleep(2)


def send_data(x_val, y_val, z_val, w_val, gripper_val):
    data = f"{x_val},{y_val},{z_val},{w_val}, {gripper_val}\n"
    arduino.write(data.encode())
    print(f"Sending to Arduino: X={x_val}, Y={y_val}, Z={z_val}, W={w_val}")


x_vali = int(controller.get_axis(0) * 90 + 90)  # Left stick X-axis
y_vali = int(controller.get_axis(1) * 90 + 90)  # Left stick Y-axis
z_vali = int(controller.get_axis(3) * 90 + 90)  # Right stick X-axis
w_vali = int(controller.get_axis(2) * 90 + 90)  # Right stick Y-axis
gripper_open = 0

try:

    while True:
        pygame.event.pump()
        x_val = (controller.get_axis(0))  #Left stick X-axis
        y_val = (controller.get_axis(1))  # Left stick Y-axis
        z_val = (controller.get_axis(3))  # Right stick X-axis
        w_val = (controller.get_axis(2))  # Right stick Y-axis

        if controller.get_button(4):
            gripper_open = 70 if gripper_open == 0 else 0
            time.sleep(0.2)

        if (x_vali - x_val) > (x_vali + 0.1) or (x_vali - x_val) < (x_vali + -0.5):
            x_vali = x_vali + 2 * x_val
        if (y_vali - y_val) > (y_vali + 0.1) or (y_vali - y_val) < (y_vali + -0.5):
            y_vali = y_vali + 2 * y_val
        if (z_vali - z_val) > (z_vali + 0.1) or (z_vali - z_val) < (z_vali + -0.5):
            z_vali = z_vali + 2 * z_val
        if (w_vali - w_val) > (w_vali + 0.1) or (w_vali - w_val) < (w_vali + -0.5):
            w_vali = w_vali + 2 * w_val
        send_data(x_vali, y_vali, z_vali, w_vali, gripper_open)
        time.sleep(0.0001)
        if x_vali > 180:
            x_vali = 180
        if y_vali > 180:
            y_vali = 180
        if z_vali > 180:
            z_vali = 180
        if w_vali > 180:
            w_vali = 180
        if x_vali < 0:
            x_vali = 0
        if y_vali < 0:
            y_vali = 0
        if z_vali < 0:
            z_vali = 0
        if w_vali < 0:
            w_vali = 0
except KeyboardInterrupt:
    print("Process interrupted.")
finally:
    arduino.close()

# import math
#
#
# x=100*math.cos((math.radians(y_vali)))+math.cos((math.radians(y_vali+z_vali)))*100+math.cos((math.radians(y_vali+z_vali+w_vali)))*60
# y=100*math.sin((math.radians(y_vali)))+math.sin((math.radians(y_vali+z_vali)))*100+math.sin((math.radians(y_vali+z_vali+w_vali)))*60
