import arrow
import pytest
from todo import Todo, ParseError

def test_parse():
    test_date_1 = arrow.get('2013-05-05', 'YYYY-MM-DD')
    test_date_2 = arrow.get('2016-12-03', 'YYYY-MM-DD')
    today = arrow.get(arrow.now().format('YYYY-MM-DD'), 'YYYY-MM-DD')

    todo = Todo('2013-05-05  This is a test ')
    assert todo.text == 'This is a test'
    assert todo.done is False
    assert todo.created == test_date_1
    assert todo.completed is None
    assert todo.priority == 50

    todo = Todo('(A) This is a test ')
    assert todo.priority == 90
    assert todo.created == today

    assert Todo('x (B)   This is a test ').priority == 80
    assert Todo('x (C)   This is a test ').priority == 70

    todo = Todo('x 2013-05-05   2016-12-03  This is a test ')
    assert todo.done is True
    assert todo.created == test_date_1
    assert todo.completed == test_date_2

