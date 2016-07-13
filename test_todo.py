import arrow
import pytest
import todo
from todo import ParseError

def test_parse():
    test_date_1 = arrow.get('2013-05-05', 'YYYY-MM-DD')
    test_date_2 = arrow.get('2016-12-03', 'YYYY-MM-DD')
    today = arrow.get(arrow.now().format('YYYY-MM-DD'), 'YYYY-MM-DD')

    assert todo.parse_line('2013-05-05  This is a test ') == {
            'text': 'This is a test',
            'done': False,
            'created': test_date_1,
            'completed': None,
            'priority': 50,
            }
    assert todo.parse_line('2013-05-05  This is a test ') == {
            'text': 'This is a test',
            'done': False,
            'created': test_date_1,
            'completed': None,
            'priority': 50,
            }
    assert todo.parse_line('(A) This is a test ') == {
            'text': 'This is a test',
            'done': False,
            'created': today,
            'completed': None,
            'priority': 90,
            }
    assert todo.parse_line('x (B)   This is a test ').priority == 80
    assert todo.parse_line('x (C)   This is a test ').priority == 70
    assert todo.parse_line('x 2013-05-05   2016-12-03  This is a test ') == {
            'text': 'This is a test',
            'done': True,
            'created': test_date_1,
            'completed': test_date_2,
            'priority': 50,
            }

