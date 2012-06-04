# -*- coding: utf-8 -*-
import base64
import os
import collections
import hashlib

#######
# API #
#######

def parse_response(xml, secret, url):
	from xml.etree import ElementTree
	root = ElementTree.XML(xml)
	data = to_dict(root)
	if check_signature(data, secret, url):
		return data

def create_response(data, secret, url):
	data['pg_salt'] = salt()
	result = dict_to_ordered(data)
	result['pg_sig'] = create_signature(result, secret, url)
	return to_xml(result, root='response')

def check_signature(data, secret, url):
	data = dict_to_ordered(data)
	data_sig = data.pop('pg_sig')
	test_sig = create_signature(data, secret, url)
	# DEBUG:
	# print "----"
	# print data
	# print "----"
	# print data_sig
	# print "----"
	# print test_sig
	# print "----"
	return data_sig == test_sig

#########
# Utils #
#########

def md5(val):
	md5 = hashlib.md5()
	md5.update(val.encode('utf-8'))
	return md5.hexdigest()

def salt():
	import base64
	return base64.urlsafe_b64encode(os.urandom(10)).replace('=', '')

def url_last(url):
	return url.split('/').pop()

def create_signature(data, secret, url):
	if isinstance(data, collections.OrderedDict):
		plain = dict_to_plain(data)
	else:
		plain = dict_to_plain(dict_to_ordered(data))
	if not url is None:
		plain.insert(0, url_last(url))
	plain.append(secret)
	# DEBUG:
	# print u';'.join(plain)
	return md5(u';'.join(plain))

def create_request(data, secret, url, method='POST'):
	"""
	secret: секретный токен, строка
	data: данные запроса, dict
	method: 'GET' или 'POST', для 'GET' формируется urlencoded-строка,
			для 'POST' запрос формируется в виде XML.

	Пример::

		create_request({'pg_param1': 1}, secret="lalala")

	Результат объект dict c ключом ``pg_xml`` и значением::

		<?xml version="1.0" encoding="utf-8"?>
		<request>
			<pg_param1>1</pg_param1>
			<pg_sig>74aa41a4f425d124a23c3a53a3140bdc15826</pg_sig>
		</request>
	"""
	data['pg_salt'] = salt()
	request = dict_to_ordered(data)
	request['pg_sig'] = create_signature(request, secret, url)
	if method in ('POST', 'XML'):
		return {'pg_xml': to_xml(request, root='request')}
	else:
		return request

def dict_to_plain(data):
	plain = []
	for k, v in data.items():
		if v is None:
			plain.append('')
		elif isinstance(v, dict):
			plain.append(dict_to_plain(v))
		else:
			plain.append(unicode(v))
	return plain

def dict_to_ordered(data):
	ordered = collections.OrderedDict
	copy = ordered(sorted(data.items(), key=lambda t: t[0]))
	for k, v in copy.items():
		if isinstance(v, dict):
			copy[k] = dict_to_ordered(v)
	return copy

#####################################################
# Simple XML serializer:							#
# http://vorushin.ru/blog/11-python-xml-serializer/ #
#####################################################

from StringIO import StringIO
from xml.etree.cElementTree import Element, ElementTree

def to_xml(data, root='content'):
	content_elem = Element(root)
	_to_xml(content_elem, data)
	tree = ElementTree(content_elem)
	f = StringIO()
	tree.write(f, 'UTF-8')
	return f.getvalue()

def _to_xml(parentem, data):
	if isinstance(data, (list, tuple)):
		_serialize_list(parentem, data)
	elif isinstance(data, dict):
		_serialize_dict(parentem, data)
	else:
		parentem.text = unicode(data)

def _serialize_list(parentem, data_list):
	for i in data_list:
		item_elem = Element('item')
		parentem.append(item_elem)
		_to_xml(item_elem, i)

def _serialize_dict(parentem, data_dict):
	for k, v in data_dict.iteritems():
		key_elem = Element(k)
		parentem.append(key_elem)
		_to_xml(key_elem, v)

#################################################################
# Simple XML parser:											#
# http://code.activestate.com/recipes/410469-xml-as-dictionary/ #
#################################################################

def to_list(nodes):
	li = []
	for el in nodes:
		if el:
			# treat like dict
			if len(el) == 1 or el[0].tag != el[1].tag:
				li.append(to_dict(el))
			# treat like list
			elif el[0].tag == el[1].tag:
				li.append(to_list(el))
		elif el.text:
			text = el.text.strip()
			if text:
				li.append(text)
	return li


def to_dict(parent):
	"""
	Example usage::

		>>> root = ElementsTree.parse('some.xml').getroot()
		>>> di = to_dict(root)

	Or, if you want to use an XML string::

		>>> root = ElementsTree.XML(xml_string)
		>>> di = to_dict(root)
	"""
	ordered = collections.OrderedDict
	di = ordered()
	if parent.items():
		di.update(ordered(parent.items()))
	for el in parent:
		if len(el):
			# treat like dict - we assume that if the first two tags
			# in a series are different, then they are all different.
			if len(el) == 1 or el[0].tag != el[1].tag:
				ch = to_dict(el)
				# if the tag has attributes, add those to the dict
				if el.items():
					ch.update(ordered(el.items()))
			# treat like list - we assume that if the first two tags
			# in a series are the same, then the rest are the same.
			else:
				# here, we put the list in dictionary; the key is the
				# tag name the list els all share in common, and
				# the value is the list itself 
				ch = {el[0].tag: to_list(el)}
			di.update({el.tag: ch})
		# this assumes that if you've got an attribute in a tag,
		# you won't be having any text. This may or may not be a 
		# good idea -- time will tell. It works for the way we are
		# currently doing XML configuration files...
		elif el.items():
			di.update({el.tag: ordered(el.items())})
		# finally, if there are no child tags and no attributes, extract
		# the text
		else:
			di.update({el.tag: el.text})
	return di

#######################
# BackportOrderedDict #
#######################

## {{{ http://code.activestate.com/recipes/576693/ (r9)

try:
    from thread import get_ident as _get_ident
except ImportError:
    from dummy_thread import get_ident as _get_ident

try:
    from _abcoll import KeysView, ValuesView, ItemsView
except ImportError:
    pass

class BackportOrderedDict(dict):
    'Dictionary that remembers insertion order'
    # An inherited dict maps keys to values.
    # The inherited dict provides __getitem__, __len__, __contains__, and get.
    # The remaining methods are order-aware.
    # Big-O running times for all methods are the same as for regular dictionaries.

    # The internal self.__map dictionary maps keys to links in a doubly linked list.
    # The circular doubly linked list starts and ends with a sentinel element.
    # The sentinel element never gets deleted (this simplifies the algorithm).
    # Each link is stored as a list of length three:  [PREV, NEXT, KEY].

    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        '''
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = []                     # sentinel node
            root[:] = [root, root, None]
            self.__map = {}
        self.__update(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link which goes at the end of the linked
        # list, and the inherited dictionary is updated with the new key/value pair.
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        'od.__delitem__(y) <==> del od[y]'
        # Deleting an existing item uses self.__map to find the link which is
        # then removed by updating the links in the predecessor and successor nodes.
        dict_delitem(self, key)
        link_prev, link_next, key = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        root = self.__root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        try:
            for node in self.__map.itervalues():
                del node[:]
            root = self.__root
            root[:] = [root, root, None]
            self.__map.clear()
        except AttributeError:
            pass
        dict.clear(self)

    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root[0]
            link_prev = link[0]
            link_prev[1] = root
            root[0] = link_prev
        else:
            link = root[1]
            link_next = link[1]
            root[1] = link_next
            link_next[0] = root
        key = link[2]
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    # -- the following methods do not depend on the internal structure --

    def keys(self):
        'od.keys() -> list of keys in od'
        return list(self)

    def values(self):
        'od.values() -> list of values in od'
        return [self[key] for key in self]

    def items(self):
        'od.items() -> list of (key, value) pairs in od'
        return [(key, self[key]) for key in self]

    def iterkeys(self):
        'od.iterkeys() -> an iterator over the keys in od'
        return iter(self)

    def itervalues(self):
        'od.itervalues -> an iterator over the values in od'
        for k in self:
            yield self[k]

    def iteritems(self):
        'od.iteritems -> an iterator over the (key, value) items in od'
        for k in self:
            yield (k, self[k])

    def update(*args, **kwds):
        '''od.update(E, **F) -> None.  Update od from dict/iterable E and F.

        If E is a dict instance, does:           for k in E: od[k] = E[k]
        If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
        Or if E is an iterable of items, does:   for k, v in E: od[k] = v
        In either case, this is followed by:     for k, v in F.items(): od[k] = v

        '''
        if len(args) > 2:
            raise TypeError('update() takes at most 2 positional '
                            'arguments (%d given)' % (len(args),))
        elif not args:
            raise TypeError('update() takes at least 1 argument (0 given)')
        self = args[0]
        # Make progressively weaker assumptions about "other"
        other = ()
        if len(args) == 2:
            other = args[1]
        if isinstance(other, dict):
            for key in other:
                self[key] = other[key]
        elif hasattr(other, 'keys'):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwds.items():
            self[key] = value

    __update = update  # let subclasses override update without breaking __init__

    __marker = object()

    def pop(self, key, default=__marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.

        '''
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        if key in self:
            return self[key]
        self[key] = default
        return default

    def __repr__(self, _repr_running={}):
        'od.__repr__() <==> repr(od)'
        call_key = id(self), _get_ident()
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())
        finally:
            del _repr_running[call_key]

    def __reduce__(self):
        'Return state information for pickling'
        items = [[k, self[k]] for k in self]
        inst_dict = vars(self).copy()
        for k in vars(OrderedDict()):
            inst_dict.pop(k, None)
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        '''
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''
        if isinstance(other, OrderedDict):
            return len(self)==len(other) and self.items() == other.items()
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

    # -- the following methods are only used in Python 2.7 --

    def viewkeys(self):
        "od.viewkeys() -> a set-like object providing a view on od's keys"
        return KeysView(self)

    def viewvalues(self):
        "od.viewvalues() -> an object providing a view on od's values"
        return ValuesView(self)

    def viewitems(self):
        "od.viewitems() -> a set-like object providing a view on od's items"
        return ItemsView(self)
## end of http://code.activestate.com/recipes/576693/ }}}

if not hasattr(collections, 'OrderedDict'):
	collections.OrderedDict = BackportOrderedDict
