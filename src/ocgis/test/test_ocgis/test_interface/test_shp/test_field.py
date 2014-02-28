from ocgis.test.test_ocgis.test_interface.test_shp.test_dimension import AbstractTestShpDimension
from ocgis.interface.base.variable import Variable
from ocgis.interface.shp.field import ShpField
import numpy as np


class TestShpField(AbstractTestShpDimension):
    
    def test_constructor(self):
        data = self.get_data()
        var = Variable(name='UGID',data=data)
        sd = self.get_spatial_dimension()
        field = ShpField(spatial=sd,variables=var)
        self.assertEqual(sd.shape,(1,2))
        self.assertEqual(field.shape,(1,1,1,1,2))
        to_test = np.ma.array(self._select_ugid,mask=False).reshape(1,1,1,1,2)
        self.assertNumpyAll(field.variables['UGID'].value,to_test)
        import ipdb;ipdb.set_trace()