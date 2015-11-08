import station
from pyspark import SparkContext

def test_local():
	station.setup()
	assert station.engine() is None
	assert station.mode() == 'local'

def test_local_context():
	with station.setup():
		mode = station.mode()
	assert mode == 'local'

def test_spark():
	station.setup(spark=True)
	assert station.mode() == 'spark'
	assert isinstance(station.engine(), SparkContext)
	assert station.engine().parallelize([1,2,3]).count() == 3

def test_spark_context():
	with station.setup(spark=True):
		mode = station.mode()
		n = station.engine().parallelize([1,2,3]).count()
	assert mode == 'spark'
	assert n == 3