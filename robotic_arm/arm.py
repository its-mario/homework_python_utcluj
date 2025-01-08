import serial
import math

L1, L2, L3 = 100, 150, 100
X0, Y0 = 0, 80


class Arm:

    def __init__(
            self,
            arduino: serial.Serial,
    ):
        self.arduino = arduino
        self.q1 = 1
        self.q2 = 89
        self.q3 = -1
        self.q4 = 1
        self.gripper_value = 0
        self.delta = 0

    def _send_data(self, q1, q2, q3, q4, gripper_val):
        data = f"{q1},{q2},{q3},{q4}, {gripper_val}\n"
        self.arduino.write(data.encode())
        print(f"Sending to Arduino: Q_1 = {q1} | Q_2 = {q2} | Q_3 = {q3} | Q_4 = {q4} | Grp = {gripper_val}")

    def set_position(self, q1, q2, q3, q4, gripper_val=20):
        # print(q1, q2, q3, q4)

        self._send_data(q1, q2, q3, q4, gripper_val)
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.gripper_value = gripper_val

    def set_position_rgm(self, x: float, y: float, z: float, delta: float) -> (
            float, float, float, float):
        q1, q2, q3, q4 = Arm.rgm(x, y, z, delta, self.q1, self.q2, self.q3, self.q4)

        self.set_position(q1, q2, q3, q4)

    @staticmethod
    def rgm(x_3d : float, y_3d: float, z_3d: float, delta: float, q1: float, q2: float, q3: float, q4: float, to_print=True) -> (
            float, float, float, float):

        print(x_3d, y_3d, z_3d, delta)
        oo_ = math.sqrt(x_3d * x_3d + y_3d * y_3d)
        q1_0 = math.degrees(math.acos((oo_ * oo_ + x_3d * x_3d - y_3d * y_3d) / (2 * oo_ * x_3d)))
        xa_ = oo_ + math.cos(math.radians(180 + delta)) * L3 - X0
        ya_ = z_3d + math.sin(math.radians(180 + delta)) * L3 - Y0
        oa_ = math.sqrt((xa_) ** 2 + (ya_) ** 2)
        oa__Ox = math.degrees(math.acos((oa_ * oa_ + xa_ * xa_ - ya_ * ya_) / (2 * oa_ * xa_)))
        a_o_oq3_2 = math.degrees(math.acos((oa_ * oa_ + L1 * L1 - L2 * L2) / (2 * oa_ * L1)))
        q2_2 = oa__Ox - a_o_oq3_2
        q2_1 = oa__Ox + a_o_oq3_2
        oq3_2_q3_2a_ = math.degrees(math.acos((L1 * L1 + L2 * L2 - oa_ * oa_) / (L1 * L2 * 2)))
        q3_2 = +(180 - oq3_2_q3_2a_)
        q3_1 = -(180 - oq3_2_q3_2a_)
        q4_2 = delta - q2_2 - q3_2
        q4_1 = delta - q2_1 - q3_1

        q1_0 = round(q1_0, 5)
        q2_1 = round(q2_1, 5)
        q3_1 = round(q3_1, 5)
        q4_1 = round(q4_1, 5)
        q2_2 = round(q2_2, 5)
        q3_2 = round(q3_2, 5)
        q4_2 = round(q4_2, 5)

        if to_print:
            # Afișarea celor două seturi de soluții posibile pentru unghiurile articulațiilor
            print(f"Coordonatele anterioare:\n"
                  f"Q1_1 : {q1_0}  Q2_1 : {q2_1}  Q3_1 : {q3_1}  Q4_1 : {q4_1}\n"
                  f"Q1_2 : {q1_0}  Q2_2 : {q2_2}  Q3_2 : {q3_2}  Q4_2 : {q4_2}\n")

        if abs(q2 - q2_1) + abs(q3 - q3_1) + abs(q4 - q4_1) <= abs(q2 - q2_2) + abs(q3 - q3_2) + abs(q4 - q4_2):
            return q1_0, q2_1, q3_1, q4_1
        else:
            return q1_0, q2_2, q3_2, q4_2

    @staticmethod
    def check_angles(q1, q2, q3, q4):
        if -90 <= q1 <= 90 and 0 <= q2 <= 100 and -90 <= q3 <= 90 and -90 <= q4 <= 90:
            return True
        else:
            return False

    @staticmethod
    def fgm(q1: float, q2: float, q3: float, q4: float, toPrint=False):
        if not Arm.check_angles(q1, q2, q3, q4):
            raise Exception("Unghiuri nebune")

        # Calcularea cinematicei directe în 2D
        x2d = L1 * math.cos(math.radians(q2)) + L2 * math.cos(math.radians(q2 + q3)) + L3 * math.cos(
            math.radians(q2 + q3 + q4)) + X0
        y2d = L1 * math.sin(math.radians(q2)) + L2 * math.sin(math.radians(q2 + q3)) + L3 * math.sin(
            math.radians(q2 + q3 + q4)) + Y0
        z3d = y2d  # Se presupune că valoarea Z este aceeași cu valoarea Y
        y3d = math.sin(math.radians(q1)) * x2d  # Componenta Y în 3D
        x3d = math.cos(math.radians(q1)) * x2d  # Componenta X în 3D
        delta = q2 + q3 + q4  # Unghiul total (sumă din q2, q3, q4)

        x3d=round(x3d,5)
        y3d = round(y3d, 5)
        z3d = round(z3d, 5)
        delta = round(delta, 5)

        if toPrint:
            print(f"X : {x3d} , Y : {y3d} , Z : {z3d} , delta : {delta}")

        return x3d, y3d, z3d, delta
