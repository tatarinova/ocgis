from ocgis.calc import base
import numpy as np
from ocgis import constants
from ocgis.util.helpers import iter_array


class Convolve1D(base.AbstractUnivariateFunction, base.AbstractParameterizedFunction):
    key = 'convolve_1d'
    parms_definition = {'v': np.ndarray, 'mode': str}
    description = 'Perform a one-dimensional convolution for each grid element along the time axis. See: http://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html'
    dtype = constants.np_float

    def calculate(self, values, v=None, mode='same'):
        """
        :param values: Array containing variable values.
        :type values: :class:`numpy.ma.core.MaskedArray`
        :param v: The one-dimensional array to convolve with ``values``.
        :type v: :class:`numpy.core.multiarray.ndarray`
        :param str mode: The convolution mode. See: http://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html
        :rtype: :class:`numpy.ma.core.MaskedArray`
        :raises: AssertionError
        """

        # 'full' is not supported as this would add dates to the temporal dimension
        assert(mode in ('same', 'valid'))
        assert(len(values.shape) == 5)

        # just to be safe, convert the second array to the same input data types as the values
        v = v.astype(values.dtype)

        # valid will have less values than the input as this checks if the two convolved arrays completely overlap
        shape_fill = list(values.shape)
        if mode == 'valid':
            shape_fill[1] = max(values.shape[1], v.shape[0]) - min(values.shape[1], v.shape[0]) + 1
        fill = np.zeros(shape_fill)

        # perform the convolution on the time axis
        itr = iter_array(values)
        for ie, it, il, ir, ic in itr:
            a = values[ie, :, il, ir, ic]
            fill[ie, :, il, ir, ic] = np.convolve(a, v, mode=mode)

        if mode == 'valid':
            # generate the mask for the output data and convert the output to a masked array
            mask = np.empty(fill.shape, dtype=bool)
            mask[...] = values.mask[0, 0, 0, :, :]
            fill = np.ma.array(fill, mask=mask)

            # identify where the two arrays completely overlap and collect the indices to subset the field object
            # attached to the calculation object
            self.field = self.field[:, slice(0, 0-(v.shape[0]-1)), :, :, :]
        else:
            # same does not modify the output array size
            fill = np.ma.array(fill, mask=values.mask)

        return fill


class MovingAverage(Convolve1D):
    key = 'moving_average'
    parms_definition = {'k': int, 'mode': str}
    description = ('Calculate a moving window average alone the time axis with window of width ``k``. The optional ',
                   'parameter ``mode`` defaults to ``same``. ``valid`` is also available in which case the time axis ',
                   'will be truncated.')
    dtype = constants.np_float

    def calculate(self, values, k=None, mode='same'):
        # the second convolution array will generate a moving average
        v = np.ones((k,))/k
        return super(MovingAverage, self).calculate(values, v=v, mode=mode)


class FrequencyPercentile(base.AbstractUnivariateSetFunction,base.AbstractParameterizedFunction):
    key = 'freq_perc'
    parms_definition = {'percentile':float}
    description = 'The percentile value along the time axis. See: http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.percentile.html.'
    dtype = constants.np_float
    
    def calculate(self,values,percentile=None):
        '''
        :param percentile: Percentile to compute.
        :type percentile: float on the interval [0,100]
        '''
        ret = np.percentile(values,percentile,axis=0)
        return(ret)


class Max(base.AbstractUnivariateSetFunction):
    description = 'Max value for the series.'
    key = 'max'
    dtype = constants.np_float
    
    def calculate(self,values):
        return(np.ma.max(values,axis=0))


class Min(base.AbstractUnivariateSetFunction):
    description = 'Min value for the series.'
    key = 'min'
    dtype = constants.np_float
    
    def calculate(self,values):
        return(np.ma.min(values,axis=0))

    
class Mean(base.AbstractUnivariateSetFunction):
    description = 'Compute mean value of the set.'
    key = 'mean'
    dtype = constants.np_float
    
    def calculate(self,values):
        return(np.ma.mean(values,axis=0))
    
    
class Median(base.AbstractUnivariateSetFunction):
    description = 'Compute median value of the set.'
    key = 'median'
    dtype = constants.np_float
    
    def calculate(self,values):
        return(np.ma.median(values,axis=0))
    
    
class StandardDeviation(base.AbstractUnivariateSetFunction):
    description = 'Compute standard deviation of the set.'
    key = 'std'
    dtype = constants.np_float
    
    def calculate(self,values):
        return(np.ma.std(values,axis=0))
