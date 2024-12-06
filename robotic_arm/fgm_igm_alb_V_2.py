# algorithm by Toth Dominik

# import math
# from tkinter.messagebox import showinfo, showerror
#
# L1 = 100  # Lungimea primului segment
# L2 = 150  # Lungimea celui de-al doilea segment
# L3 = 100  # Lungimea celui de-al treilea segment
# X0 = 0  # Coordonata inițială pe axa X
# Y0 = 10  # Coordonata inițială pe axa Y
#
#
# def check_angles(q1, q2, q3, q4):
#     if -90 < q1 < 90 and 0 < q2 < 50 and -90 < q3 < 90 and -90 < q4 < 90:
#         return True
#     else:
#         return False
#
#
# while True:
#     print("Introducerea modelului geometric direct:")
#     q1 = float(input("Q1: "))  # Citirea valorii pentru unghiul Q1
#     q2 = float(input("Q2: "))  # Citirea valorii pentru unghiul Q2
#     q3 = float(input("Q3: "))  # Citirea valorii pentru unghiul Q3
#     q4 = float(input("Q4: "))  # Citirea valorii pentru unghiul Q4
#     if check_angles(q1, q2, q3, q4) == False:
#         showerror("Unghiuri nebune")
#         break
#     # Calcularea cinematicei directe în 2D
#     x2d = L1 * math.cos(math.radians(q2)) + L2 * math.cos(math.radians(q2 + q3)) + L3 * math.cos(
#         math.radians(q2 + q3 + q4)) + X0
#     y2d = L1 * math.sin(math.radians(q2)) + L2 * math.sin(math.radians(q2 + q3)) + L3 * math.sin(
#         math.radians(q2 + q3 + q4)) + Y0
#     z3d = y2d  # Se presupune că valoarea Z este aceeași cu valoarea Y
#     y3d = math.sin(math.radians(q1)) * x2d  # Componenta Y în 3D
#     x3d = math.cos(math.radians(q1)) * x2d  # Componenta X în 3D
#     delta = q2 + q3 + q4  # Unghiul total (sumă din q2, q3, q4)
#
#     print(f"X : {x3d} , Y : {y3d} , Z : {z3d} , delta : {delta}")  # Afișează coordonatele calculate
#     # up to here FGM
#     # Calcularea unor parametri auxiliare pentru cinematica inversă
#     r = math.sqrt(x3d * x3d + y3d * y3d)  # Distanța de la origine în proiecția 2D
#     q1_0 = math.degrees(math.acos((r * r + x3d * x3d - y3d * y3d) / (2 * r * x3d)))  # Unghiul pentru q1
#
#     # Calcularea coordonatelor pentru următoarea poziție
#     xa = r + math.cos(math.radians(180 + delta)) * L3 - X0
#     ya = z3d + math.sin(math.radians(180 + delta)) * L3 - Y0
#     oa = math.sqrt(xa ** 2 + ya ** 2)  # Distanța până la noua poziție
#
#     # Calcularea unghiurilor pentru soluțiile cinematice inverse
#     oa_ox = math.degrees(math.acos((oa * oa + xa * xa - ya * ya) / (2 * oa * xa)))
#     a_o_q3 = math.degrees(math.acos((oa * oa + L1 * L1 - L2 * L2) / (2 * oa * L1)))  # Unghiul care implică q3
#
#     q2_2 = oa_ox - a_o_q3  # A doua valoare posibilă pentru q2
#     q2_1 = oa_ox + a_o_q3  # Prima valoare posibilă pentru q2
#
#     q3_angle = math.degrees(math.acos((L1 * L1 + L2 * L2 - oa * oa) / (L1 * L2 * 2)))  # Unghiul pentru q3
#     q3_2 = 180 - q3_angle  # A doua valoare posibilă pentru q3
#     q3_1 = -(180 - q3_angle)  # Prima valoare posibilă pentru q3
#
#     # Calcularea valorilor posibile pentru q4
#     q4_2 = delta - q2_2 - q3_2  # A doua valoare posibilă pentru q4
#     q4_1 = delta - q2_1 - q3_1  # Prima valoare posibilă pentru q4
#
#     # Afișarea celor două seturi de soluții posibile pentru unghiurile articulațiilor
#     print(f"Coordonatele anterioare:\n"
#           f"Q1_1 : {q1_0}  Q2_1 : {q2_1}  Q3_1 : {q3_1}  Q4_1 : {q4_1}\n"
#           f"Q1_2 : {q1_0}  Q2_2 : {q2_2}  Q3_2 : {q3_2}  Q4_2 : {q4_2}\n")
#     # rgm
