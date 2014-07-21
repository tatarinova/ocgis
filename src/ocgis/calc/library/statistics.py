import numpy as np
from ocgis.calc import base
from ocgis import constants
from ocgis.calc.library.math import Convolve1D


class MovingAverage(Convolve1D):
    key = 'moving_average'
    parms_definition = {'k': int, 'mode': str}
    description = ('Calculate a moving window average alone the time axis with window of width ``k``. The optional ',
                   'parameter ``mode`` defaults to ``same``. ``valid`` is also available in which case the time axis ',
                   'will be truncated.')
    dtype = constants.np_float

    def calculate(self, values, k=None, mode='same'):
        """
        :param values: Array containing variable values.
        :type values: :class:`numpy.ma.core.MaskedArray`
        :param k: The width of the moving window.
        :type k: int
        :param str mode: The convolution mode. See: http://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html.
         The output mode ``full`` is not supported.
        :rtype: :class:`numpy.ma.core.MaskedArray`
        :raises: AssertionError
        """

        # the second convolution array will generate a moving average
        v = np.ones((k,))/k
        return super(MovingAverage, self).calculate(values, v=v, mode=mode)

    @staticmethod
    def _iter_kernel_values_(values, k, mode='valid'):
        assert(k % 2 != 0)
        assert(k >= 3)
        assert(len(values.shape) == 1)

        origin = 0
        shift = (k - 1)/2
        shape_values = values.shape[0]

        if mode == 'valid':
            while True:
                start = origin - shift
                if start < 0:
                    origin += 1
                    continue
                stop = origin + shift + 1
                if stop > shape_values:
                    raise StopIteration
                yield origin, values[start:stop]
                origin += 1
        else:
            while True:
                start = origin - shift
                stop = origin + shift + 1
                if start < 0:
                    start = 0
                yield origin, values[start:stop]
                origin += 1
                if origin == shape_values:
                    raise StopIteration


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
