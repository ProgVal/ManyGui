
''' Event framework for Anygui. For more information, see Anygui
    IRFC 0010 at http://anygui.sf.net/irfc.

    Magnus Lie Hetland, 2001-11-16
'''

__all__ = '''

    connect
    disconnect
    dispatch
    disconnectSource
    disconnectHandler
    disconnectMethods
    Event
    CallbackAdapter

'''.split()

categories = BOTH, SOURCE, TYPE, ANON = range(4)
registry   = {}, {}, {}, {}
sources = {}

import time
from Utils import WeakMethod, HashableWeakRef
ref = HashableWeakRef

def locators(event, weak=0):
    'Get indexing information about an event.'
    source = getattr(event, 'source', None)
    type   = getattr(event, 'type',   None)
    if not None in [source, type]:
        cat = BOTH
    elif source != None:
        cat = SOURCE
    elif type != None:
        cat = TYPE
    else:
        cat = ANON
    if source != None: source = ref(source, weak)
    key = source, type
    return cat, key

def connect(event, handler, weak=0):
    'Connect an event pattern to an event handler.'
    cat, key = locators(event, weak)
    if not sources.has_key(key) and key[0]:
        sources[key] = key[0]
    handler = WeakMethod(handler, weak)
    try:
        if not handler in registry[cat][key]:
            registry[cat][key].append(handler)
    except KeyError:
        registry[cat][key] = [handler]

def disconnect(event, handler):
    'Disconnect an event handler from an event pattern.'
    cat, key = locators(event)
    handler = WeakMethod(handler)
    if handler in registry[cat][key]:
        registry[cat][key].remove(handler)

def set_time(event):
    if not hasattr(event, 'time'):
        try:
            event.time = time.time()
        except TypeError: pass

def compatible(cat, filter):
    if cat == BOTH:
        return 1
    elif cat == SOURCE:
        return filter in [SOURCE, ANON]
    elif cat == TYPE:
        return filter in [TYPE, ANON]
    elif cat == ANON:
        return filter == ANON

# Sources sending events:
source_stack = []

def dispatch(event):
    'Call the appropriate event handlers with event as the argument. \
    As a side-effect, dead handlers are removed from the candidate lists.'
    source_stack.append(id(getattr(event, 'source', None)))
    try:
        set_time(event)
        event.freeze()
        cat1, key = locators(event)
        src, type = key
        dead = 0
        if sources.has_key(key):
            real_src = sources[key]
            dead = not real_src()
        for cat2 in categories:
            if dead:
                try: del registry[cat2][key]
                except: pass
                continue
            if not compatible(cat1, cat2): continue
            if cat2 is ANON: key = (None, None)
            handlers = registry[cat2].get(key, [])
            live_handlers = []
            for weak_handler in handlers:
                obj = weak_handler.get_obj()
                if id(obj) in source_stack: continue
                handler = weak_handler()
                if handler:
                    live_handlers.append(weak_handler)
                    handler(event)
            registry[cat2][key] = live_handlers
    finally:
        source_stack.pop()

def disconnectSource(source):
    'Disconnect all handlers connected to a given source.'
    for cat in [BOTH, SOURCE]:
        for ident, type in categories[cat].keys():
            if ident == ref(source):
                del categories[BOTH][ident,type]

def disconnectHandler(handler):
    'Disconnect a handler from the event framework.'
    handler = WeakMethod(handler)
    for cat in categories:
        for handlers in registry[cat].values():
            if handler in handlers:
                handlers.remove(WeakMethod(handler))

def disconnectMethods(obj):
    'Disconnect all the methods of obj that are handlers.'
    for name in dir(obj):
        attr = getattr(obj, name)
        if callable(attr):
            try:
                disconnectHandler(attr)
            except: pass

class Event:
    __frozen = 0
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    def __setattr__(self, name, value):
        if not self.__frozen:
            self.__dict__[name] = value
        else:
            raise TypeError, 'object has been frozen'
    def freeze(self):
        if not self.__frozen:
            self.__frozen = 1
    def match(self, other):
        """
        Match another event if it has the same type and source as self.
        Ignore either type or source or both if self doesn't have them.
        """
        try:
            type_match = self.type == other.type
        except AttributeError:
            type_match = not hasattr(self, 'type')
        try:
            source_match = self.source == other.source
        except AttributeError:
            source_match = not hasattr(self, 'source')
        return type_match and source_match

class CallbackAdapter:
    def dispatch(self, event):
        '''
        If self has a proper callback, call it, then call global
        dispatch().
        '''
        if not hasattr(event, 'source'):
            event.source = self
        set_time(event)
        event.freeze()
        callback = getattr(self, event.type, None)
        if callback:
            callback(event)
        dispatch(event)
