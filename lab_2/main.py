from printer_class import *
sys.stdout.write(AnsiCodes.CLEAR_SCREEN)

Printer.load_font("font7.json")

Printer.print_static("ПРИВЕТ", Color.RED, (10, 10), "0")


with Printer(Color.GREEN, (1, 1), "0") as p:
    p.print("С НАСТУПАЮЩИМ МИХАИЛ ДМИТРИЕВИЧ")

# 2. Меняем шрифт на ходу (если есть второй файл)
# if os.path.exists("font7.json"):
#     Printer.load_font("font7.json")
#     Printer.print_static("ДАЙТЕ ТАНК", Color.BLUE, (5, 25), "0")
