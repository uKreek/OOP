import math

PI = math.pi


class Angle:
    """Класс для работы с углами"""

    def __init__(self, value=0.0, radians=None, degrees=None):
        """
        Создание угла. Можно задать:
        - напрямую значение в радианах: Angle(1.57)
        - через именованные параметры: Angle(radians=1.57) или Angle(degrees=90)
        """
        if radians is not None:
            self._radians = float(radians)
        elif degrees is not None:
            self._radians = math.radians(float(degrees))
        else:
            self._radians = float(value)

    @property
    def _normal_ang(self):
        """Нормализация угла в диапазон [0, 2*pi)"""
        return self._radians % (2 * PI)

    @property
    def radians(self):
        return self._radians

    @property
    def degrees(self):
        return self._radians

    @radians.setter
    def radians(self, value):
        self._radians = float(value)

    @degrees.setter
    def radians(self, value):
        self._radians = float(math.radians(value))

    def __eq__(self, other):
        '''сравнение углов в радианах'''
        if isinstance(other, Angle):
            return math.isclose(self._normal_ang, other._normal_ang, rel_tol=1e-9)

    def __int__(self):
        return int(self._radians)

    def __float__(self):
        return float(self._radians)

    def __lt__(self, other):
        '''less than'''
        if isinstance(other, Angle):
            return self._normal_ang < other._normal_ang

    def __le__(self, other):
        '''less or equal'''
        if isinstance(other, Angle):
            return self._normal_ang <= other._normal_ang

    def __gt__(self, other):
        '''greater than'''
        if isinstance(other, Angle):
            return self._normal_ang > other._normal_ang

    def __ge__(self, other):
        '''great or equal'''
        if isinstance(other, Angle):
            return self._normal_ang >= other._normal_ang

    def __add__(self, other):
        if isinstance(other, Angle):
            return self._radians + other._radians
        return self._radians + other

    def __sub__(self, other):
        if isinstance(other, Angle):
            return self._radians - other._radians
        return self._radians - other

    def __mul__(self, other):
        return self._radians * other

    def __truediv__(self, other):
        return self._radians / other

    def __str__(self):
        return f'{self._radians:.4f}'

    def __repr__(self):
        return f"Angle(radians={self._radians})"



class AngleRange:
    def __init__(self, start, end, start_inclusive=True, end_inclusive=True):
        """
        Создание промежутка углов.
        start, end: начальный и конечный углы (Angle, float или int)
        start_inclusive, end_inclusive: включающие ли границы
        """
        self.start = self._to_angle(start)
        self.end = self._to_angle(end)
        self.start_inclusive = start_inclusive
        self.end_inclusive = end_inclusive

    def _to_angle(self, value):
        """Преобразование в Angle"""
        if isinstance(value, Angle):
            return value
        elif isinstance(value, (int, float)):
            return Angle(value)
        else:
            raise TypeError("Значение должно быть Angle, int или float")

    def __eq__(self, other):
        if not isinstance(other, AngleRange):
            return False
        return (self.start == other.start and
                self.end == other.end and
                self.start_inclusive == other.start_inclusive and
                self.end_inclusive == other.end_inclusive)

    def __str__(self):
        start_bracket = "[" if self.start_inclusive else "("
        end_bracket = "]" if self.end_inclusive else ")"
        return f"{start_bracket}{self.start} - {self.end}{end_bracket}"

    def __repr__(self):
        start_bracket = "[" if self.start_inclusive else "("
        end_bracket = "]" if self.end_inclusive else ")"
        return f"AngleRange({start_bracket}{self.start._radians:.6f}, {self.end._radians:.6f}{end_bracket})"


    def __abs__(self):
        """Длина промежутка в радианах"""
        start_rad = self.start.radians
        end_rad = self.end.radians

        if end_rad >= start_rad:
            return end_rad - start_rad
        else:
            return (2 * PI - start_rad) + end_rad

    def __contains__(self, item):
        if isinstance(item, Angle):
            angle = item.radians
        elif isinstance(item, (int, float)):
            angle = Angle(item).radians
        elif isinstance(item, AngleRange):
            return self._contains_range(item)
        else:
            return False

        start_rad = self.start.radians
        end_rad = self.end.radians

        if start_rad <= end_rad:
            # Нормальный случай
            left_ok = angle > start_rad or (angle == start_rad and self.start_inclusive)
            right_ok = angle < end_rad or (angle == end_rad and self.end_inclusive)
            return left_ok and right_ok
        else:
            # Промежуток пересекает 0
            left_ok = angle >= start_rad or (angle == start_rad and self.start_inclusive)
            right_ok = angle <= end_rad or (angle == end_rad and self.end_inclusive)
            return left_ok or right_ok

    def _contains_range(self, other):
        """Проверка вхождения одного промежутка в другой"""
        # Упрощенная проверка - проверяем что обе границы другого промежутка содержатся в текущем
        return other.start in self and other.end in self

    def __add__(self, other):
        """Объединение промежутков"""
        if not isinstance(other, AngleRange):
            return NotImplemented

        # Упрощенная реализация - возвращаем список промежутков
        if self._can_merge(other):
            start = min(self.start, other.start, key=lambda x: x.radians)
            end = max(self.end, other.end, key=lambda x: x.radians)
            return [AngleRange(start, end)]
        else:
            return [self, other]

    def __sub__(self, other):
        """Разность промежутков"""
        if not isinstance(other, AngleRange):
            return NotImplemented

        # Упрощенная реализация
        if other in self:
            start_bracket = False if other.start_inclusive else True
            end_bracket = False if other.end_inclusive else True
            # Если другой промежуток полностью внутри текущего
            return [AngleRange(self.start, other.start, end_inclusive=start_bracket), AngleRange(other.end, self.end, start_inclusive=end_bracket)]
        else:
            return [self]

    def _can_merge(self, other):
        """Проверка возможности объединения промежутков"""
        return (other.start in self or other.end in self or
                self.start in other or self.end in other)

# region angle test
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

# endregion

# region range test
range1 = AngleRange(start=1.0, end=3.0)  # [1.0 - 3.0] (float, по умолчанию включительно)
range2 = AngleRange(start=Angle(degrees=350), end=Angle(degrees=10), end_inclusive=False) # [350° - 10°) (Пересекает 0)
range3 = AngleRange(start=0.5, end=0.5, start_inclusive=True, end_inclusive=True) # [0.5 - 0.5] (Точка)

print("### Инициализация и Представление")
print(f"range1 (нормальный): {range1}")  # __str__
print(f"range2 (через 0): {range2}")    # __str__
print(f"repr(range1): {repr(range1)}")  # __repr__

print("\n### длина __abs__")

# range1: [1.0 - 3.0]
abs1 = abs(range1)  # __abs__
print(f"длина range1: {abs1:.4f}")

print("\n### Вхождение (__contains__)")

# Тестируемый диапазон: range1 = [1.0 - 3.0] (включительно)

test_angle1 = Angle(1.5)
test_angle2 = Angle(1.0) # Граница
test_angle3 = Angle(3.0) # Граница
test_angle4 = Angle(3.1) # Снаружи

print(f"Угол 1.5 in range1 = {range1}: {test_angle1 in range1}") # True (внутри)
print(f"Угол 1.0 in range1 = {range1}: {test_angle2 in range1}") # True (границу включает)
print(f"Угол 3.0 in range1 = {range1}: {test_angle3 in range1}") # True (границу включает)
print(f"Угол 3.1 in range1 = {range1}: {test_angle4 in range1}") # False (снаружи)

# Тестируем невключенную границу
range5 = AngleRange(start=1.0, end=3.0, end_inclusive=False) # [1.0 - 3.0)
print(f"Угол 3.0 in range5 = [1.0 - 3.0): {test_angle3 in range5}") # False

# Тестируем диапазон (метод _contains_range)
sub_range = AngleRange(start=1.5, end=2.5)
print(f"Диапазон [1.5 - 2.5] in range1 = {range1}: {sub_range in range1}") # True

# Частично перекрывающийся диапазон (проверка упрощенная, обе границы должны быть внутри)
overlap_range = AngleRange(start=0.9, end=2.5)
print(f"Диапазон [0.9 - 2.5] in range1 = {range1}: {overlap_range in range1}") # False (0.9 вне)


print("\n### Операции с Диапазонами")

range_A = AngleRange(start=1.0, end=3.0) # [1.0 - 3.0]
range_B = AngleRange(start=2.5, end=4.0) # [2.5 - 4.0] (Перекрывается)
range_C = AngleRange(start=5.0, end=6.0) # [5.0 - 6.0] (Не перекрывается)

# __add__ (Объединение)
merged = range_A + range_B # [1.0 - 4.0]
print(f"range_A + range_B (объединение): {range_A} + {range_B} = {merged}") # Возвращает список из одного диапазона
not_merged = range_A + range_C
print(f"range_A + range_C (нет объединения): {range_A} + {range_C} = {not_merged}") # Возвращает список из двух диапазонов

# __sub__ (Разность) - Упрощенная реализация
range_D = AngleRange(start=1.5, end=2.5, start_inclusive=0, end_inclusive=1) # [1.5 - 2.5] (Полностью внутри range_A)
sub_result = range_A - range_D
print(f"range_A - range_D (разность): {range_A} - {range_D} = {sub_result}") # Возвращает два диапазона: [1.0-1.5], [2.5-3.0]

# Разность, когда нет вхождения
# sub_no_change = range_A - range_C
# print(f"range_A - range_C (нет изменения): {range_A} - {range_C} = {sub_no_change}") # Возвращает [range_A]


print("\n### Сравнение (__eq__)")

# range1: [1.0 - 3.0]
range4 = AngleRange(start=1.0, end=3.0) # [1.0 - 3.0]

print(f"range1 == range4: {range1} == {range4}: {range1 == range4}") # True (точное совпадение)
print(f"range1 == range2: {range1} == {range2}: {range1 == range2}") # False (разные границы)

# Разница во включенности
range5 = AngleRange(start=1.0, end=3.0, end_inclusive=False) # [1.0 - 3.0)
print(f"range1 == range5: {range1} == {range5}: {range1 == range5}") # False
# endregion
