import shutil # Модуль для высокоуровневых операций (копирование, перемещение)
import os

source_file = "dummy.txt" # Исходный файл
target_dir = "test_dir"   # Папка назначения (которую мы создали в прошлом скрипте)

# Создаем тестовый файл, чтобы нам было что перемещать
with open(source_file, "w") as f:
    f.write("Тестовый файл")

# Проверяем, существуют ли и сам файл, и папка, куда мы хотим его перенести
if os.path.exists(source_file) and os.path.exists(target_dir):
    # shutil.move() работает как "Вырезать и Вставить" (Cut & Paste). 
    # Он убирает файл из старого места и кладет в 'target_dir'.
    destination = shutil.move(source_file, target_dir)
    print(f"Файл перемещен по пути: {destination}")