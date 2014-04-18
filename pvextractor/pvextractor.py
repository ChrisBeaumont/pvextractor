import numpy as np
from scipy.ndimage import map_coordinates
from astropy.wcs import WCS
from astropy import units as u
from .utils.wcs_utils import assert_independent_3rd_axis, wcs_spacing
from .geometry import extract_slice

def extract_pv_slice_hdu(hdu, path, **kwargs):
    """
    Create a PV diagram starting from a set of WCS coordinates

    Parameters
    ----------
    hdu: astropy.io.fits.PrimaryHDU object
        The cube HDU
    endpoints: tuple of float pairs
        The endpoints along which to sample specified in the world coordinates
        of the FITS header
    spacing: float or astropy quantity
        The spacing between samples in the output PV diagram.  Assumed to be
        pixels unless valid units are given
    """

    wcs = WCS(hdu.header)
    assert_independent_3rd_axis(wcs)

    # convert the endpoints from WCS to pixels by assuming that the 3rd axis is
    # independent
    px,py = wcs.wcs_world2pix([[a,b,wcs.wcs.crval[2]]
                               for a,b in zip(x,y)], 0)[:,:2]

    return pvdiagram(hdu.data, px, py,
                     spacing=wcs_spacing(wcs, spacing)
                     **kwargs)

def extract_pv_slice(cube, path, spacing=1.0, order=3, respect_nan=True, width=None):
    """
    Given a position-position-velocity cube with dimensions (nv, ny, nx), and
    a path, extract a position-velocity slice.

    Alternative implementations:
        gipsy::sliceview
        karma::kpvslice
        casaviewer::slice

    Parameters
    ----------
    path : `Path`
        The path along which to define the position-velocity slice
    spacing : float
        The position resolution in the final position-velocity slice.
    order : int, optional
        Spline interpolation order when using line paths. Does not have any
        effect for polygon paths.
    respect_nan : bool, optional
        If set to `False`, NaN values are changed to zero before computing
        the slices. If set to `True`, in the case of line paths a second
        computation is performed to ignore the NaN value while interpolating,
        and set the output values of NaNs to NaN.

    Returns
    -------
    slice : `numpy.ndarray`
        The position-velocity slice
    """

    pv_slice = extract_slice(cube, path, order=order, respect_nan=respect_nan)

    return pv_slice
