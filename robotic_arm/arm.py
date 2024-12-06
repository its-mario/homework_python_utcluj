import serial
import math

L1, L2, L3 = 56.5, 40.5, 40.5
X0, Y0 = 0, 80


class Arm:

    def __init__(
            self,
            arduino: serial.Serial,
    ):
        self.arduino = arduino
        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0
        self.q4 = 0.0
        self.delta = 0

    def _send_data(self, x_val, y_val, z_val, w_val, gripper_val):
        data = f"{x_val},{y_val},{z_val},{w_val}, {gripper_val}\n"
        self.arduino.write(data.encode())
        print(f"Sending to Arduino: X={x_val}, Y={y_val}, Z={z_val}, W={w_val}")

    def set_position(self, q1, q2, q3, q4):
        print(q1, q2, q3, q4)
        self._send_data(q1, q2, q3, q4, 0)
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4

    def set_position_rgm(self, x: float, y: float, z: float, delta: float) -> (
            float, float, float, float):
        q1, q2, q3, q4 = Arm.rgm(x, y, z, delta, self.q1, self.q2, self.q3, self.q4)

        self.set_position(q1, q2, q3, q4)

    @staticmethod
    def rgm(x: float, y: float, z: float, delta: float, q1: float, q2: float, q3: float, q4: float, to_print=False) -> (
            float, float, float, float):
        r = math.sqrt(x * x + y * y)  # Distanța de la origine în proiecția 2D
        q1_0 = math.degrees(math.acos((r * r + x * x - y * y) / (2 * r * x)))  # Unghiul pentru q1

        # Calcularea coordonatelor pentru următoarea poziție
        xa = r + math.cos(math.radians(180 + delta)) * L3 - X0
        ya = z + math.sin(math.radians(180 + delta)) * L3 - Y0
        oa = math.sqrt(xa ** 2 + ya ** 2)  # Distanța până la noua poziție

        # Calcularea unghiurilor pentru soluțiile cinematice inverse
        oa_ox = math.degrees(math.acos((oa * oa + xa * xa - ya * ya) / (2 * oa * xa)))
        a_o_q3 = math.degrees(math.acos((oa * oa + L1 * L1 - L2 * L2) / (2 * oa * L1)))  # Unghiul care implică q3

        q2_2 = oa_ox - a_o_q3  # A doua valoare posibilă pentru q2
        q2_1 = oa_ox + a_o_q3  # Prima valoare posibilă pentru q2

        q3_angle = math.degrees(math.acos((L1 * L1 + L2 * L2 - oa * oa) / (L1 * L2 * 2)))  # Unghiul pentru q3
        q3_2 = 180 - q3_angle  # A doua valoare posibilă pentru q3
        q3_1 = -(180 - q3_angle)  # Prima valoare posibilă pentru q3

        # Calcularea valorilor posibile pentru q4
        q4_2 = delta - q2_2 - q3_2  # A doua valoare posibilă pentru q4
        q4_1 = delta - q2_1 - q3_1  # Prima valoare posibilă pentru q4

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
        if -90 < q1 < 90 and 0 < q2 < 50 and -90 < q3 < 90 and -90 < q4 < 90:
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

        if toPrint:
            print(f"X : {x3d} , Y : {y3d} , Z : {z3d} , delta : {delta}")

        return x3d, y3d, z3d, delta
