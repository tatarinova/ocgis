from ocgis.test.base import TestBase
from ocgis.util.shp_cabinet import ShpCabinet, ShpCabinetIterator
from ocgis.interface.shp.dimension import ShpVectorDimension
from shapely.geometry.polygon import Polygon
import numpy as np
from ocgis.interface.base.dimension.spatial import SpatialDimension,\
    SpatialGeometryDimension
import abc


class AbstractTestShpDimension(TestBase):
    __metaclass__ = abc.ABCMeta
    
    def get_data(self):
        sc = ShpCabinet()
        uri = sc.get_shp_path('state_boundaries')
        data = ShpCabinetIterator(path=uri,select_ugid=[23,18])
        return(data)
    
    def get_spatial_dimension(self):
        data = self.get_data()
        src_idx = np.array(data.select_ugid).reshape(1,2)
        svd = ShpVectorDimension(data=data,name='POLYGON',src_idx=src_idx)
        geom = SpatialGeometryDimension(polygon=svd)
        sd = SpatialDimension(geom=geom)
        return(sd)
    
    def run_value_tsts(self,value_object):
        self.assertEqual(value_object._value,None)
        self.assertEqual(value_object.value.shape,(1,2))
        self.assertEqual(map(type,value_object.value.flat),[Polygon,Polygon])


class TestShpDimension(AbstractTestShpDimension):
    
    def test_constructor(self):
        data = self.get_data()
        src_idx = np.array(data.select_ugid)
        sd = ShpVectorDimension(data=data,name='POLYGON',src_idx=src_idx)
        self.run_value_tsts(sd)
        
        ## the internal iterator should be able to be used again
        sd2 = ShpVectorDimension(data=data,name='POLYGON',src_idx=src_idx)
        self.run_value_tsts(sd2)
        self.assertFalse(np.may_share_memory(sd.value,sd2.value))
        
    def test_uid(self):
        sd = self.get_spatial_dimension()
        self.assertEqual(sd._uid,None)
        self.assertEqual(sd.geom._uid,None)
        self.assertEqual(sd.geom.polygon._uid,None)
        print sd.uid
        self.assertNumpyAll(sd.uid,np.array([[23,18]]))
        
    def test_SpatialDimension(self):
        sd = self.get_spatial_dimension()
        self.run_value_tsts(sd.geom.polygon)
        self.assertEqual(sd.geom.shape,sd.geom.polygon.shape)
