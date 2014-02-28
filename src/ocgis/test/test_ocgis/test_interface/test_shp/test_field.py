from ocgis.test.test_ocgis.test_interface.test_shp.test_dimension import AbstractTestShpDimension
from ocgis.interface.base.variable import Variable
from ocgis.interface.shp.field import ShpField


class TestShpField(AbstractTestShpDimension):
    
    def test_constructor(self):
        data = self.get_data()
        var = Variable(name='UGID',data=data)
        sd = self.get_spatial_dimension()
        field = ShpField(spatial=sd,variables=var)
        raise