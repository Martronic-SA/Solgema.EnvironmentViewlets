# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
$Id: options.py 1516 2008-05-03 12:57:53Z cwithers $
"""
try:
    from zope.annotation import IAnnotations
except ImportError:
    # BBB for Zope 2.9
    from zope.app.annotation import IAnnotations
from persistent.dict import PersistentDict
from persistent import Persistent
from zope import schema
from zope.interface import classImplements, implements

import interfaces

_marker = object()

class PropertyBag( object ):
    """ you can subclass and init to a particular schema, meant for transient adapter bags
    """
    def __init__( self, **kw ):
        for field_name, field in schema.getFieldsInOrder( self.schema ):
            if field_name in kw:
                field.set( self, kw[ field_name ] )

    @classmethod
    def initclass( cls, iface ):
        cls.schema = iface
        for field_name, field in schema.getFieldsInOrder( iface ):
            setattr( cls, field_name, field.default )
        classImplements( cls, iface )            

    @classmethod
    def makeclass( cls, schema ):
        klass = type( "transientbag", ( cls, ), {} )
        klass.initclass( schema )
        classImplements( klass, schema )
        return klass

    @classmethod
    def makeinstance( cls, schema ):
        return cls.makeclass( schema )()
        
    # post initialziation class method
    @classmethod
    def frominstance( cls, instance):
        assert cls.schema.providedBy( instance )
        d = {}
        for field_name, field in schema.getFieldsInOrder( cls.schema ):
            d[field_name] = field.get(instance)
        return cls( **d )
        
class PersistentBag( Persistent, PropertyBag):

    def getProperty( self, property_name ):
        return getattr( self, property_name, None )

    def setProperty( self, property_name, property_value ):
        setattr( self, property_name, property_value )
        self._p_changed = True
        
class PersistentOptions( object ):

    implements( interfaces.IPersistentOptions )
    
    _storage = None
    
    def __init__( self, context ):
        self.context = context

    def storage( self, name=None ):
        """ name if given is the key of a persistent dictionary off of
        the annotation.
        """ 
        if self._storage is None:
            annotations = IAnnotations( self.context )
            self._storage = annotations.get( self.annotation_key, None )
            if self._storage is None:
                annotations[ self.annotation_key ] = self._storage = PersistentDict()

        if name is None:
            return self._storage
        if name in self._storage:
            return self._storage[name]
        
        self._storage[ name ] = PersistentDict()
        return self._storage[name]

    def getProperty( self, property_name ):
        return self.storage().get( property_name )

    def getFieldProperty( self, field ):
        value = self.storage().get( field.__name__, _marker )
        if value is _marker:
            return field.default
        return value
    
    def setProperty( self, property_name, property_value ):
        self.storage()[ property_name ] = property_value

    def nullProperty( self, *args):
        return None

    def wire( cls, name, key, *interfaces, **options ):
        fields = {}
        bases = (cls, ) + options.get('bases', ())
        
        for iface in interfaces:
            for field in schema.getFields( iface ).values():
                fields[ field.__name__ ] = property( lambda self, field=field: self.getFieldProperty( field ),
                lambda self, value, field_name=field.__name__: self.setProperty( field_name, value ) )
        new_class = type( name, bases, fields)
        cls.annotation_key = key
        classImplements( new_class, interfaces )
        return new_class

    wire = classmethod( wire )

