from angle_class import Angle
from math import pi

PI = pi

ang1 = Angle(1.5708)                # Значение в радианах (1.5708)
ang2 = Angle(radians=PI / 2)        # Именованный параметр radians (pi/2)
ang3 = Angle(degrees=90)            # Именованный параметр degrees (90 градусов)
ang4 = Angle(degrees=450)           # Угол больше 360 градусов (450 градусов)
ang5 = Angle()                      # Угол по умолчанию (0.0)

print(f"ang1 (1.5708 радиан): {ang1}")
print(f"ang2 (PI/2 радиан): {ang2}")
print(f"ang3 (90 градусов): {ang3}")
print(f"ang4 (450 градусов): {ang4}")
print(f"ang5 (по умолчанию): {ang5}")

## Геттеры
print("\n### Геттеры")
print(f"ang4.radians: {ang4.radians:.4f}")
print(f"ang4.degrees (вернет радианы): {ang4.degrees:.4f}")

## Сеттеры
print("\n### Сеттеры")
print(f"ang5 до установки: {ang5.radians:.4f}")
ang5.radians = 3.14159  # Установка через сеттер radians
print(f"ang5 после установки radians=3.14159: {ang5.radians:.4f}")

ang5.radians = 180  # Установка через сеттер degrees (ошибочно названный radians)
print(f"ang5 после установки degrees=180: {ang5.radians:.4f}") # 180° = PI радиан


ang_a = Angle(radians=1.0) # 1 радиан
ang_b = Angle(radians=0.5) # 0.5 радиан

print("\n### Арифметические операции")

# __add__ (Сложение)
print(f"{ang_a=}, {ang_b=}")
print(f"{ang_a + ang_b=}")

# __sub__ (Вычитание)
print(f"{ang_a - ang_b=}")

# __mul__ (Умножение)
mul_scalar = ang_a * 3
print(f"ang_a * 3 (1.0 * 3): {mul_scalar:.4f}")

# __truediv__ (Деление)
div_scalar = ang_a / 4
print(f"ang_a / 4 (1.0 / 4): {div_scalar:.4f}")

ang_c = Angle(degrees=90)   # 90°
ang_d = Angle(degrees=450)  # 450° -> нормализованный 90°
ang_e = Angle(degrees=180)  # 180°

print("\n### Операции сравнения")

# __eq__ (Равенство)
print(f"ang_c == ang_d (90° == 450°): {ang_c == ang_d}") # True (нормализованные равны)
print(f"ang_c == ang_e (90° == 180°): {ang_c == ang_e}") # False

# __lt__ (Меньше)
print(f"ang_c < ang_e (90° < 180°): {ang_c < ang_e}") # True

# __le__ (Меньше или равно)
print(f"ang_c <= ang_d (90° <= 450°): {ang_c <= ang_d}") # True

# __gt__ (Больше)
print(f"ang_e > ang_c (180° > 90°): {ang_e > ang_c}") # True

# __ge__ (Больше или равно)
print(f"ang_e >= ang_c (180° >= 90°): {ang_e >= ang_c}") # True

ang_f = Angle(radians=3.14159) # ~PI

print("\n### Преобразования и Представление")

# __int__ (Преобразование в целое число)
int_val = int(ang_f)
print(f"int(ang_f) (3.14159 -> int): {int_val}")

# __float__ (Преобразование в число с плавающей точкой)
float_val = float(ang_f)
print(f"float(ang_f) (3.14159 -> float): {float_val}")

# __str__ (Строковое представление для пользователя)
str_val = str(ang_f)
print(f"str(ang_f): '{str_val}'")

# __repr__ (Строковое представление для разработчика)
repr_val = repr(ang_f)
print(f"repr(ang_f): '{repr_val}'")

