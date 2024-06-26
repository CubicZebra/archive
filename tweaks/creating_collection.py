# conf related
from info.me import FuncTools, T, Null
from typing import Any
from info.vis import visualization as vis
import numpy as np
import time
import pyqtgraph as pg
np.random.seed(10)  # maybe vary


def py_func(**kw):
    time.sleep(0.1)
    return kw.get('data')



@FuncTools.attach_attr(docstring='rst', info_func=True, entry_tp=Any, return_tp=Any)
def info_func1(**kw):
    time.sleep(0.1)
    return kw.get('data')


@FuncTools.params_setting(data=T[Null: Any])
def info_func2(**kw):
    time.sleep(0.1)
    return kw.get('data')


@FuncTools.params_setting(data=T[Null: Any])
@FuncTools.attach_attr(docstring='rst', info_func=True, entry_tp=Any, return_tp=Any)
def info_func3(**kw):
    time.sleep(0.1)
    return kw.get('data')


res = np.array([[float(FuncTools.test_for(data=_, **{'~in_decorator': False})(func)()[-1][-8:]) for _ in range(30)]
                for func in [py_func, info_func1, info_func2, info_func3]])
func_names = ['NoDeco', 'FlowConf', 'ArgConf', 'FlowConf+ArgConf']
palettes = [pg.intColor(_, hues=4) for _ in range(4)]


vis.Canvas.play(data=res, fig_type='beeswarm', fig_configs=vis.FigConfigs.Beeswarm.update(name=func_names,
                                                                                        symbolBrush=palettes),
                cvs_left_label='time consumption (s)', cvs_legend=True)
vis.Canvas.play(data=res, fig_type='box', fig_configs=vis.FigConfigs.Box.update(name=func_names,
                                                                                brush=palettes),
                cvs_left_label='time consumption (s)', cvs_legend=True)


from info.me import Unit
from info.me import tensorn as tsn
from info.ins import datasets


crop, denoise, resample = [Unit(mappings=[_]) for _ in [tsn.cropper, tsn.gaussian_filter, tsn.resize]]
processing = crop >> denoise >> resample
prewitt, canny, log = [Unit(mappings=[_]) for _ in [tsn.prewitt_filter, tsn.canny_filter, 
                                                    tsn.laplacian_of_gaussian_filter]]
compare_experiment = processing >> (prewitt | canny | log)

config = {'k_shape': (5, 5), 'new_size': (450, 800), 'crop_range': [(0.7, 0.1), (0.99, 0.6)]}
p = compare_experiment.shadow(**config)
vis.Canvas.play(data=datasets.accent(), fig_type='image')
vis.Canvas.play(data=processing(data=datasets.accent(), **config), fig_type='image', cvs_size=(400, 520))
_ = [vis.Canvas.play(data=_, fig_type='image', cvs_size=(400, 520)) for _ in p(data=datasets.accent())]
