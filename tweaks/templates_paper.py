from info.ins import datasets
from info.vis import visualization as vis


img = datasets.blackcurrant()
vis.Canvas.play(data=img, fig_type='image')
