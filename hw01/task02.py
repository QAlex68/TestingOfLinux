# Задание 2. (повышенной сложности)
# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка string.punctuation
# модуля string). В этом режиме должно проверяться наличие слова в выводе.


import subprocess
import string


def checkout(directory: str, find_name: str, use_word_mode: bool = False) -> bool:
    result = subprocess.run(directory, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        if use_word_mode:
            # Удаляем пунктуацию
            translator = str.maketrans('', '', string.punctuation)
            cleaned_output = out.translate(translator)
            words = cleaned_output.split()
            return find_name in words
        else:
            lst = out.split("\\n")
            if find_name in lst:
                return True
            return False
    return False


if __name__ == '__main__':
    # Проверка в обычном режиме
    print(checkout('cat /etc/os-release', 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'))

    # Проверка в режиме поиска слова
    print(checkout('cat /etc/os-release', '22', use_word_mode=True))
