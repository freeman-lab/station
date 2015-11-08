# station

Data analysis typically requires working across different scales, with different tools and computational engines. `station` provides a simple context manager to make it easier to write code across different levels, and move back and forth between different modes.

Currently supports `spark` and `local` modes. Hope to add support for `dask` and `distributed` soon.

### install

```
pip install station
```

### initializing

if you have an existing spark context as `sc`
```
station.setup(sc)
```

or create a new spark context
```
station.setup(spark=True, opts={'master': 'local'})
```

or create a local environment
```
station.setup()
```

you can also use in a `with` for tight control (e.g. in unit testing)
```
with station.setup(spark=True):
  # do spark stuff
  
with station.setup():
  # do local stuff

with station.setup(spark=True):
  # do more spark stuff
```

### methods

once created you can access
```
station.agent()
```
to get whatever context / engine / object provided by the backend

to get the current mode
```
station.mode()
```

to shut down
```
station.close()
```
