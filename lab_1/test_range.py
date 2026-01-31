from angle_class import AngleRange, Angle
from math import pi

PI = pi

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

