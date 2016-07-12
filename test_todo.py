import todo

def test_parse():
    assert todo.parse_line('This is a test ') == { 'text': 'This is a test', 'done': False }
    assert todo.parse_line('x   This is a test ') == { 'text': 'This is a test', 'done': True }
