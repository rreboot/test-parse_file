import gzip
import re
from typing import List


def read_file(path: str) -> str:
    """ Чтение файла или архива построчно.

    Parameters
    ----------
    path : str
        Путь к файлу.

    Yields
    -------
    line : str
        Строка файла.

    """
    ext = path.split('.')[-1]

    if ext == 'gz':
        file = gzip.open(path, 'rt')
    else:
        file = open(path, 'r')
    for line in file:
        yield line
    file.close()


def is_comment(line: str) -> bool:
    if line.startswith('#'):
        return True
    return False


def prepare_line(raw_line: str) -> str:
    """ Подготовка строки - удаление пустых символов. """

    return re.sub(r'[ \t\f\v\r]+', ' ', raw_line).strip()


def parse_line(line: str) -> tuple:
    """ Получение из строки ключа и значения. По умолчанию - None, line."""
    parts = line.split(': ')
    key = None

    if len(parts) > 2:
        raise Exception('Не удалось распарсить строку: частей больше 2')

    if len(parts) == 1:
        value = line
    else:
        key, value = parts

    return key, value


def parse_file(path: str) -> List[dict]:
    """
    new_doc_flag - флаг, для определения начала нового документа;
    key - буфер для хранения предыдущего ключа.

    """
    documents: List[dict] = []
    key: str = ''
    new_doc_flag: bool = True
    doc: dict = dict()

    for raw_line in read_file(path):
        line = prepare_line(raw_line)

        if is_comment(line):
            continue

        if not line:
            if new_doc_flag:
                continue
            else:
                documents.append(doc)
                doc = {}
                new_doc_flag = True
        else:
            new_doc_flag = False
            new_key, value = parse_line(line)

            if new_key:
                if new_key == key:
                    doc[key] += '\n' + value
                else:
                    key = new_key
                    doc[key] = value
            else:
                doc[key] += '\n' + value

    return documents


if __name__ == '__main__':
    parsed_data = parse_file('example.txt')
    for document in parsed_data:
        print(document)
