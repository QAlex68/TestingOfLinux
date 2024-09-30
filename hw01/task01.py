# Задание 1.
# Условие: Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess


def checkout(directory: str, find_name: str) -> bool:
    result = subprocess.run(directory, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        lst = out.split("\n")
        if find_name in lst:
            return True
        return False
    return False


if __name__ == '__main__':
    print(checkout('cat /etc/os-release', 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'))
