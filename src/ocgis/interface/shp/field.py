from ocgis.interface.base.field import Field
import numpy as np


class ShpField(Field):
    
    def _get_value_from_source_(self,data,attribute_name):
        data.load_geoms = False
        try:
            ret = np.array([row['properties'][attribute_name] for row in data])
            ret.reshape(1,1,1,1,len(ret))
        finally:
            data.load_geoms = True
        return(ret)