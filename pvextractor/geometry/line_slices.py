import numpy as np

from scipy.ndimage import map_coordinates


def extract_line_slice(cube, x, y, order=3, respect_nan=True):
    """
    Given an array with shape (z, y, x), extract a (z, n) slice by
    interpolating at n (x, y) points.

    All units are in *pixels*.

    .. note:: If there are NaNs in the cube, they will be treated as zeros when
              using spline interpolation.

    Parameters
    ----------
    cube : `~numpy.ndarray`
        The data cube to extract the slice from
    curve : list or tuple
        A list or tuple of (x, y) pairs, with minimum length 2
    order : int, optional
        Spline interpolation order. Set to ``0`` for nearest-neighbor
        interpolation.

    Returns
    -------
    slice : `numpy.ndarray`
        The (z, d) slice
    """

    if order == 0:

        slice = cube[:, np.round(y).astype(int), np.round(x).astype(int)]

    else:

        nx = len(x)
        nz = cube.shape[0]

        zi = np.outer(np.arange(nz, dtype=int), np.ones(nx))
        xi = np.outer(np.ones(nz), x)
        yi = np.outer(np.ones(nz), y)

        slice = map_coordinates(np.nan_to_num(cube), [zi,yi,xi], order=order, cval=np.nan)

        if respect_nan:
            slice_bad = map_coordinates(np.nan_to_num(np.isnan(cube).astype(int)),
                                        [zi,yi,xi], order=order)
            slice[np.nonzero(slice_bad)] = np.nan

    return slice

