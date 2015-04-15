from callMe import Listener

L = Listener()

@L.listen('call',repeat=False)
def answer(name):
    print "{name}'s call was answered".format(name=name)


@L.trigger('call')
def call(name):
    print name, "is calling"
    return name

L2 = Listener()

@L2.listen('we')
@L2.listen('call')
def bob(name):
    print "bob was called by", name

call('willem')

L + L2
print L, L2

call('willem')
L - L2
print L
call('willem')
