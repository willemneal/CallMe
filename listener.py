from event import Event
class Listener(dict):
    def update(self,listener):
        map(lambda key:self.addListener(key,listener[key]),listener.keys())

    def addListener(self,name,callback):
        event = self.setdefault(name,Event())
        event.append(callback)

    def listen(self,event):
        def wrap(f):
            self.addListener(event,f)
            return f
        return wrap

    def trigger(self,event):
        def wrap(f):
            def newFunc(*args,**kwargs):
                res = f(*args, **kwargs)
                if event in self:
                    self[event](res)
                return res
            return newFunc
        return wrap

L = Listener()

@L.listen('call')
def answer(name):
    print name,"answered"


@L.trigger('call')
def call(name):
    print "I'm calling", name
    return name


call('willem')
