import logging
from Acquisition import aq_parent, aq_inner
from urllib import urlencode
import zope.lifecycleevent
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.utilities import marker

from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.app.layout.icons.interfaces import IContentIcon
from plone.app.layout.icons.icons import BaseIcon
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.blob.interfaces import IATBlobImage
from plone.z3cform.layout import wrap_form

from zope.formlib import form
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.i18nmessageid import MessageFactory
from zope.event import notify
_ = MessageFactory('plone')

try:
    from plone.app.contenttypes.interfaces import IDocument, IImage
    has_dx = True
except:
    has_dx = False

from z3c.form import form as z3cform, field as z3cfield
from z3c.form import widget, button

from Products.ATContentTypes.interface import IATFolder, IATTopic, IATImage

from Solgema.EnvironmentViewlets.config import _
from Solgema.EnvironmentViewlets import event, interfaces, options
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
_logger = logging.getLogger(__name__)

def view_url(context):
    portalProperties = getToolByName(context, 'portal_properties')
    siteProperties = getattr(portalProperties, 'site_properties', None)
    useViewAction = []
    if siteProperties is not None:
        useViewAction = siteProperties.getProperty('typesUseViewActionInListings', None)
    if useViewAction == None:
        registry = getUtility(IRegistry)
        useViewAction = frozenset(
            registry.get('plone.types_use_view_action_in_listings', []))
    _logger.info(useViewAction)
    _logger.info(context.portal_type)   
    extra = ''
    if context.portal_type in useViewAction:
        extra = '/view'
    return extra

class EnvironmentFormView( z3cform.EditForm ):

    adapters = None
    interface = None
    marker = None
    fields = z3cfield.Fields()

class BaseEnvironmentForm( EnvironmentFormView ):

    def allowed( self ):
        adapter = component.queryAdapter( self.context, self.interface )
        return not ( adapter is None )

class EnvironmentFormCreation( BaseEnvironmentForm ):

    actions = form.Actions()

    def update( self ):
        marker.mark( self.context, self.marker )
        self.adapters = { self.interface : options.PropertyBag.makeinstance( self.interface ),
                          self.interface : options.PropertyBag.makeinstance( self.interface ) }

        return super( BaseEnvironmentForm, self).update()

    @button.buttonAndHandler(_('label_enable'), name='activate')
    def activateEnvironment( self, action):
        data, errors = self.extractData()
        changes = self.applyChanges(data)
        notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
        notify(
            event.EnvironmentCreationEvent( self.context, self.adapters[ self.interface ], self.interface )
            )

        # redirect to view

        translated_message = self.context.utranslate(u'Changes saved.', domain='plone').encode('utf-8')
        encoded_message = urlencode({'portal_status_message' : translated_message})
        extra = view_url(self.context)
        getToolByName(self.context, 'portal_css').cookResources()
        self.request.response.redirect( '%s%s?%s' % (self.context.absolute_url(), extra, encoded_message) )

    @button.buttonAndHandler(_('label_cancel'), name='cancel')
    def handleCancel( self, action):
        marker.erase( self.context, self.marker )
        self.request.RESPONSE.redirect( self.context.absolute_url() )

class EnvironmentEdit( BaseEnvironmentForm ):

    @button.buttonAndHandler(_('label_save'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        changes = self.applyChanges(data)
        if changes:
            notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            notify(
                event.EnvironmentModificationEvent( self.context, self.interface, self.interface )
                )
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage
        extra = view_url(self.context)
        getToolByName(self.context, 'portal_css').cookResources()
        self.request.response.redirect( '%s%s' % (self.context.absolute_url(), extra) )

    @button.buttonAndHandler(_('label_cancel'), name='cancel')
    def handleCancel( self, action):
        self.request.RESPONSE.redirect( self.context.absolute_url() )

##### BANNER

class SolgemaBandeauDestruction( BrowserView ):
    marker = interfaces.IBandeauMarker
    def __call__(self):
        marker.erase( self.context, self.marker )
        self.context.reindexObject()
        notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
        extra = view_url(self.context)
        getToolByName(self.context, 'portal_css').cookResources()
        self.request.response.redirect( '%s%s' % (self.context.absolute_url(), extra) )

class BandeauForm( BaseEnvironmentForm ):
    interface = interfaces.IBandeauContent
    marker = interfaces.IBandeauMarker

    @property
    def fields(self):
        if IATImage.providedBy(self.context):
            fields = z3cfield.Fields( self.interface )
            fields['bannerImageLink'].widgetFactory = ContentTreeFieldWidget
        else:
            fields = z3cfield.Fields( self.interface ).select('bannerLocalOnly', 'bannerStopAcquisition')
        return fields

class ZBandeauCreation( BandeauForm, EnvironmentFormCreation ):
    actions = EnvironmentFormCreation.actions
    update  = EnvironmentFormCreation.update

class ZBandeauEdit( BandeauForm, EnvironmentEdit ):
    pass

SolgemaBandeauCreation = wrap_form(ZBandeauCreation)
SolgemaBandeauEdit = wrap_form(ZBandeauEdit)

##### FOOTER

class FooterForm( BaseEnvironmentForm ):
    interface = interfaces.IFooterContent
    marker = interfaces.IFooterMarker
    fields = z3cfield.Fields( interface )

class ZFooterCreation(FooterForm, EnvironmentFormCreation ):
    actions = EnvironmentFormCreation.actions
    update  = EnvironmentFormCreation.update

class ZFooterEdit(FooterForm, EnvironmentEdit ):
    pass

SolgemaFooterCreation = wrap_form(ZFooterCreation)
SolgemaFooterEdit = wrap_form(ZFooterEdit)

class SolgemaFooterDestruction( SolgemaBandeauDestruction ):
    marker = interfaces.IFooterMarker

##### PRINT FOOTER

class PrintFooterForm( BaseEnvironmentForm ):
    interface = interfaces.IPrintFooterContent
    marker = interfaces.IPrintFooterMarker
    fields = z3cfield.Fields( interface )

class ZPrintFooterCreation(PrintFooterForm, EnvironmentFormCreation ):
    actions = EnvironmentFormCreation.actions
    update  = EnvironmentFormCreation.update

class ZPrintFooterEdit(PrintFooterForm, EnvironmentEdit ):
    pass

SolgemaPrintFooterCreation = wrap_form(ZPrintFooterCreation)
SolgemaPrintFooterEdit = wrap_form(ZPrintFooterEdit)

class SolgemaPrintFooterDestruction( SolgemaBandeauDestruction ):
    marker = interfaces.IPrintFooterMarker

##### LOGO

class LogoForm( BaseEnvironmentForm ):
    interface = interfaces.ILogoContent
    marker = interfaces.ILogoMarker
    fields = z3cfield.Fields( interface )

class ZLogoCreation(LogoForm, EnvironmentFormCreation ):
    actions = EnvironmentFormCreation.actions
    update  = EnvironmentFormCreation.update

class ZLogoEdit(LogoForm, EnvironmentEdit ):
    pass

SolgemaLogoCreation = wrap_form(ZLogoCreation)
SolgemaLogoEdit = wrap_form(ZLogoEdit)

class SolgemaLogoDestruction( SolgemaBandeauDestruction ):
    marker = interfaces.ILogoMarker

##### PRINT LOGO

class PrintLogoForm( BaseEnvironmentForm ):
    interface = interfaces.IPrintLogoContent
    marker = interfaces.IPrintLogoMarker
    fields = z3cfield.Fields( interface )

class ZPrintLogoCreation(PrintLogoForm, EnvironmentFormCreation ):
    actions = EnvironmentFormCreation.actions
    update  = EnvironmentFormCreation.update

class ZPrintLogoEdit(PrintLogoForm, EnvironmentEdit ):
    pass

SolgemaPrintLogoCreation = wrap_form(ZPrintLogoCreation)
SolgemaPrintLogoEdit = wrap_form(ZPrintLogoEdit)

class SolgemaPrintLogoDestruction( SolgemaBandeauDestruction ):
    marker = interfaces.IPrintLogoMarker

##### Background image

class BackgroundForm( BaseEnvironmentForm ):
    interface = interfaces.IBackgroundContent
    marker = interfaces.IBackgroundMarker

    @property
    def fields(self):
        if IATBlobImage.providedBy(self.context) or (has_dx and IImage.providedBy(self.context)):
            fields = z3cfield.Fields( self.interface )
            fields['bannerImageLink'].widgetFactory = ContentTreeFieldWidget
        else:
            fields = z3cfield.Fields( self.interface ).select('bannerLocalOnly', 'bannerStopAcquisition')
        return fields

class ZBackgroundCreation(BackgroundForm, EnvironmentFormCreation ):
    actions = EnvironmentFormCreation.actions
    update  = EnvironmentFormCreation.update

class ZBackgroundEdit(BackgroundForm, EnvironmentEdit ):
    pass

SolgemaBackgroundCreation = wrap_form(ZBackgroundCreation)
SolgemaBackgroundEdit = wrap_form(ZBackgroundEdit)

class SolgemaBackgroundDestruction( SolgemaBandeauDestruction ):
    marker = interfaces.IBackgroundMarker

class SolgemaBandeauContentControl( BrowserView ):
    """ conditions for presenting various actions
    """

    __allow_access_to_unprotected_subobjects__ = 1
    #__slots__ = ( 'context', 'request', 'options' )

    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def canBandeau( self ):
        if has_dx and (IDocument.providedBy(self.context) or IImage.providedBy(self.context)):
            return True
        if hasattr(self.context, 'getText'):
            return True
        if hasattr(self.context, 'tag'):
            return True
        if self.context.portal_type == 'Collage':
            return True
        if self.context.portal_type == 'FlashMovie':
            return True
        if self.context.portal_type == 'Folder':
            return True
        return False

    def canLogo( self ):
        if has_dx and (IDocument.providedBy(self.context) or IImage.providedBy(self.context)):
            return True
        if hasattr(self.context, 'getText'):
            return True
        if hasattr(self.context, 'tag'):
            return True
        if self.context.portal_type == 'FlashMovie':
            return True
        return False

    # BACKGROUND

    def canBackground( self ):
        if has_dx and IImage.providedBy(self.context):
            return True
        return IATBlobImage.providedBy(self.context)

    def isBackground( self ):
        return interfaces.IBackgroundMarker.providedBy( self.context )

    isBackground.__roles__ = None

    def allowActivateBackground( self ):
        return self.canBackground() and not self.isBackground()

    allowActivateBackground.__roles__ = None

    def allowDeactivateBackground( self ):
        return self.isBackground()

    allowDeactivateBackground.__roles__ = None
        
    # BANNER

    def isBandeau( self ):
        return interfaces.IBandeauMarker.providedBy( self.context )

    isBandeau.__roles__ = None

    def allowActivateBandeau( self ):
        return self.canBandeau() and not self.isBandeau()

    allowActivateBandeau.__roles__ = None

    def allowDeactivateBandeau( self ):
        return self.isBandeau()

    allowDeactivateBandeau.__roles__ = None

    # FOOTER

    def isFooter( self ):
        return interfaces.IFooterMarker.providedBy( self.context )

    isFooter.__roles__ = None

    def allowActivateFooter( self ):
        return self.canBandeau() and not self.isFooter()

    allowActivateFooter.__roles__ = None

    def allowDeactivateFooter( self ):
        return self.isFooter()

    allowDeactivateFooter.__roles__ = None

    # Print FOOTER

    def isPrintFooter( self ):
        """  does the context implement the IRealEstate interface
        """
        return interfaces.IPrintFooterMarker.providedBy( self.context )

    isPrintFooter.__roles__ = None

    def allowActivatePrintFooter( self ):
        return self.canBandeau() and not self.isPrintFooter()

    allowActivatePrintFooter.__roles__ = None

    def allowDeactivatePrintFooter( self ):
        return self.isPrintFooter()

    allowDeactivatePrintFooter.__roles__ = None

    # Logo

    def isLogo( self ):
        """  does the context implement the IRealEstate interface
        """
        return interfaces.ILogoMarker.providedBy( self.context )

    isLogo.__roles__ = None

    def allowActivateLogo( self ):
        return self.canLogo() and not self.isLogo()

    allowActivateLogo.__roles__ = None

    def allowDeactivateLogo( self ):
        return self.isLogo()

    allowDeactivateLogo.__roles__ = None

    # Print Logo

    def isPrintLogo( self ):
        """  does the context implement the IRealEstate interface
        """
        return interfaces.IPrintLogoMarker.providedBy( self.context )

    isPrintLogo.__roles__ = None

    def allowActivatePrintLogo( self ):
        return self.canLogo() and not self.isPrintLogo()

    allowActivatePrintLogo.__roles__ = None

    def allowDeactivatePrintLogo( self ):
        return self.isPrintLogo()

    allowDeactivatePrintLogo.__roles__ = None

