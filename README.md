# station

Simple context manager to make it easier to write code targeting different computational engines. Currently supports `spark` and `local` modes, support for `dask` and `distributed` coming soon. Credit to Matt Rocklin (@mrocklin) for providing nice examples of custom context managers.

### install

```
pip install station
```

### initializing

if you have an existing spark context you can use it
```python
station.setup(sc)
```

or create a new spark context with options
```python
station.setup(spark=True, opts={'master': 'local'})
```

or use the default local environment
```python
station.setup()
```

### methods

once created you can get the context object provided by the backend with
```python
station.setup(spark=True)
station.engine()
>> <pyspark.context.SparkContext at 0x105f31cd0>
```

get the current mode with
```python
station.setup(spark=True)
station.mode()
>> 'spark'
```

```python
station.setup()
station.mode()
>> 'local'
```

and shut down with
```python
station.close()
```

### more

you can use in a `with` for tight context control e.g. for unit testing or benchmarking
```python
with station.setup(spark=True):
  # do spark stuff
  
with station.setup():
  # do local stuff

with station.setup(spark=True):
  # do more spark stuff
```
