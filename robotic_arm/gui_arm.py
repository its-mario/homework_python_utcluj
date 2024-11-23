from tkinter import *
from tkinter.filedialog import askopenfilename
from typing import Callable


class GUIArm(Tk):
    def __init__(self, fn_joystick: Callable, frequency=5):
        """
        :param fn_joystick: the function that will execute reading and executing joystick instructions
        :type fn_joystick: Callable[]
        :param frequency: interval in milliseconds when @fn_joystick will be called
        """

        super().__init__()

        self.fn_joystick = fn_joystick
        self.frequency = frequency

        self.joint = {
            1: DoubleVar(value=0),
            2: DoubleVar(value=0),
            3: DoubleVar(value=0),
            4: DoubleVar(value=0),
        }

        self.coordinates = {
            "x": DoubleVar(value=0),
            "y": DoubleVar(value=0),
            "z": DoubleVar(value=0),
        }

        self.saved_points = []

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
                   self.loop_for_controller)  # for those who understand what i did here please forgive me

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
            joint = self.joint[i + 1]

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

        # creating 10 buttons
        for i in range(10):
            btn = Button(bottom, text=str(i + 1))
            btn.pack(side="left")
            # TODO: implement save/load from point


if __name__ == "__main__":
    def test_joystick():
        print("from joystick")


    app = GUIArm(fn_joystick=test_joystick)
    app.mainloop()
