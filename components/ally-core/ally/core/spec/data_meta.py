'''
Created on Jan 27, 2012

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the data meta support. 
'''

from ally.api.operator import Model
from ally.api.type import Type, TypeProperty, TypeModel
from ally.core.spec.resources import Path
from ally.support.util import immutable, immut

# --------------------------------------------------------------------

returnSame = lambda obj: obj
# Function that just returns the same value received.

# --------------------------------------------------------------------

@immutable
class MetaModel:
    '''
    Provides the meta model object.
    '''
    
    __slots__ = __immutable__ = ('model', 'getModel', 'metaLink', 'properties')
    
    def __init__(self, model, getModel, metaLink=None, properties={}):
        '''
        Construct the object meta.
    
        @param model: Model
            The model of the meta.
        @param getModel: Callable(object)
            A callable that takes as an argument the object to extract the model instance.
        @param metaLink: MetaLink|None
            The meta link of the model or None.
        @param metaLink: MetaLink|None
            The meta link of the model or None.
        @param properties: dictionary{string, meta object}
            The properties of the meta model.
        '''
        assert isinstance(model, Model), 'Invalid model %s' % model
        assert callable(getModel), 'Invalid get model callable %s' % getModel
        assert metaLink is None or isinstance(metaLink, MetaLink), 'Invalid meta link %s' % metaLink
        assert isinstance(properties, dict), 'Invalid properties %s' % properties
        if __debug__:
            for name in properties: assert isinstance(name, str), 'Invalid property name %s' % name
        self.model = model
        self.getModel = getModel
        self.metaLink = metaLink
        self.properties = immut(properties)
    
    def __str__(self): return '%s[%s, %s]' % (self.__class__.__name__, self.metaLink, self.properties)

@immutable  
class MetaList:
    '''
    Provides the list meta.
    '''
    
    __slots__ = __immutable__ = ('metaItem', 'getItems')
    
    def __init__(self, metaItem, getItems):
        '''
        Construct the list meta.

        @param metaItem: MetaModel|MetaLink|MetaValue
            The meta item.
        @param getItems: Callable(object)
            A callable that takes as an argument the object to extract this meta iterable instance.
        '''
        assert isinstance(metaItem, (MetaModel, MetaLink, MetaValue)), 'Invalid meta item %s' % metaItem
        assert callable(getItems), 'Invalid get items callable %s' % getItems
        self.metaItem = metaItem
        self.getItems = getItems
    
    def __str__(self): return '%s[%s]' % (self.__class__.__name__, self.metaItem)

@immutable
class MetaLink:
    '''
    Provides the link meta.
    '''
    
    __slots__ = __immutable__ = ('getLink',)
    
    def __init__(self, getLink):
        '''
        Construct the link meta.
        
        @param getLink: Callable(object)
            A callable that takes as an argument the object to extract the path.
        '''
        assert callable(getLink), 'Invalid get link callable %s' % getLink
        self.getLink = getLink

@immutable
class MetaValue:
    '''
    Provides the value meta.
    '''
    
    __slots__ = __immutable__ = ('type', 'getValue')
    
    def __init__(self, type, getValue):
        '''
        Construct the list meta.
        
        @param type: Type
            The value type.
        @param getValue: Callable(object)
            A callable that takes as an argument the object to extract this meta value instance.
        '''
        assert isinstance(type, Type), 'Invalid value type %s' % type
        assert callable(getValue), 'Invalid get value callable %s' % getValue
        self.type = type
        self.getValue = getValue
    
    def __str__(self): return '%s[%s]' % (self.__class__.__name__, self.type)

class MetaFetch:
    '''
    Provides a meta that just fetches a value that has to be used by the contained meta.
    This type of meta is not rendered.
    '''
    
    __slots__ = __immutable__ = ('meta', 'getValue')
    
    def __init__(self, meta, getValue):
        '''
        Construct the fetch meta.
        
        @param meta: meta object
            The meta object to be used on the fetched value.
        @param getValue: Callable(object)
            A callable that takes as an argument the object to extract the contained meta value.
        '''
        assert meta is not None, 'A meta object is required'
        assert callable(getValue), 'Invalid get value callable %s' % getValue
        self.meta = meta
        self.getValue = getValue
    
    def __str__(self): return '%s[%s]' % (self.__class__.__name__, self.meta)

# --------------------------------------------------------------------

class MetaPath(MetaLink):
    '''
    Provides the link on path meta.
    '''
    
    __slots__ = __immutable__ = ('type', 'path', 'getValue')
    
    def __init__(self, path, type, getValue):
        '''
        Construct the update path callable.
        
        @param path: Path
            The path to be updated and returned.
        @param type: TypeProperty|TypeModel
            The type of the object to be updated.
        @param getValue: Callable(object)
            A callable that takes as an argument the object to extract the value for the path.
        '''
        assert isinstance(path, Path), 'Invalid path %s' % path
        assert isinstance(type, (TypeProperty, TypeModel)), 'Invalid type %s' % type
        assert callable(getValue), 'Invalid get value callable %s' % getValue
        self.type = type
        self.path = path
        self.getValue = getValue
        
    def getLink(self, obj):
        '''
        Provides the updated path.
        
        @return: Path|None
            The updated path or None if no path is available.
        '''
        assert isinstance(self.path, Path)
        value = self.getValue(obj)
        path = self.path.clone()
        path.update(value, self.type)
        if path.isValid(): return path
        
    def __str__(self): return '%s[%s, %s]' % (self.__class__.__name__, self.path, self.type)
