import time

import pygame

class Joystick:

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        # self.controller = pygame.joystick.Joystick(0)
        # self.controller.init()

    def on_move(self, q1_i, q2_i, q3_i, q4_i, gripper_i):

        pygame.event.pump()
        q1 = (self.controller.get_axis(0))
        q2 = (self.controller.get_axis(1))
        q3 = (self.controller.get_axis(2))
        q4 = (self.controller.get_axis(3))
        gripper_plus = (self.controller.get_axis(4)) + 1
        gripper_minus = (self.controller.get_axis(5)) + 1
        if -0.05 < q1 < 0.05:
            q1 = 0
        if -0.05 < q2 < 0.05:
            q2 = 0
        if -0.05 < q3 < 0.05:
            q3 = 0
        if -0.05 < q4 < 0.05:
            q4 = 0

        return q1_i + q1 /2, q2_i + q2/2, q3_i + q3/2, q4_i + q4/2, gripper_i - gripper_minus/2 + gripper_plus/2

if __name__ == "__main__":
    joystick = Joystick()

    q1, q2, q3, q4, gripper = 0, 0, 0, 0, 0
    while True:
        q1, q2, q3, q4, gripper = joystick.on_move(q1, q2, q3, q4, gripper)
        print(q1, q2, q3, q4)
        time.sleep(0.05)