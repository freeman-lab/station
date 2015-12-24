import station
from pyspark import SparkContext

def test_local():
	station.start()
	assert station.engine() is None
	assert station.mode() == 'local'

def test_local_context():
	with station.start():
		mode = station.mode()
	assert mode == 'local'

def test_spark():
	station.start(spark=True)
	assert station.mode() == 'spark'
	assert isinstance(station.engine(), SparkContext)
	assert station.engine().parallelize([1,2,3]).count() == 3
	station.stop()

def test_spark_existing():
	sc = SparkContext()
	station.start(sc)
	assert station.mode() == 'spark'
	assert isinstance(station.engine(), SparkContext)
	assert station.engine().parallelize([1,2,3]).count() == 3
	station.stop()

def test_spark_opts():
	station.start(spark=True, opts={'master': 'local', 'appName': 'hello'})
	assert station.mode() == 'spark'
	assert isinstance(station.engine(), SparkContext)
	assert station.engine().master == 'local'
	assert station.engine().appName == 'hello'
	assert station.engine().parallelize([1,2,3]).count() == 3
	station.stop()

def test_spark_context():
	with station.start(spark=True):
		mode = station.mode()
		n = station.engine().parallelize([1,2,3]).count()
	assert mode == 'spark'
	assert n == 3
	assert station.mode() == 'local'

def test_spark_close():
	station.start(spark=True)
	assert station.mode() == 'spark'
	station.stop()
	assert station.mode() == 'local'