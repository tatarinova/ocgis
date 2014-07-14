import pickle
import unittest
from ocgis.api.parms.definition import Calc, OutputFormat
from ocgis.calc.library.statistics import Mean, FrequencyPercentile, Convolve1D, MovingAverage
from ocgis.interface.base.variable import DerivedVariable, Variable
import numpy as np
import itertools
from ocgis.test.test_ocgis.test_interface.test_base.test_field import AbstractTestField
from ocgis.test.test_simple.test_simple import ToTest, nc_scope
import ocgis
from cfunits.cfunits import Units



class TestConvolve1D(AbstractTestField):

    def get_convolve1d_field(self, slice_stop=3):
        field = self.get_field(month_count=1, with_value=True)
        field = field[:, 0:slice_stop, :, :, :]
        field.variables['tmax'].value[:] = 1
        field.variables['tmax'].value.mask[:, :, :, 1, 1] = True
        return field

    def test_execute_same(self):
        """Test convolution with the 'same' mode (numpy default)."""

        field = self.get_convolve1d_field()
        parms = {'v': np.array([1, 1, 1])}
        cd = Convolve1D(field=field, parms=parms)
        self.assertDictEqual(cd._format_parms_(parms), parms)
        vc = cd.execute()
        self.assertNumpyAll(vc['convolve_1d'].value.mask, field.variables['tmax'].value.mask)
        self.assertEqual(vc['convolve_1d'].value.fill_value, field.variables['tmax'].value.fill_value)
        actual = '\x80\x02cnumpy.ma.core\n_mareconstruct\nq\x01(cnumpy.ma.core\nMaskedArray\nq\x02cnumpy\nndarray\nq\x03K\x00\x85q\x04U\x01btRq\x05(K\x01(K\x02K\x03K\x02K\x03K\x04tcnumpy\ndtype\nq\x06U\x02f4K\x00K\x01\x87Rq\x07(K\x03U\x01<NNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK\x00tb\x89T@\x02\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@U\x90\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00cnumpy.core.multiarray\n_reconstruct\nq\x08h\x03K\x00\x85U\x01b\x87Rq\t(K\x01)h\x06U\x02f8K\x00K\x01\x87Rq\n(K\x03U\x01<NNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK\x00tb\x89U\x08@\x8c\xb5x\x1d\xaf\x15Dtbtb.'
        actual = np.ma.loads(actual)
        self.assertNumpyAll(actual, vc['convolve_1d'].value, check_fill_value_dtype=False)

    def test_execute_valid(self):
        """Test convolution with the 'valid' mode."""
#todo: test field is appropriately modified in output from calculation engine
        #todo: add to docs
        field = self.get_convolve1d_field(slice_stop=4)
        parms = {'v': np.array([1, 1, 1]), 'mode': 'valid'}
        cd = Convolve1D(field=field, parms=parms)
        self.assertDictEqual(cd._format_parms_(parms), parms)
        vc = cd.execute()
        actual = '\x80\x02cnumpy.ma.core\n_mareconstruct\nq\x01(cnumpy.ma.core\nMaskedArray\nq\x02cnumpy\nndarray\nq\x03K\x00\x85q\x04U\x01btRq\x05(K\x01(K\x02K\x02K\x02K\x03K\x04tcnumpy\ndtype\nq\x06U\x02f4K\x00K\x01\x87Rq\x07(K\x03U\x01<NNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK\x00tb\x89T\x80\x01\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00\x00\x00\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@\x00\x00@@U`\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00cnumpy.core.multiarray\n_reconstruct\nq\x08h\x03K\x00\x85U\x01b\x87Rq\t(K\x01)h\x06U\x02f8K\x00K\x01\x87Rq\n(K\x03U\x01<NNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK\x00tb\x89U\x08@\x8c\xb5x\x1d\xaf\x15Dtbtb.'
        actual = np.ma.loads(actual)
        self.assertNumpyAll(actual, vc['convolve_1d'].value, check_fill_value_dtype=False)
        self.assertEqual(cd.field.shape, (2, 2, 2, 3, 4))
        actual = np.loads('\x80\x02cnumpy.core.multiarray\n_reconstruct\nq\x01cnumpy\nndarray\nq\x02K\x00\x85U\x01b\x87Rq\x03(K\x01K\x02\x85cnumpy\ndtype\nq\x04U\x02O8K\x00K\x01\x87Rq\x05(K\x03U\x01|NNNJ\xff\xff\xff\xffJ\xff\xff\xff\xffK?tb\x89]q\x06(cdatetime\ndatetime\nq\x07U\n\x07\xd0\x01\x02\x0c\x00\x00\x00\x00\x00\x85Rq\x08h\x07U\n\x07\xd0\x01\x03\x0c\x00\x00\x00\x00\x00\x85Rq\tetb.')
        self.assertNumpyAll(actual, cd.field.temporal.value)

    def test_execute_valid_through_operations(self):
        """Test executing a "valid" convolution mode through operations ensuring the data is appropriately truncated."""

        rd = self.test_data.get_rd('cancm4_tas')
        calc = [{'func': 'convolve_1d', 'name': 'convolve', 'kwds': {'v': np.array([1, 1, 1, 1, 1]), 'mode': 'valid'}}]
        ops = ocgis.OcgOperations(dataset=rd, calc=calc, slice=[None, [0, 365], None, [0, 10], [0, 10]])
        ret = ops.execute()
        self.assertEqual(ret[1]['tas'].shape, (1, 361, 1, 10, 10))
        self.assertAlmostEqual(ret[1]['tas'].variables['convolve'].value.mean(), 1200.4059833795013)

    def test_registry(self):
        Calc([{'func': 'convolve_1d', 'name': 'convolve'}])


class TestMovingAverage(AbstractTestField):

    def test_execute(self):
        #todo: add to docs
        field = self.get_field(month_count=1, with_value=True)
        field = field[:, 0:4, :, :, :]
        field.variables['tmax'].value[:] = 1
        field.variables['tmax'].value.mask[:, :, :, 1, 1] = True
        parms = {'k': 3}
        ma = MovingAverage(field=field, parms=parms)
        vc = ma.execute()
        to_test = vc['moving_average'].value[0, :, 0, 0, 0]
        actual = np.ma.array([0.6666666865348816, 1.0, 1.0, 0.6666666865348816], mask=False, dtype=to_test.dtype)
        self.assertNumpyAll(to_test, actual)

    def test_registry(self):
        Calc([{'func': 'moving_average', 'name': 'ma'}])


class TestFrequencyPercentile(AbstractTestField):
    
    def test(self):
        field = self.get_field(with_value=True,month_count=2)
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        fp = FrequencyPercentile(field=field,tgd=tgd,parms={'percentile':99})
        ret = fp.execute()
        self.assertNumpyAllClose(ret['freq_perc'].value[0,1,1,0,:],
         np.ma.array(data=[0.92864656,0.98615474,0.95269281,0.98542988],
                     mask=False,fill_value=1e+20))


class TestMean(AbstractTestField):
    
    def test_units_are_maintained(self):
        field = self.get_field(with_value=True,month_count=2)
        self.assertEqual(field.variables['tmax'].cfunits,Units('kelvin'))
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        mu = Mean(field=field,tgd=tgd,alias='my_mean',calc_sample_size=False,
                  dtype=np.float64)
        dvc = mu.execute()
        self.assertEqual(dvc['my_mean'].cfunits,Units('kelvin'))
    
    def test(self):
        field = self.get_field(with_value=True,month_count=2)
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        mu = Mean(field=field,tgd=tgd,alias='my_mean',dtype=np.float64)
        dvc = mu.execute()
        dv = dvc['my_mean']
        self.assertEqual(dv.name,'mean')
        self.assertEqual(dv.alias,'my_mean')
        self.assertIsInstance(dv,DerivedVariable)
        self.assertEqual(dv.value.shape,(2,2,2,3,4))
        self.assertNumpyAll(np.ma.mean(field.variables['tmax'].value[1,tgd.dgroups[1],0,:,:],axis=0),
                            dv.value[1,1,0,:,:])
        
    def test_sample_size(self):
        field = self.get_field(with_value=True,month_count=2)
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        mu = Mean(field=field,tgd=tgd,alias='my_mean',calc_sample_size=True,
                  dtype=np.float64)
        dvc = mu.execute()
        dv = dvc['my_mean']
        self.assertEqual(dv.name,'mean')
        self.assertEqual(dv.alias,'my_mean')
        self.assertIsInstance(dv,DerivedVariable)
        self.assertEqual(dv.value.shape,(2,2,2,3,4))
        self.assertNumpyAll(np.ma.mean(field.variables['tmax'].value[1,tgd.dgroups[1],0,:,:],axis=0),
                            dv.value[1,1,0,:,:])

        ret = dvc['n_my_mean']
        self.assertNumpyAll(ret.value[0,0,0],
                            np.ma.array(data=[[31,31,31,31],[31,31,31,31],[31,31,31,31]],
                                        mask=[[False,False,False,False],[False,False,False,False],
                                              [False,False,False,False]],
                                        fill_value=999999))
        
        mu = Mean(field=field,tgd=tgd,alias='my_mean',calc_sample_size=False)
        dvc = mu.execute()
        self.assertNotIn('n_my_mean',dvc.keys())
        
    def test_two_variables(self):
        field = self.get_field(with_value=True,month_count=2)
        field.variables.add_variable(Variable(value=field.variables['tmax'].value+5,
                                              name='tmin',alias='tmin'))
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        mu = Mean(field=field,tgd=tgd,alias='my_mean',dtype=np.float64)
        ret = mu.execute()
        self.assertEqual(len(ret),2)
        self.assertAlmostEqual(5.0,abs(ret['my_mean_tmax'].value.mean() - ret['my_mean_tmin'].value.mean()))
        
    def test_two_variables_sample_size(self):
        field = self.get_field(with_value=True,month_count=2)
        field.variables.add_variable(Variable(value=field.variables['tmax'].value+5,
                                              name='tmin',alias='tmin'))
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        mu = Mean(field=field,tgd=tgd,alias='my_mean',dtype=np.float64,calc_sample_size=True)
        ret = mu.execute()
        self.assertEqual(len(ret),4)
        self.assertAlmostEqual(5.0,abs(ret['my_mean_tmax'].value.mean() - ret['my_mean_tmin'].value.mean()))
        self.assertEqual(set(['my_mean_tmax', 'n_my_mean_tmax', 'my_mean_tmin', 'n_my_mean_tmin']),
                         set(ret.keys()))
        
    def test_file_only(self):
        rd = self.test_data.get_rd('cancm4_tas')
        field = rd.get()
        field = field[:,10:20,:,20:30,40:50]
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        ## value should not be loaded at this point
        self.assertEqual(field.variables['tas']._value,None)
        mu = Mean(field=field,tgd=tgd,alias='my_mean',file_only=True)
        ret = mu.execute()
        ## value should still not be loaded
        self.assertEqual(field.variables['tas']._value,None)
        ## there should be no value in the variable present and attempts to load
        ## it should fail.
        with self.assertRaises(Exception):
            ret['my_mean_tas'].value
            
    def test_output_datatype(self):
        ## ensure the output data type is the same as the input data type of
        ## the variable.
        rd = self.test_data.get_rd('cancm4_tas')
        ops = ocgis.OcgOperations(dataset=rd,calc=[{'func':'mean','name':'mean'}],
                                  calc_grouping=['month'],geom='state_boundaries',
                                  select_ugid=[27])
        ret = ops.execute()
        with nc_scope(rd.uri) as ds:
            var_dtype = ds.variables['tas'].dtype
        self.assertEqual(ret[27]['tas'].variables['mean'].dtype,var_dtype)
            
    def test_file_only_by_operations(self):
        rd = self.test_data.get_rd('cancm4_tas')
        ops = ocgis.OcgOperations(dataset=rd,calc=[{'func':'mean','name':'mean'}],
                                  calc_grouping=['month'],geom='state_boundaries',
                                  select_ugid=[27],file_only=True,output_format='nc')
        ret = ops.execute()
        with nc_scope(ret) as ds:
            var = ds.variables['mean']
            ## all data should be masked since this is file only
            self.assertTrue(var[:].mask.all())
        
    def test_use_raw_values(self):
        field = self.get_field(with_value=True,month_count=2)
        field.variables.add_variable(Variable(value=field.variables['tmax'].value+5,
                                              name='tmin',alias='tmin'))
        grouping = ['month']
        tgd = field.temporal.get_grouping(grouping)
        
        ur = [True,False]
        agg = [
               True,
               False
               ]
        
        for u,a in itertools.product(ur,agg):
            if a:
                cfield = field.get_spatially_aggregated()
                self.assertNotEqual(cfield.shape,cfield._raw.shape)
                self.assertEqual(set([r.value.shape for r in cfield.variables.values()]),set([(2, 60, 2, 1, 1)]))
                self.assertEqual(cfield.shape,(2,60,2,1,1))
            else:
                cfield = field
                self.assertEqual(set([r.value.shape for r in cfield.variables.values()]),set([(2, 60, 2, 3, 4)]))
                self.assertEqual(cfield.shape,(2,60,2,3,4))
            mu = Mean(field=cfield,tgd=tgd,alias='my_mean',use_raw_values=u)
            ret = mu.execute()
            if a:
                self.assertEqual(set([r.value.shape for r in ret.values()]),set([(2, 2, 2, 1, 1)]))
            else:
                self.assertEqual(set([r.value.shape for r in ret.values()]),set([(2, 2, 2, 3, 4)]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
