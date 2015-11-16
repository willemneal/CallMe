'''
The following is from http://stackoverflow.com/a/2022629
Thanks to Longpoke
'''
import types

class Event(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:
    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = Event()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    # g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __init__(self,repeat=True):
        super(Event,self).__init__()
        self.repeat = repeat

    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)
        if not self.repeat:
            map(lambda func: self.remove(func),self)

    def remove(self, func):
        if func in self:
            list.remove(self,func)

    def __repr__(self):
        #Make function names look prettier
        items = [item.__name__ if isinstance(item, types.FunctionType) or isinstance(item, types.MethodType)
                else item
                for item in self]
        return "Event %s" % list.__repr__(items)

class Listener(dict):
    def addSub(self, name, callback,repeat=True):
        '''sets self[name] to Event() if there is no key name.
           Either way self[name] is returned and callback is appended'''
        self.setdefault(name, Event(repeat)).append(callback)

    def removeSub(self, name, callback):
        if name in self:
            self[name].remove(callback)
            if len(self[name]) == 0:
                del self[name]

    def listen(self, event, repeat=True):
        def wrap(f):
            self.addSub(event, f,repeat)
            return f
        return wrap

    def trigger(self, event):
        def wrap(f):
            def newFunc(*args, **kwargs):
                res = f(*args, **kwargs)
                self(event, res)
                return res
            return newFunc
        return wrap


    def __call__(self, event, *args, **kwargs):
        if event in self:
            self[event](*args, **kwargs)
            if len(self[event])==0:
                self.removeSub(event,self[event])

        if "listeners" in self:
            self['listeners'](event, *args, **kwargs)

    def __add__(self, listener):
        self.addSub('listeners', listener)

    def __sub__(self, listener):
        self.removeSub('listeners', listener)

    def __repr__(self):
        return "Listener %s"% dict.__repr__(self)

    def getListeners(self):
        if "listeners" in self:
            return self['listeners']
        return None

    def isListener(self, listener):
        return listener in self.getListeners()
