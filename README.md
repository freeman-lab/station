# station

Simple context manager to make it easier to write code targeting different computational engines. Currently supports `spark` and `local` modes, support for `dask` and `distributed` coming soon.

### install

```
pip install station
```

### initializing

if you have an existing spark context as `sc`
```python
station.setup(sc)
```

or create a new spark context
```python
station.setup(spark=True, opts={'master': 'local'})
```

or create a local environment
```python
station.setup()
```

you can also use in a `with` for tight control (e.g. in unit testing)
```python
with station.setup(spark=True):
  # do spark stuff
  
with station.setup():
  # do local stuff

with station.setup(spark=True):
  # do more spark stuff
```

### methods

once created you can get the context object provided by the backend with
```python
station.engine()
```

get the current mode with
```python
station.mode()
```

and shut down with
```python
station.close()
```
