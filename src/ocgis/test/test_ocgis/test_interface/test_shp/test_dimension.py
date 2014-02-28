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
        svd = self.get_shpvector_dimension()
        geom = SpatialGeometryDimension(polygon=svd)
        sd = SpatialDimension(geom=geom)
        return(sd)
    
    def get_shpvector_dimension(self,data=None):
        data = data or self.get_data()
        src_idx = np.array(data.select_ugid).reshape(1,2)
        uid = src_idx.copy()
        svd = ShpVectorDimension(data=data,name='POLYGON',src_idx=src_idx,uid=uid)
        return(svd)
    
    def run_value_tsts(self,value_object):
        self.assertEqual(value_object._value,None)
        self.assertEqual(value_object.value.shape,(1,2))
        self.assertEqual(map(type,value_object.value.flat),[Polygon,Polygon])


class TestShpDimension(AbstractTestShpDimension):
    
    def test_constructor(self):
        data = self.get_data()
        sd = self.get_shpvector_dimension(data=data)
        self.run_value_tsts(sd)
        
        ## the internal iterator should be able to be used again
        sd2 = self.get_shpvector_dimension(data=data)
        self.run_value_tsts(sd2)
        self.assertFalse(np.may_share_memory(sd.value,sd2.value))
        
    def test_uid(self):
        sd = self.get_spatial_dimension()
        self.assertEqual(sd._uid,None)
        self.assertEqual(sd.geom._uid,None)
        uid = np.ma.array([[23,18]])
        self.assertNumpyAll(sd.geom.polygon._uid,uid)
        self.assertNumpyAll(sd.uid,uid)
        
    def test_uid_is_required(self):
        data = self.get_data()
        src_idx = np.array(data.select_ugid).reshape(1,2)
        with self.assertRaises(ValueError):
            ShpVectorDimension(data=data,name='POLYGON',src_idx=src_idx)
        
    def test_SpatialDimension(self):
        sd = self.get_spatial_dimension()
        self.run_value_tsts(sd.geom.polygon)
        self.assertEqual(sd.geom.shape,sd.geom.polygon.shape)
