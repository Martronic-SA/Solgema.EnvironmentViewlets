import logging
from zope import schema
from zope.interface import Interface
from Products.Archetypes.config import REFERENCE_CATALOG
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.CMFCore.utils import getToolByName
from plone.app.uuid.utils import uuidToObject
from zope.annotation.interfaces import IAnnotations
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
try:
    from plone.app.contenttypes.migration.migration import ICustomMigrator
    from plone.app.contenttypes.migration.field_migrators import migrate_filefield, migrate_simplefield
    from plone.app.contenttypes.migration.utils import link_items
    from z3c.relationfield.relation import RelationValue
except:
    class ICustomMigrator(Interface):
        """""" 
try:
    from zope.intid.interfaces import IIntIds
except ImportError:
    from zope.app.intid.interfaces import IIntIds
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from zope.component import adapter
from Products.Five.utilities import marker
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IBool
from zope.component import getAllUtilitiesRegisteredFor
from plone.dexterity.interfaces import IDexterityFTI, IDexterityContent
from Solgema.EnvironmentViewlets.interfaces import IBandeauMarker, IBandeauContent, IFooterMarker,\
IFooterContent, IPrintFooterMarker, IPrintFooterContent, ILogoMarker, ILogoContent, IPrintLogoMarker,\
IPrintLogoContent, IBackgroundMarker, IBackgroundContent
_logger = logging.getLogger(__name__)

@implementer(ICustomMigrator)
@adapter(IBandeauMarker)
class BandeauMigator(object):

    def __init__(self, context):
        self.context = context
    
    def migrate(self, old, new):
        marker.mark(new, IBandeauMarker)
            
        for name, field in schema.getFieldsInOrder(IBandeauContent):
            migrate_simplefield(old, IBandeauContent(new), name, name)

        _logger.info(
            "Migrating Bandeau Content for %s" % new.absolute_url())
            
@implementer(ICustomMigrator)
@adapter(IFooterMarker)
class FooterMigator(object):

    def __init__(self, context):
        self.context = context
    
    def migrate(self, old, new):
        marker.mark(new, IFooterMarker)
            
        for name, field in schema.getFieldsInOrder(IFooterContent):
            migrate_simplefield(old, IFooterContent(new), name, name)

        _logger.info(
            "Migrating Footer Content for %s" % new.absolute_url())
            
@implementer(ICustomMigrator)
@adapter(IPrintFooterMarker)
class PrintFooterMigator(object):

    def __init__(self, context):
        self.context = context
    
    def migrate(self, old, new):
        marker.mark(new, IPrintFooterMarker)
            
        for name, field in schema.getFieldsInOrder(IPrintFooterContent):
            migrate_simplefield(old, IPrintFooterContent(new), name, name)

        _logger.info(
            "Migrating PrintFooter Content for %s" % new.absolute_url())

        _logger.info(
            "Migrating Footer Content for %s" % new.absolute_url())
            
@implementer(ICustomMigrator)
@adapter(ILogoMarker)
class LogoMigator(object):

    def __init__(self, context):
        self.context = context
    
    def migrate(self, old, new):
        marker.mark(new, ILogoMarker)
            
        for name, field in schema.getFieldsInOrder(ILogoContent):
            migrate_simplefield(old, ILogoContent(new), name, name)

        _logger.info(
            "Migrating Logo Content for %s" % new.absolute_url())
            
@implementer(ICustomMigrator)
@adapter(IPrintLogoMarker)
class PrintLogoMigator(object):

    def __init__(self, context):
        self.context = context
    
    def migrate(self, old, new):
        marker.mark(new, IPrintLogoMarker)
            
        for name, field in schema.getFieldsInOrder(IPrintLogoContent):
            migrate_simplefield(old, IPrintLogoContent(new), name, name)

        _logger.info(
            "Migrating PrintLogo Content for %s" % new.absolute_url())
            
@implementer(ICustomMigrator)
@adapter(IBackgroundMarker)
class BackgroundMigator(object):

    def __init__(self, context):
        self.context = context
    
    def migrate(self, old, new):
        marker.mark(new, IBackgroundMarker)
            
        for name, field in schema.getFieldsInOrder(IBackgroundContent):
            migrate_simplefield(old, IBackgroundContent(new), name, name)

        _logger.info(
            "Migrating PrintLogo Content for %s" % new.absolute_url())
