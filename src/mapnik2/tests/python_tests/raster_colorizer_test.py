#coding=utf8
import os
import mapnik2
from mapnik2.tests.python_tests.utilities import execution_path
from nose.tools import *

def setup():
    # All of the paths used are relative, if we run the tests
    # from another directory we need to chdir()
    os.chdir(execution_path('.'))

def test_gen_map():
    mapxmlfile = '../data/good_maps/raster_colorizer.xml'
    mapxmloutputfile = 'raster_colorizer_test_save.xml'
    outputfile = 'raster_colorizer_test.png'

    m = mapnik2.Map(800, 600)
    try:
        mapnik2.load_map(m, mapxmlfile)
        mapnik2.save_map(m, mapxmloutputfile)
        m.zoom_all()
        mapnik2.render_to_file(m, outputfile)
    except RuntimeError,e:
        # only test datasources that we have installed
        if not 'Could not create datasource' in str(e):
            raise RuntimeError(str(e))

#test discrete colorizer mode
def test_get_color_discrete():
    #setup
    colorizer = mapnik2.RasterColorizer();
    colorizer.default_color = mapnik2.Color(0,0,0,0);
    colorizer.default_mode = mapnik2.COLORIZER_DISCRETE;

    colorizer.add_stop(10, mapnik2.Color(100,100,100,100));
    colorizer.add_stop(20, mapnik2.Color(200,200,200,200));



    #should be default colour
    eq_(colorizer.get_color(-50), mapnik2.Color(0,0,0,0));
    eq_(colorizer.get_color(0), mapnik2.Color(0,0,0,0));
    
    #now in stop 1
    eq_(colorizer.get_color(10), mapnik2.Color(100,100,100,100));
    eq_(colorizer.get_color(19), mapnik2.Color(100,100,100,100));
    
    #now in stop 2
    eq_(colorizer.get_color(20), mapnik2.Color(200,200,200,200));
    eq_(colorizer.get_color(1000), mapnik2.Color(200,200,200,200));

#test exact colorizer mode
def test_get_color_exact():
    #setup
    colorizer = mapnik2.RasterColorizer();
    colorizer.default_color = mapnik2.Color(0,0,0,0);
    colorizer.default_mode = mapnik2.COLORIZER_EXACT;

    colorizer.add_stop(10, mapnik2.Color(100,100,100,100));
    colorizer.add_stop(20, mapnik2.Color(200,200,200,200));

    #should be default colour
    eq_(colorizer.get_color(-50), mapnik2.Color(0,0,0,0));
    eq_(colorizer.get_color(11), mapnik2.Color(0,0,0,0));
    eq_(colorizer.get_color(20.001), mapnik2.Color(0,0,0,0));
    
    #should be stop 1
    eq_(colorizer.get_color(10), mapnik2.Color(100,100,100,100));
    
    #should be stop 2
    eq_(colorizer.get_color(20), mapnik2.Color(200,200,200,200));
    
    


#test linear colorizer mode
def test_get_color_linear():
    #setup
    colorizer = mapnik2.RasterColorizer();
    colorizer.default_color = mapnik2.Color(0,0,0,0);
    colorizer.default_mode = mapnik2.COLORIZER_LINEAR;

    colorizer.add_stop(10, mapnik2.Color(100,100,100,100));
    colorizer.add_stop(20, mapnik2.Color(200,200,200,200));

    #should be default colour
    eq_(colorizer.get_color(-50), mapnik2.Color(0,0,0,0));
    eq_(colorizer.get_color(9.9), mapnik2.Color(0,0,0,0));
    
    #should be stop 1
    eq_(colorizer.get_color(10), mapnik2.Color(100,100,100,100));
    
    #should be stop 2
    eq_(colorizer.get_color(20), mapnik2.Color(200,200,200,200));

    #half way between stops 1 and 2
    eq_(colorizer.get_color(15), mapnik2.Color(150,150,150,150));

    #after stop 2
    eq_(colorizer.get_color(100), mapnik2.Color(200,200,200,200));


def test_stop_label():
    stop = mapnik2.ColorizerStop(1, mapnik2.COLORIZER_LINEAR, mapnik2.Color('red'))
    assert not stop.label
    label = u"32º C".encode('utf8')
    stop.label = label
    assert stop.label == label, stop.label

if __name__ == "__main__":
    setup()
    [eval(run)() for run in dir() if 'test_' in run]


