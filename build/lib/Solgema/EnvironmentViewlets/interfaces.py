import datetime
from zope.interface import Interface, Attribute, directlyProvides
from zope import schema
from zope.schema.interfaces import ValidationError
from zope.formlib.interfaces import IInputWidget, IDisplayWidget
from zope.container.interfaces import IContainer
from zope.browser.interfaces import IAdding
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
import zope.viewlet.interfaces
from plone.formwidget.contenttree import PathSourceBinder
from Products.ATContentTypes.interface import IATFolder
from Products.CMFCore.utils import getToolByName
from zope.viewlet.interfaces import IViewletManager

from zope.browsermenu.interfaces import IBrowserMenu
from zope.browsermenu.interfaces import IBrowserSubMenuItem

from zope.contentprovider.interfaces import IContentProvider
try:
    from zope.component.interfaces import IObjectEvent
except ImportError:
    # BBB for Zope 2.9
    from zope.app.event.interfaces import IObjectEvent

from zope.schema import interfaces as izs
from zope.interface import Interface

from zope.container.constraints import contains

from Solgema.EnvironmentViewlets.config import _

###### INTERFACES

class IPersistentOptions( Interface ):
    """
    a base interface that our persistent option annotation settings,
    can adapt to. specific schemas that want to have context stored
    annotation values should subclass from this interface, so they
    use adapation to get access to persistent settings. for example,
    settings = IMySettings(context)
    """

class ISolgemaEnvironmentViewletsLayer( IDefaultPloneLayer ):
    """Solgema Immo layer""" 

class IEnvironmentMarker( Interface ):
    """Marker for Real Estate Content"""
    
class IBandeauMarker( IEnvironmentMarker ):
    """Marker for Real Estate Content"""

class IBandeauContent( Interface ):
    """
    Bandeau informations
    """

    bannerLocalOnly = schema.Bool(
        title = _(u"label_bannerLocalOnly", default=(u"Local Banner")),
        description=_(u'help_bannerLocalOnly', default=u"Display the banner in the current folder only"),
        required = False,
        default = False,
        )

    bannerStopAcquisition = schema.Bool(
        title = _(u"label_bannerStopAcquisition", default=(u"Stop Acquisition")),
        description=_(u'help_bannerStopAcquisition', default=u"Stop banners research to this folder and don't display banners in upper folders"),
        required = False,
        default = True,
        )
    
    bannerImageLink = schema.Choice(
        title=_(u"label_bannerImageLink", default=u"A link for the banner"),
        source=PathSourceBinder(portal_type=['Document', 'Folder']),
        required = False
        )


class IFooterMarker( IEnvironmentMarker ):
    """Marker for Real Estate Content"""

class IFooterContent( Interface ):
    """
    Bandeau informations
    """

    footerLocalOnly = schema.Bool(
        title = _(u"label_footerLocalOnly", default=(u"Local Footer")),
        description=_(u'help_footerLocalOnly', default=u"Display the footer in the current folder only"),
        required = False,
        default = False,
        )

    footerStopAcquisition = schema.Bool(
        title = _(u"label_footerStopAcquisition", default=(u"Stop Acquisition")),
        description=_(u'help_footerStopAcquisition', default=u"Stop footers research to this folder and don't display footers in upper folders"),
        required = False,
        default = True,
        )

class IPrintFooterMarker( IEnvironmentMarker ):
    """Marker for Real Estate Content"""

class IPrintFooterContent( Interface ):
    """
    Bandeau informations
    """

    printfooterLocalOnly = schema.Bool(
        title = _(u"label_printfooterLocalOnly", default=(u"Local Footer")),
        description=_(u'help_printfooterLocalOnly', default=u"Display the footer in the current folder only"),
        required = False,
        default = False,
        )

    printfooterStopAcquisition = schema.Bool(
        title = _(u"label_printfooterStopAcquisition", default=(u"Stop Acquisition")),
        description=_(u'help_printfooterStopAcquisition', default=u"Stop footers research to this folder and don't display footers in upper folders"),
        required = False,
        default = True,
        )

class ILogoMarker( IEnvironmentMarker ):
    """Marker for Real Estate Content"""

class ILogoContent( Interface ):
    """
    Bandeau informations
    """

    logoLocalOnly = schema.Bool(
        title = _(u"label_logoLocalOnly", default=(u"Local Logo")),
        description=_(u'help_logoLocalOnly', default=u"Display the logo in the current folder only"),
        required = False,
        default = False,
        )

class IPrintLogoMarker( IEnvironmentMarker ):
    """Marker for Real Estate Content"""

class IPrintLogoContent( Interface ):
    """
    Bandeau informations
    """

    printlogoLocalOnly = schema.Bool(
        title = _(u"label_printlogoLocalOnly", default=(u"Local Print Logo")),
        description=_(u'help_printlogoLocalOnly', default=u"Display the logo for pinting in the current folder only"),
        required = False,
        default = False,
        )

class IBackgroundMarker( IEnvironmentMarker ):
    """Marker for Real Estate Content"""

class IBackgroundContent( Interface ):
    """
    Bandeau informations
    """

    bannerLocalOnly = schema.Bool(
        title = _(u"label_bannerLocalOnly", default=(u"Local Banner")),
        description=_(u'help_bannerLocalOnly', default=u"Display the banner in the current folder only"),
        required = False,
        default = False,
        )

    bannerStopAcquisition = schema.Bool(
        title = _(u"label_bannerStopAcquisition", default=(u"Stop Acquisition")),
        description=_(u'help_bannerStopAcquisition', default=u"Stop banners research to this folder and don't display banners in upper folders"),
        required = False,
        default = True,
        )
    
    bannerImageLink = schema.Choice(
        title=_(u"label_bannerImageLink", default=u"A link for the banner"),
        source=PathSourceBinder(portal_type=['Document', 'Folder'])
        )
    
    backgroundRepeat = schema.Choice(
        title=_(u"label_backgroundRepeat", default=u"Repeat the background"),
        values = ['no-repeat',
                  'repeat-x',
                  'repeat-y',
                  'repeat'],
        required = True,
        )
    
    backgroundExtend = schema.Bool(
        title=_(u"label_backgroundExtend", default=u"Extend the background"),
        required = True,
        default = True,
        )
    
    backgroundFixed = schema.Bool(
        title=_(u"label_backgroundFixed", default=u"Fix the background"),
        required = True,
        default = True,
        )
    
    backgroundAlign = schema.Choice(
        title=_(u"label_backgroundAlign", default=u"Background alignment"),
        values = ['left','center','right'],
        )

class IEnvironmentCreationEvent( IObjectEvent ):
    """ sent out when a payable is created
    """

    item = Attribute("object implementing environment interface")    
    environment_interface = Attribute("environment interface the object implements")

class IEnvironmentModificationEvent( IEnvironmentCreationEvent ):
    """"""


######################################

class ISolgemaBandeauManager(IViewletManager):
    """bandeauManager"""

class ISolgemaFooterManager(IViewletManager):
    """bandeauManager"""

class ISolgemaPrintFooterManager(IViewletManager):
    """bandeauManager"""

################# MENU

class ISolgemaEnvironmentActionsSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the actions menu.
    """

class ISolgemaEnvironmentActionsMenu(IBrowserMenu):
    """The actions menu.

    This gets its menu items from portal_actions.
    """
