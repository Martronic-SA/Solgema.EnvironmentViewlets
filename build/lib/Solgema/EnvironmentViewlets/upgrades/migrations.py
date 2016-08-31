import logging
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from Products.Five.utilities import marker

LOG = logging.getLogger('Solgema.EnvironmentViewlets')

def update02(context):
    catalogindexes = ['localBanner',
                      'stopAcquisitionBanner',
                      'localFooter',
                      'stopAcquisitionFooter',
                      'localPrintFooter',
                      'stopAcquisitionPrintFooter',
                      'localLogo',
                      'localPrintLogo']
    portal_catalog = getToolByName(context, 'portal_catalog')
    for index in catalogindexes:
        try:
            portal_catalog.manage_delIndex(index)
        except:
            pass
        try:
            portal_catalog.manage_delColumn(index)
        except:
            pass
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets.upgrades:update02')
    interfaceslist = ['Solgema.EnvironmentViewlets.interfaces.IBandeauMarker',
                      'Solgema.EnvironmentViewlets.interfaces.IFooterMarker',
                      'Solgema.EnvironmentViewlets.interfaces.IPrintFooterMarker',
                      'Solgema.EnvironmentViewlets.interfaces.ILogoMarker',
                      'Solgema.EnvironmentViewlets.interfaces.IPrintLogoMarker']
    items = [a.getObject() for a in portal_catalog.searchResults(object_provides={'query':interfaceslist, 'operator':'or'})]
    for item in items:
        portal_catalog.catalog_object(item)
        LOG.info(item.id+' has been updated.')

def update03(context):
    portal_catalog = getToolByName(context, 'portal_catalog')
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets.upgrades:update03')
    interfaceslist = ['Solgema.EnvironmentViewlets.interfaces.IBandeauMarker',]
    items = [a.getObject() for a in portal_catalog.searchResults(object_provides={'query':interfaceslist, 'operator':'or'})]
    for item in items:
        portal_catalog.catalog_object(item)
        LOG.info(item.id+' has been updated.')

def update04(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Solgema.EnvironmentViewlets.upgrades:update04')

