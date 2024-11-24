from gui_arm import GUIArm
from save_settings import load_settings, save_settings

if __name__ == '__main__':
    def joystick(): pass


    gui_arm = GUIArm(
        fn_joystick=joystick,
        fn_load=load_settings,
        fn_save=save_settings,
    )
    gui_arm.mainloop()
