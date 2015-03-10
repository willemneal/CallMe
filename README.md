# CallMe
A simple event listener

```python
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
```

returns
```
willem is calling
willem's call was answered
Listener {'listeners': Event [Listener {'call': Event ['bob']}], 'call': Event ['answer']} Listener {'call': Event ['bob']}
willem is calling
willem's call was answered
bob was called by willem
```
