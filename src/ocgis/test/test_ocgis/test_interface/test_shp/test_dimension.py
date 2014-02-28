from ocgis.test.base import TestBase
from ocgis.util.shp_cabinet import ShpCabinet, ShpCabinetIterator
from ocgis.interface.shp.dimension import ShpVectorDimension
from shapely.geometry.polygon import Polygon
import numpy as np


class TestShpDimension(TestBase):
    
    def test_constructor(self):
        sc = ShpCabinet()
        uri = sc.get_shp_path('state_boundaries')
        data = ShpCabinetIterator(path=uri,select_ugid=[23,18])
        sd = ShpVectorDimension(data=data,name='SPATIAL')
        self.assertEqual(sd._value,None)
        self.assertEqual(sd.value.shape,(1,2))
        self.assertEqual(map(type,sd.value.flat),[Polygon,Polygon])
        
        ## the internal iterator should be able to be used again
        sd2 = ShpVectorDimension(data=data,name='SPATIAL')
        self.assertEqual(sd2._value,None)
        self.assertEqual(sd2.value.shape,(1,2))
        self.assertEqual(map(type,sd2.value.flat),[Polygon,Polygon])
        self.assertFalse(np.may_share_memory(sd.value,sd2.value))
