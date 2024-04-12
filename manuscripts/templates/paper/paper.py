import numpy as np
from numpy import ndarray
img = np.random.random((50, 60))


def scalar(x: ndarray) -> ndarray:
    _mean, _std = np.mean(x), np.std(x)
    return (x - _mean) / _std


norm_img = scalar(img)
print(norm_img.shape)