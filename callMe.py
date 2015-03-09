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

    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def remove(self, func):
        if func in self:
            list.remove(self,func)

    def __repr__(self):
        items = []
        for item in self:
            if isinstance(item, types.FunctionType): #make functions prettier
                items.append(item.__name__)
            else:
                items.append(item)
        return "Event %s" % list.__repr__(items)

class Listener(dict):
    def addSub(self, name, callback):
        '''sets self[name] to Event() if there is no key name.
           Either way self[name] is returned and callback is appended'''
        self.setdefault(name, Event()).append(callback)

    def removeSub(self, name, callback):
        if name in self:
            self[name].remove(callback)
            if len(self[name]) == 0:
                del self[name]

    def listen(self,event):
        def wrap(f):
            self.addSub(event, f)
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
        if "listeners" in self:
            self['listeners'](event, *args, **kwargs)

    def __add__(self, listener):
        self.addSub('listeners', listener)

    def __sub__(self, listener):
        self.removeSub('listener', listener)

    def __repr__(self):
        return "Listener %s"% dict.__repr__(self)




L = Listener()

@L.listen('call')
def answer(name):
    print "{name}'s call was answered".format(name=name)


@L.trigger('call')
def call(name):
    print name, "is calling"
    return name

L2 = Listener()


@L2.listen('call')
def bob(name):
    print "bob was called by", name

call('willem')

L + L2
print L, L2

call('willem')
