from functools import partial
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Callable

from pygame.joystick import Joystick

from arm import Arm
from save_settings import check_validity


class GUIArm(Tk):
    def __init__(
            self,
            arm: Arm,
            joystick: Joystick,
            fn_load: Callable[[str], dict],
            fn_save: Callable[[str, dict], None],
            fn_validity=check_validity,
            frequency=5,
    ):
        """
        :param: arm: Arm object
        :param joystick: joystick that implements a `on_move` method that returns joints values
        :type joystick: Joystick
        :param fn_load: the function that will access file and load settings
        :param fn_save: function to save settings
        :param frequency: interval in milliseconds when @fn_joystick will be called
        """

        super().__init__()

        self.arm = arm

        self.joystick = joystick
        self.frequency = frequency
        self.fn_load = fn_load
        self.fn_save = fn_save
        self.fn_validity = fn_validity

        self.filename = ""
        self.saved_settings = {

            "saved_points": {

            }
        }

        self.joint = {
            "1": DoubleVar(value=0),
            "2": DoubleVar(value=0),
            "3": DoubleVar(value=0),
            "4": DoubleVar(value=0),
            "5": DoubleVar(value=0),
        }

        self.coordinates = {
            "x": DoubleVar(value=0.0),
            "y": DoubleVar(value=0.0),
            "z": DoubleVar(value=0.0),
            "delta": DoubleVar(value=0.0),
        }

        self.control_from_joystick = BooleanVar(value=False)
        self.save_position = BooleanVar(value=True)

        self.file_path_label = Label()

        self.configure_window()
        self.draw_header()
        self.draw_body()
        self.draw_bottom()
        self.loop_for_controller()
        self.to_home() # initial to send to 0, 0, 0, 0 position

    def to_home(self):
        self.arm.set_position(0, 90, 0, 0)

        self.joint["1"].set(self.arm.q1)
        self.joint["2"].set(self.arm.q2)
        self.joint["3"].set(self.arm.q3)
        self.joint["4"].set(self.arm.q4)

    def _move_from_joints(self):
        q1 = self.joint["1"].get()
        q2 = self.joint["2"].get()
        q3 = self.joint["3"].get()
        q4 = self.joint["4"].get()
        gripper = self.joint["5"].get()


        self.arm.set_position(q1, q2, q3, q4, gripper_val=gripper)

        x, y, z, delta = self.arm.fgm(q1, q2, q3, q4)

        self.coordinates["x"].set(x)
        self.coordinates["y"].set(y)
        self.coordinates["z"].set(z)
        self.coordinates["delta"].set(delta)

    def _move_from_coordinates(self):
        x = self.coordinates["x"].get()
        y = self.coordinates["y"].get()
        z = self.coordinates["z"].get()
        delta = self.coordinates['delta'].get()

        self.arm.set_position_rgm(x, y, z, delta)

        self.joint["1"].set(self.arm.q1)
        self.joint["2"].set(self.arm.q2)
        self.joint["3"].set(self.arm.q3)
        self.joint["4"].set(self.arm.q4)

    def loop_for_controller(self):
        if self.control_from_joystick.get():
            """here will read the position from joystick and change it"""
            q1 = self.joint["1"].get()
            q2 = self.joint["2"].get()
            q3 = self.joint["3"].get()
            q4 = self.joint["4"].get()
            gripper = self.joint["5"].get()
            q1, q2, q3, q4, gripper = self.joystick.on_move(q1, q2, q3, q4, gripper)


            self.joint["1"].set(round(q1, 2))
            self.joint["2"].set(round(q2, 2))
            self.joint["3"].set(round(q3, 2))
            self.joint["4"].set(round(q4, 2))
            self.joint["5"].set(round(gripper, 2))

            self._move_from_joints()

        self.after(self.frequency, self.loop_for_controller)  # for those who understand what I did here please forgive me

    def load_from_file(self):
        self.filename = askopenfilename()
        self.file_path_label.config(text=self.filename)
        self.saved_settings = self.fn_load(self.filename)

    def save_to_file(self):
        if not self.fn_validity(self.filename):
            self.filename = asksaveasfilename(defaultextension=".json")
            self.file_path_label.config(text=self.filename)

        self.fn_save(self.filename, self.saved_settings)

    def configure_window(self):
        self.title("Robotic Arm Electronics 1524e")

        # Set the Windows size...
        self.geometry('900x150')

        # Scale it up, so we can see it better...
        self.tk.call('tk', 'scaling', 1.5)

    def draw_header(self):
        header = Frame(self)
        header.pack(side='top')

        radio_btn_c = Radiobutton(header, text="Calculator", variable=self.control_from_joystick, value=False)
        radio_btn_c.pack(side='left')
        radio_btn_joystick = Radiobutton(header, text="Joystick", variable=self.control_from_joystick, value=True)
        radio_btn_joystick.pack(side='left')

        self.file_path_label = Label(header, text="")
        self.file_path_label.pack(side='right')
        save_btn = Button(header, text="Save", command=self.save_to_file)
        save_btn.pack(side='right')
        load_btn = Button(header, text="Load from File", command=self.load_from_file)
        load_btn.pack(side='right')

    def draw_body(self):
        body = Frame(self)
        body.pack()

        # row 1
        row1 = Frame(body)
        row1.pack()
        for i in range(len(self.joint)):
            joint = self.joint[f"{i + 1}"]

            element = Frame(row1)
            element.grid(column=i, row=0)

            label = Label(element, text=f"{i + 1}")
            label.pack(side='left')
            spin_number = Spinbox(element, from_=-180, to=180, textvariable=joint, format="%.2f")
            spin_number.pack(side='left')


        btn_joint = Button(row1, text="MOVE FGM", command=self._move_from_joints)
        btn_joint.grid(column=len(self.joint) + 1, row=0)

        # row 2
        row2 = Frame(body)
        row2.pack()
        for key, coordinate in self.coordinates.items():
            element = Frame(row2)
            element.pack(side="left")

            label = Label(element, text=key)
            label.pack(side="left")
            # TODO: change the axial limits (when will know actual dimensions)
            spin_number = Spinbox(element, from_=10, to=300, textvariable=coordinate)
            spin_number.pack(side="left")

        btn_joint = Button(row2, text="MOVE RGM", command=self._move_from_coordinates)
        btn_joint.pack(side="right")


    def draw_bottom(self):
        bottom = Frame(self)
        bottom.pack(side='bottom')

        button_home = Button(bottom, text="Home", command=self.to_home)
        button_home.pack(side="left")

        saved_options = Frame(bottom)
        saved_options.pack(side="left")

        check_box_1 = Radiobutton(saved_options, text="Save", variable=self.save_position, value=True)
        check_box_1.grid(row=0, column=0)
        check_box_2 = Radiobutton(saved_options, text="Load", variable=self.save_position, value=False)
        check_box_2.grid(row=0, column=1)

        def on_point(nr: int):

            if self.save_position.get():
                joint = {k: v.get() for k, v in self.joint.items()}
                # TODO: convert joint in coordinates
                coordinates = {}
                self.saved_settings["saved_points"][f"{nr}"] = {
                    "joint": joint,
                    "coordinates": coordinates,
                }
                print(f"save_position True {joint}")
            else:
                joint = self.saved_settings["saved_points"][f"{nr}"]["joint"]
                if len(joint) == 0: return  # finish execution if there is no settings saved

                for k, v in joint.items():
                    self.joint[k].set(int(v))
                self._move_from_joints()

        # creating 10 buttons
        for i in range(10):
            func = partial(on_point, i + 1)
            btn = Button(bottom, text=str(i + 1), command=func)
            btn.pack(side="left")


