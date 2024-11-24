from functools import partial
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Callable
from save_settings import check_validity


class GUIArm(Tk):
    def __init__(
            self,
            fn_joystick: Callable,
            fn_load: Callable[[str], dict],
            fn_save: Callable[[str, dict], None],
            fn_validity=check_validity,
            frequency=5,
    ):
        """
        :param fn_joystick: the function that will execute reading and executing joystick instructions
        :type fn_joystick: Callable[]
        :param fn_load: the function that will access file and load settings
        :param fn_save: function to save settings
        :param frequency: interval in milliseconds when @fn_joystick will be called
        """

        super().__init__()

        self.fn_joystick = fn_joystick
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
            "1": IntVar(value=0),
            "2": IntVar(value=0),
            "3": IntVar(value=0),
            "4": IntVar(value=0),
        }

        self.coordinates = {
            "x": DoubleVar(value=0),
            "y": DoubleVar(value=0),
            "z": DoubleVar(value=0),
        }

        self.control_from_joystick = BooleanVar(value=False)
        self.save_position = BooleanVar(value=True)

        self.file_path_label = Label()

        self.configure_window()
        self.draw_header()
        self.draw_body()
        self.draw_bottom()
        self.loop_for_controller()

    def loop_for_controller(self):
        if self.control_from_joystick.get():
            """here will read the position from joystick and change it"""
            self.fn_joystick()

        self.after(self.frequency,
                   self.loop_for_controller)  # for those who understand what I did here please forgive me

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
            spin_number = Spinbox(element, from_=0, to=180, textvariable=joint)
            spin_number.pack(side='left')

        btn_joint = Button(row1, text="MOVE")
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

        btn_joint = Button(row2, text="MOVE", )
        btn_joint.pack(side="right")

    def draw_bottom(self):
        bottom = Frame(self)
        bottom.pack(side='bottom')
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
                # TODO: convert joint to coordinates
                coordinates = {}

                for k, v in joint.items():
                    self.joint[k].set(int(v))
                self.coordinates = {k: DoubleVar(value=v) for k, v in coordinates.items()}

        # creating 10 buttons
        for i in range(10):
            func = partial(on_point, i + 1)
            btn = Button(bottom, text=str(i + 1), command=func)
            btn.pack(side="left")


if __name__ == "__main__":
    def test_joystick():
        print("from joystick")


    app = GUIArm(fn_joystick=test_joystick)
    app.mainloop()
