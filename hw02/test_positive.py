# Задание 1.
# Условие: Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
# *Задание 2. *
# •Установить пакет для расчёта crc32
# sudo apt install libarchive-zip-perl
# •Доработать проект, добавив тест команды расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.

import subprocess
import zlib

tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"
folder2 = "/home/user/folder2"


# Расчет контрольной суммы CRC32 для файла, параметр cmd
def crc32(cmd):
    with open(cmd, 'rb') as g:  # открываем для чтения в бинарном режиме
        my_hash = 0
        while True:
            s = g.read(65536)  # читаем блоками 65536 байт
            if not s:
                break
            my_hash = zlib.crc32(s, my_hash)  # обновляем значение хеша для каждого блока
        return "%08X" % (my_hash & 0xFFFFFFFF)  # возвращаем в 16-теричном формате с ведущими нулями


# checkout для позитивных тестов
def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


# создание архива arx2.7z в каталоге out и его наличие
def test_step1():
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "test1 FAIL"


# разархивирование arx2.7z в folder1 и наличие файлов one и two
def test_step2():
    result1 = checkout(f"cd {out}; 7z e arx2.7z -o{folder1} -y", "Everything is Ok")
    result2 = checkout(f"cd {folder1}; ls", "one")
    result3 = checkout(f"cd {folder1}; ls", "two")
    assert result1 and result2 and result3, "test2 FAIL"


# проверка списка файлов в архиве arx2.7z
def test_step3():
    result1 = checkout(f"cd {out}; 7z l arx2.7z", "")
    result2 = checkout(f"cd {out}; 7z l arx2.7z", "one")
    result3 = checkout(f"cd {out}; 7z l arx2.7z", "two")
    assert result1 and result2 and result3, "test3 FAIL"


# проверка разархивирования arx2.7z в folder2
def test_step4():
    result1 = checkout(f"cd {out}; 7z x arx2.7z -o{folder2}", "Everything is Ok")
    result2 = checkout(f"cd {folder2}; ls", "one")
    result3 = checkout(f"cd {folder2}; ls", "two")
    assert result1 and result2 and result3, "test4 FAIL"


# сравнение контрольной суммы (функция crc32), с результатом выполнения команды crc32 из командной строки
def test_step5():
    result1 = crc32(f'{out}/arx2.7z').lower()
    assert checkout(f'crc32 {out}/arx2.7z', result1), "test5 FAIL"


# проверка целостности архива с помощью команды 7z t
def test_step6():
    assert checkout(f"cd {out}; 7z t arx2.7z", "Everything is Ok"), "test6 FAIL"


# проверка обновление архива arx2.7z
def test_step7():
    assert checkout(f"cd {tst}; 7z u {out}/arx2.7z", "Everything is Ok"), "test7 FAIL"


# проверка удаления архива arx2.7z
def test_step8():
    assert checkout(f"cd {out}; 7z d arx2.7z", "Everything is Ok"), "test8 FAIL"
