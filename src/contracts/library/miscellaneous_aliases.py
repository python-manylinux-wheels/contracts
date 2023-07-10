import collections



def ist(C):
    def f(x):
        f.__name__ = 'isinstance_of_%s' % C.__name__
        if not isinstance(x, C):
            raise ValueError('Value is not an instance of %s.' % C.__name__)
    return f


def m_new_contract(name, f):
    from contracts.library.extensions import CheckCallable
    from contracts.library.extensions import Extension
    Extension.registrar[name] = CheckCallable(f)


m_new_contract('Container', ist(collections.abc.Container))
# todo: Iterable(x)
m_new_contract('Iterable', ist(collections.abc.Iterable))

m_new_contract('Hashable', ist(collections.abc.Hashable))



m_new_contract('Iterator', ist(collections.abc.Iterator))
m_new_contract('Sized', ist(collections.abc.Sized))
m_new_contract('Callable', ist(collections.abc.Callable))
m_new_contract('Sequence', ist(collections.abc.Sequence))
m_new_contract('Set', ist(collections.abc.Set))
m_new_contract('MutableSequence', ist(collections.abc.MutableSequence))
m_new_contract('MutableSet', ist(collections.abc.MutableSet))
m_new_contract('Mapping', ist(collections.abc.Mapping))
m_new_contract('MutableMapping', ist(collections.abc.MutableMapping))
#new_contract('MappingView', ist(collections.MappingView))
#new_contract('ItemsView', ist(collections.ItemsView))
#new_contract('ValuesView', ist(collections.ValuesView))


# Not a lambda to have better messages
def is_None(x):
    return x is None

m_new_contract('None', is_None)
m_new_contract('NoneType', is_None)
