from ocgis.interface.base.dimension.base import VectorDimension
import numpy as np


class ShpVectorDimension(VectorDimension):
    
    def _set_value_from_source_(self):
        
        if self.name in ('POINT','POLYGON'):
            self._value = np.atleast_2d(np.ma.array(list((row['geom'] for row in self._data)),mask=False))
        else:
            raise(NotImplementedError(self.name))