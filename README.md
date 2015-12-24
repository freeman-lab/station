# station

[![Build Status](https://travis-ci.org/freeman-lab/station.svg?branch=master)](https://travis-ci.org/freeman-lab/station)

Simple context manager to make it easier to write code targeting different computational engines. Currently supports `spark` and `local` modes, support for `dask` and `distributed` coming soon. Credit to Matt Rocklin (@mrocklin) for providing nice examples of custom context managers.

### install

```
pip install station
```

### initializing

if you have an existing spark context you can use it
```python
station.start(sc)
```

or create a new spark context with options
```python
station.start(spark=True, opts={'master': 'local'})
```

or use the default local environment
```python
station.start()
```

### methods

once created you can get the context object provided by the backend
```python
station.engine()
>> None | <pyspark.context.SparkContext>
```

get the current mode with
```python
station.mode()
>> 'local' | 'spark'
```

and stop with
```python
station.stop()
```

### more

you can use in a `with` for tight context control e.g. for unit testing or benchmarking
```python
with station.start(spark=True):
  # do spark stuff
  
with station.start():
  # do local stuff

with station.start(spark=True):
  # do more spark stuff
```
any engines created inside a `with` will be shut down upon exit, so results requiring the engine should be collected locally
