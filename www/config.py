'''
configuration
'''
import config_default

def merge(default, override):
    conf={}
    for k,v in default.items():
        if k in override:
            if isinstance(v,dict):
                conf[k]=merge(v,override[k])
            else:
                conf[k]=override[k]
        conf[k]=v
    return conf

class Dict(dict):
    '''
    add x.y stype to dict
    '''
    def __init__(self,keys=(),values=(),**kw):
        super(Dict,self).__init__(**kw)
        for k,v in zip(keys,values):
            self[k]=values

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'Dict':%s has no attribute: %s" %(self.__name__,key))

    def __setattr__(self,key,value):
        self[key]=value


def toDict(d):
    D=Dict()
    for k,v in d.items():
        D[k]=toDict(v) if isinstance(v,dict) else v
    return D

try:
    import config_override
    configs=merge(config_default.configs,config_override.configs)
except ImportError:
    pass

configs=toDict(configs)