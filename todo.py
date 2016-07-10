#!/usr/bin/env python
import arrow
import click
import os

TODO_DIR = os.path.expanduser('~/Dropbox/todo')
TODO_FILE = os.path.join(TODO_DIR, 'todo.txt')


class Todo:
    def __init__(self, line, prepend_date=False):
        self.text = ''
        self.valid = self.parse_line(line)
        if prepend_date:
            self.text = '{} {}'.format(arrow.now().format('YYYY-MM-DD'), self.text)

    def parse_line(self, line):
        self.text = line.strip()
        return True

class TodoFile:
    todo = None

    @classmethod
    def init(cls):
        if not cls.todo:
            cls.todo = TodoFile(TODO_FILE)

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
                f.write(todo.text + '\n')

    def add(self, todo):
        self.todos.append(todo)

    def report(self):
        line = 1
        for todo in self.todos:
            print '{} {}'.format(line, todo.text)
            line += 1

        print

@click.group()
def cli():
    pass

@cli.command()
@click.argument('task', nargs=-1)
def add(task):
    todo = Todo(' '.join(task), prepend_date=True)
    TodoFile.todo.add(todo)
    TodoFile.todo.write_file()

@cli.command()
def ls():
    TodoFile.todo.report()

@cli.command()
@click.argument('id')
def rm(id):
    TodoFile.todo.todos.pop(int(id)-1)
    TodoFile.todo.write_file()

if __name__ == '__main__':
    TodoFile.init()
    cli()

