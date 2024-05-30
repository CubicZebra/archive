def function1(pos: int, opt: int = 1, *args, **kwargs):
    print(pos, opt, len(args), len(kwargs))
    return pos + opt + len(args) + len(kwargs)


function1(2)                 # 2, 1, 0, 0
function1(2, 3)              # 2, 3, 0, 0
function1(2, 3, 4, 5)        # 2, 3, 2, 0
function1(2, kw1=5, kw2=6)   # 2, 1, 0, 2


def function2(**kw):
    return function1(
        kw.get('pos'),
        kw.get('opt', 1),
        *kw.get('args', ()),
        **kw.get('kwargs', {}),
    )

from info.me import FuncTools
from typing import Union, Any


@FuncTools.attach_attr(info_func=True,
                       entry_tp=Union[str, list[str]],
                       return_tp=Any)
def func1(**kw):
    _ = kw.get('data')
    ...
    return 0


func1(data='string0')               # valid, str
func1(data=['string1', 'string2'])  # valid, list[str]
func1(data=('string3', 'string4'))  # invalid, tuple[str, ...]
func1(data=50)                      # invalid, int
func1(data=['string5', 50])         # invalid, list[str | int]

...
if not isinstance(_, (str, list)):
    raise ValueError('...')
elif isinstance(_, list):
    if not all([isinstance(_v, str) for _v in _]):
        raise ValueError('...')
...


def doc_func(**kw):
    """
    documentation begin
    ... rst doc for main_func ...
    documentation end
    """
    ...

@FuncTools.attach_attr(docstring=doc_func)
def main_func(**kw):
    ...


from info.me import FuncTools, T, Null
from numpy import ndarray


@FuncTools.params_setting(data=T[Null: ndarray],
                          arg1=T[(.3, 60): tuple[float, int]],
                          arg2=T[0.7: (lambda x: 0 < x < 1)])
def func2(**kw):
    ...


import numpy as np


_sym = (lambda x: True if (x.ndim == 2 and
                           x.shape[0] == x.shape[1] and
                           np.allclose(x, x.T)) else False)
_pos = (lambda x: np.all(np.linalg.eigvals(x) > 0))
_semi_pos = (lambda x: np.all(np.linalg.eigvals(x) >= 0))


@FuncTools.params_setting(mat1=T[Null: _sym],
                          mat2=T[Null: _pos],
                          mat3=T[Null: _semi_pos])
def func3(**kw):
    ...


from info.me import Unit


crop, denoise, resample = [Unit(mappings=[_]) for _ in [...]]
processing = crop >> denoise >> resample
prewitt, canny, log = [Unit(mappings=[_]) for _ in [...]]
compare_experiment = processing >> (prewitt | canny | log)