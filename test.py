import inspect


def a():
    print(inspect.stack()[1].function)


def minasan():
    a()


minasan()
