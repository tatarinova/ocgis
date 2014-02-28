from ocgis.test.test_ocgis.test_interface.test_shp.test_dimension import AbstractTestShpDimension
from ocgis.interface.base.variable import Variable
from ocgis.interface.shp.field import ShpField
import numpy as np


class TestShpField(AbstractTestShpDimension):
    
    def get_shpfield(self,select_ugid='default'):
        data = self.get_data(select_ugid=select_ugid)
        var = Variable(name='UGID',data=data)
        sd = self.get_spatial_dimension(data=data)
        field = ShpField(spatial=sd,variables=var)
        return(field)
    
    def test_constructor(self):
        field = self.get_shpfield()
        self.assertEqual(field.spatial.shape,(1,2))
        self.assertEqual(field.shape,(1,1,1,1,2))
        to_test = np.ma.array(self._select_ugid,mask=False).reshape(1,1,1,1,2)
        self.assertNumpyAll(field.variables['UGID'].value,to_test)
        self.assertEqual(field.temporal,None)
        self.assertEqual(field.level,None)
        self.assertEqual(field.realization,None)
        
    def test_get_iter(self):
        field = self.get_shpfield()
        self.assertEqual(len(list(field.get_iter())),2)

    def test_load_all_state_boundaries_in_field(self):
        field = self.get_shpfield(select_ugid=None)
        self.assertEqual(field.shape,(1,1,1,1,51))