import inspect

from typing import Callable, Iterator

def show_func(func: Callable)-> None:
    print(inspect.getsource(func))

