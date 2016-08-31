import logging
from zope import component
from zope.component.hooks import getSite
from Products.CMFPlone import CatalogTool
from Products.CMFCore.utils import getToolByName
from plone.indexer.decorator import indexer
from zope.component import getMultiAdapter

from Solgema.EnvironmentViewlets.interfaces import *
LOG = logging.getLogger('Solgema.EnvironmentViewlets')

@indexer(IEnvironmentMarker)
def get_localEnvironment(object):
    if IBandeauMarker.providedBy(object):
        adapted = IBandeauContent(object, None)
        if adapted is not None:
            return adapted.bannerLocalOnly
    elif IFooterMarker.providedBy(object):
        adapted = IFooterContent(object, None)
        if adapted is not None:
            return adapted.footerLocalOnly
    elif IPrintFooterMarker.providedBy(object):
        adapted = IPrintFooterContent(object, None)
        if adapted is not None:
            return adapted.printfooterLocalOnly
    elif ILogoMarker.providedBy(object):
        adapted = ILogoContent(object, None)
        if adapted is not None:
            return adapted.logoLocalOnly
    elif IPrintLogoMarker.providedBy(object):
        adapted = IPrintLogoContent(object, None)
        if adapted is not None:
            return adapted.printlogoLocalOnly
    elif IBackgroundMarker.providedBy(object):
        adapted = IBackgroundContent(object, None)
        if adapted is not None:
            return adapted.bannerLocalOnly
    return None

@indexer(IEnvironmentMarker)
def get_stopAcquisitionEnvironment(object):
    if IBandeauMarker.providedBy(object):
        adapted = IBandeauContent(object, None)
        if adapted is not None:
            return adapted.bannerStopAcquisition
    if IFooterMarker.providedBy(object):
        adapted = IFooterContent(object, None)
        if adapted is not None:
            return adapted.footerStopAcquisition
    if IPrintFooterMarker.providedBy(object):
        adapted = IPrintFooterContent(object, None)
        if adapted is not None:
            return adapted.printfooterStopAcquisition
    if IBackgroundMarker.providedBy(object):
        adapted = IBackgroundContent(object, None)
        if adapted is not None:
            return adapted.bannerStopAcquisition
     
    return None

@indexer(IEnvironmentMarker)
def get_bannerImageLink(object):
    portal = getSite()
    context_state = getMultiAdapter((object, object.REQUEST), name=u'plone_context_state')
    folder = context_state.folder()
    folder_path = '/'.join(folder.getPhysicalPath())
    if IBandeauMarker.providedBy(object):
        adapted = IBandeauContent(object, None)
        if adapted is not None and getattr(adapted, 'bannerImageLink', None):
            return portal.restrictedTraverse(folder_path+adapted.bannerImageLink).UID()
    elif IFooterMarker.providedBy(object):
        adapted = IFooterContent(object, None)
        if adapted is not None and getattr(adapted, 'bannerImageLink', None):
            return portal.restrictedTraverse(folder_path+adapted.bannerImageLink).UID()
    elif ILogoMarker.providedBy(object):
        adapted = ILogoContent(object, None)
        if adapted is not None and getattr(adapted, 'bannerImageLink', None):
            return portal.restrictedTraverse(folder_path+adapted.bannerImageLink).UID()
    elif IBackgroundMarker.providedBy(object):
        adapted = IBackgroundContent(object, None)
        if adapted is not None and getattr(adapted, 'bannerImageLink', None):
            return portal.restrictedTraverse(folder_path+adapted.bannerImageLink).UID()
    return None

@indexer(IEnvironmentMarker)
def get_backgroundRepeat(object):
    adapted = IBackgroundContent(object, None)
    if adapted:
        return adapted.backgroundRepeat
    return None

@indexer(IEnvironmentMarker)
def get_backgroundExtend(object):
    adapted = IBackgroundContent(object, None)
    if adapted:
        return adapted.backgroundExtend
    return None

@indexer(IEnvironmentMarker)
def get_backgroundFixed(object):
    adapted = IBackgroundContent(object, None)
    if adapted:
        return adapted.backgroundFixed
    return None

@indexer(IEnvironmentMarker)
def get_backgroundAlign(object):
    adapted = IBackgroundContent(object, None)
    if adapted:
        return adapted.backgroundAlign
    return None

