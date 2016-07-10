#!/usr/bin/env python
import arrow
import click
import os

TODO_DIR = os.path.expanduser('~/Dropbox/todo')
TODO_FILE = os.path.join(TODO_DIR, 'todo.txt')

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
        self.todos.append(todo)

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
    TODOS.report(search=search)

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

TODOS = TodoFile(TODO_FILE)

if __name__ == '__main__':
    cli()

