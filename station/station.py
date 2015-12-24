from collections import defaultdict

_globals = defaultdict(lambda: None)
_globals.update({'engine': None, 'mode': 'local', 'updated': False})

class start(object):
    """
    Setup a globally controlled context for a comptuational engine.

    Can use an existing engine, or create a new one with options.

    Parameters
    ----------
    spark : boolean or SparkContext, optional, default=False
        If True, will try to initialize a SparkContext using opts,
        if given a SparkContext, will use it

    opts : dict, optional, default=None
        Extra options for starting engines. 
        For Spark, should be a dictionary of arguments passed to SparkContext(),
        e.g. station.start(spark=True, opts={'master': 'local', 'appName': 'hello'})

    credentials : dict, optional, default=None
        Dictionary of credentials to associate with context,
        useful for accessing web services (e.g. AWS and GCE).
        Will automatically add to engine where appropriate.
    """
    def __init__(self, spark=False, opts=None, credentials=None):

        self.old = _globals.copy()
        new = {'engine': None, 'mode': 'local'}
        _globals['updated'] = False

        if credentials:
            new['credentials'] = credentials

        if spark:
            if self.old['mode'] == 'spark':
                return

            try:
                from pyspark import SparkContext
            except ImportError as e:
                return

            if isinstance(spark, SparkContext):
                new['engine'] = spark
                new['mode'] = 'spark'
            else:
                import muffle
                with muffle.on():
                    opts = {} if not opts else opts
                    sc = SparkContext(**opts)
                new['engine'] = sc
                new['mode'] = 'spark'

                _globals['updated'] = True

            if credentials and ('access' in credentials.keys()) and ('secret' in credentials.keys()):
                new['engine']._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", credentials['access'])
                new['engine']._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", credentials['secret'])

        else:
            if self.old['mode'] == 'local':
                return

            if not self.old['mode'] == 'local':
                self.old['engine'].stop()

            _globals['updated'] = True

        _globals.update(new)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.old['mode'] == 'local':
            shutdown()
        _globals.clear()
        _globals.update(self.old)

    def __repr__(self):
        prefix = 'running' if _globals['updated'] else 'already'
        return '[station] ' + prefix + ' in ' + _globals['mode'] + ' mode'

def shutdown():
    if _globals['mode'] == 'spark':
        _globals['engine'].stop()

def stop():
    shutdown()
    _globals.clear()
    _globals.update({'engine': None, 'mode': 'local', 'credentials': None})

def engine():
    return _globals['engine']

def mode():
    return _globals['mode']

def credentials():
    return _globals['credentials']