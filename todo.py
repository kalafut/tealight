#!/usr/bin/env python
import arrow
import click
import os
import re

class ParseError(Exception):
    pass

TODAY = arrow.get(arrow.now().format('YYYY-MM-DD'), 'YYYY-MM-DD')
TODO_DIR = os.path.expanduser('~/Dropbox/todo')
TODO_FILE = os.path.join(TODO_DIR, 'todo.txt')

PRIORITY_MAP = {
    'A': 90,
    'B': 80,
    'C': 70,
    None: 50,
    }

#https://regex101.com/r/fR0dN9/3
TODO_LEGACY_RE = re.compile(r'^(?P<done>x +)?(?P<priority>\([A-Z]\) +)?(?P<created>\d{4}-\d\d-\d\d +)?(?P<completed>\d{4}-\d\d-\d\d)? *(?P<text>.*?) *$')

class dotdict(dict):
    """Make for less verbose dict syntax"""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Basic data structures

def parse_file(name):
    todos = []
    with open(name) as f:
        for line in f:
            todos.append(parse_line(line))
    return todos

def write_file(name, todos):
    with open(name, 'w') as f:
        for todo in todos:
            f.write(render_string(todo) + '\n')

def render_string(todo):
    if todo.done:
        return 'x ' + todo.text
    else:
        return todo.text

def parse_line(line):
    m = TODO_LEGACY_RE.match(line)
    if not m:
        raise ParseError()

    vals = dotdict(m.groupdict())
    for k, v in vals.items():
        if v:
            vals[k] = v.strip()
            if k == 'priority':
                vals[k] = v[1]

    priority = PRIORITY_MAP[vals.priority]

    return dotdict({
        'done': vals.done == 'x',
        'text': vals.text,
        'created': arrow.get(vals.created, 'YYYY-MM-DD') if vals.created else TODAY,
        'completed': arrow.get(vals.completed, 'YYYY-MM-DD') if vals.completed else None,
        'priority': priority,
        })

def print_report(todos, search=''):
    line = 1
    for todo in todos:
        if search in todo.text and not todo.done:
            print '{} {}'.format(line, render_string(todo))
        line += 1
    print

class Todo:
    def __init__(self, line, prepend_date=False):
        self.text = ''
        self.done = False
        self.valid = self.parse_line(line)
        if prepend_date:
            self.text = '{} {}'.format(arrow.now().format('YYYY-MM-DD'), self.text)

    def parse_line(self, line):
        line = line.strip()
        if line.startswith('x '):
            self.done = True
            line = line[2:].strip()
        self.text = line
        return True

    def render(self):
        if self.done:
            return 'x ' + self.text
        else:
            return self.text

class TodoFile:
    def __init__(self, name):
        self.name = name
        self.todos = []
        self.parse_file()

    def parse_file(self):
        with open(self.name) as f:
            for line in f:
                todo = Todo(line)
                if todo.valid:
                    self.todos.append(todo)

    def write_file(self):
        with open(self.name, 'w') as f:
            for todo in self.todos:
                f.write(todo.render() + '\n')

    def add(self, todo):
        self.todos.insert(0, todo)

    def report(self, search=''):
        line = 1
        for todo in self.todos:
            if search in todo.text and not todo.done:
                print '{} {}'.format(line, todo.render())
            line += 1
        print

@click.group()
def cli():
    pass

@cli.command()
@click.argument('task', nargs=-1)
def add(task):
    todo = Todo(' '.join(task), prepend_date=True)
    TODOS.add(todo)
    TODOS.write_file()

@cli.command()
def addm():
    while True:
        line = raw_input()
        if not line:
            break
        todo = Todo(line, prepend_date=True)
        TODOS.add(todo)
        TODOS.write_file()

@cli.command()
@click.argument('search', default='')
def ls(search):
    print_report(TODOS2, search)

@cli.command()
@click.argument('ids', nargs=-1)
def rm(ids):
    ids = sorted(list(ids), reverse=True)
    for id in ids:
        TODOS.todos.pop(int(id)-1)
        TODOS.write_file()

@cli.command()
@click.argument('id')
def do(id):
    TODOS.todos[int(id)-1].done = True
    TODOS.write_file()

if __name__ == '__main__':
    TODOS = TodoFile(TODO_FILE)
    TODOS2 = parse_file(TODO_FILE)

    cli()

