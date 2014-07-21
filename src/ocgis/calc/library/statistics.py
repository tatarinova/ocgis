import itertools
import numpy as np
from ocgis.calc import base
from ocgis import constants
from ocgis.calc.base import AbstractUnivariateFunction, AbstractParameterizedFunction
from ocgis.calc.library.math import Convolve1D
from ocgis.util.helpers import iter_array


class MovingAverage(AbstractUnivariateFunction, AbstractParameterizedFunction):
    key = 'moving_average'
    parms_definition = {'k': int, 'mode': str}
    description = ('Calculate a moving window average alone the time axis with window of width ``k``. The optional ',
                   'parameter ``mode`` defaults to ``valid`` which will truncate the time axis. ``same`` is also ',
                   'available which outputs the same time dimension. The moving window is centered on the time coordinate.',
                   '``k`` must be odd and greater than 3.')
    dtype = constants.np_float

    def calculate(self, values, k=None, mode='valid'):
        """
        :param values: Array containing variable values.
        :type values: :class:`numpy.ma.core.MaskedArray`
        :param k: The width of the moving window. ``k`` must be odd and greater than three.
        :type k: int
        :param str mode: See: http://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html. The output mode
         ``full`` is not supported.
        :rtype: :class:`numpy.ma.core.MaskedArray`
        :raises: AssertionError, NotImplementedError
        """

        mean = np.ma.mean

        # 'full' is not supported as this would add dates to the temporal dimension
        assert(mode in ('same', 'valid'))
        assert(len(values.shape) == 5)

        fill = values.copy()

        # perform the moving average on the time axis
        itr = iter_array(values)
        axes = [0, 2, 3, 4]
        itrs = [range(values.shape[axis]) for axis in axes]
        for ie, il, ir, ic in itertools.product(*itrs):
            values_slice = values[ie, :, il, ir, ic]
            build = True
            for origin, values_kernel in self._iter_kernel_values_(values_slice, k, mode=mode):
                if build:
                    idx_start = origin
                    build = False
                fill[ie, origin, il, ir, ic] = mean(values_kernel)

        if mode == 'valid':
            self.field = self.field[:, idx_start:origin+1, :, :, :]
            fill = fill[:, idx_start:origin+1, :, :, :]
        elif mode == 'same':
            pass
        else:
            raise NotImplementedError(mode)

        return fill

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
        elif mode == 'same':
            while True:
                start = origin - shift
                stop = origin + shift + 1
                if start < 0:
                    start = 0
                yield origin, values[start:stop]
                origin += 1
                if origin == shape_values:
                    raise StopIteration
        else:
            raise NotImplementedError(mode)


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
