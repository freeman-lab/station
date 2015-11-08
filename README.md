# station

Data analysis typically requires working across different scales, with different tools and computational backends. `station` provides a simple context manager to make it easier to write code across different levels.

### install

pip install station

### create a 

with an existing spark context
```
station.setup(sc)
```

create a new spark context
```
station.setup(spark=True, opts={'master': 'local'})
```

create a local environment
```
station.setup()
```

you can also use in a `with`, great for unit testing!
```
with station.setup(spark=True):
  # do spark stuff
  
with station.setup():
  # do local stuff

with station.setup(spark=True):
  # do more spark stuff
```

###
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
