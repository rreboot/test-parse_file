from io import StringIO
from typing import List

import pytest

from main import parse_file, read_file


def test_output_type():
    result = parse_file('example.txt')

    assert isinstance(result, List)

    if result:
        assert isinstance(result[0], dict)
    else:
        assert result == []


def test_wrong_path():
    path = 'wrong-path'
    with pytest.raises(FileNotFoundError) as excinfo:
        next(read_file(path))
    print(excinfo.value)


def test_read_file(mocker):
    mocker.patch('builtins.open').return_value = StringIO('Some text')
    result = read_file('some file.txt')

    assert list(result) == ['Some text']
