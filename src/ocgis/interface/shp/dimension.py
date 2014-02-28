from ocgis.interface.base.dimension.base import VectorDimension
import numpy as np


class ShpVectorDimension(VectorDimension):
    
    def __init__(self,*args,**kwds):
        VectorDimension.__init__(self, *args, **kwds)
        
        ## the uid parameter is directly related to the unique UGID parameter in
        ## the input shapefile. the parameter is required to avoid reading from
        ## the shapefile multiple times.
        try:
            assert(self._uid is not None)
        except AssertionError:
            msg = 'The "uid" argument is required for shapefile dimensions.'
            raise(ValueError(msg))
    
    def _set_value_from_source_(self):
        
        if self.name in ('POINT','POLYGON'):
            self._value = np.atleast_2d(np.ma.array(list((row['geom'] for row in self._data)),mask=False))
        else:
            raise(NotImplementedError(self.name))