from collections import defaultdict

_globals = defaultdict(lambda: None)
_globals.update({'engine': None, 'mode': 'local'})

class setup(object):
    """
    Setup a globally controlled context for a comptuational engine.

    Can use an existing engine, or create a new one with options.

    Parameters
    ----------
    spark : boolean or SparkContext, optional, default=False
        If True, will try to initialize a SparkContext using opts,
        if given a SparkContext, will use it

    opts : dictionary, optional, default=None
        Options for starting engines

    access : str, optional, default=None
        Access key for web services (e.g. AWS or GCE)

    credentials : dict, optional, default=None
        Credentials for engine if required
    """
    def __init__(self, spark=False, opts=None, credentials=None):

        self.old = _globals.copy()
        new = {'engine': None, 'mode': 'local'}

        if credentials:
            new['credentials'] = credentials

        if spark:
            if self.old['mode'] == 'spark':
                print("Already running Spark, will use existing context")
                return

            try:
                from pyspark import SparkContext
            except ImportError as e:
                print("Requested Spark but could not import its libraries, check your python path")
                print("Got error: %s" % e)
                print("Switching to local mode")
                return

            if isinstance(spark, SparkContext):
                print("Using provided Spark context")
                new['engine'] = spark
                new['mode'] = 'spark'
            else:
                print("Starting spark...")
                import muffle
                with muffle.on():
                    opts = {} if not opts else opts
                    sc = SparkContext(**opts)
                new['engine'] = sc
                new['mode'] = 'spark'
                print("Spark initialized")

            if credentials and ('access' in credentials.keys()) and ('secret' in credentials.keys()):
                new['engine']._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", credentials['access'])
                new['engine']._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", credentials['secret'])

        else:
            if not self.old['mode'] == 'local':
                self.old['engine'].stop()

        _globals.update(new)

    def __enter__(self):
        return

    def __exit__(self, type, value, traceback):
        if self.old['mode'] == 'local':
            stop()
        _globals.clear()
        _globals.update(self.old)

def stop():
    if _globals['mode'] == 'spark':
        _globals['engine'].stop()

def close():
    stop()
    _globals.clear()
    _globals.update({'engine': None, 'mode': 'local', 'credentials': None})

def engine():
    return _globals['engine']

def mode():
    return _globals['mode']

def credentials():
    return _globals['credentials']